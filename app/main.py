from __future__ import annotations

import json
import re
from datetime import datetime, timezone
from http import HTTPStatus
from itertools import count
from typing import Any, Callable
from wsgiref.simple_server import make_server

Json = dict[str, Any] | list[dict[str, Any]] | None
Handler = Callable[[dict[str, str], dict[str, Any], dict[str, str]], tuple[int, Json]]

ROUTES: list[tuple[str, re.Pattern[str], Handler]] = []

_counters = {
    "pigeons": count(1),
    "breeding": count(1),
    "health": count(1),
    "race": count(1),
    "files": count(1),
    "announcements": count(1),
}

_store: dict[str, dict[str, dict[str, Any]]] = {
    "users": {},
    "pigeons": {},
    "breeding": {},
    "health": {},
    "race": {},
    "files": {},
    "knowledge": {
        "1": {
            "id": "1",
            "title": "Foundations of Racing Pigeon Care",
            "content": "A starter article covering nutrition, loft hygiene, training, and observation.",
            "tags": ["care", "training"],
        }
    },
    "announcements": {},
}


def route(method: str, path_template: str) -> Callable[[Handler], Handler]:
    """Register a JSON endpoint with simple {parameter} path matching."""

    pattern = "^" + re.sub(r"\{([A-Za-z_][A-Za-z0-9_]*)\}", r"(?P<\1>[^/]+)", path_template) + "$"

    def decorator(handler: Handler) -> Handler:
        ROUTES.append((method.upper(), re.compile(pattern), handler))
        return handler

    return decorator


def _now() -> str:
    return datetime.now(timezone.utc).isoformat()


def _payload(body: dict[str, Any]) -> dict[str, Any]:
    data = body.get("data", body)
    return data if isinstance(data, dict) else {}


def _created(resource: str, payload: dict[str, Any]) -> dict[str, Any]:
    item_id = str(next(_counters[resource]))
    item = {"id": item_id, **payload, "created_at": _now(), "updated_at": _now()}
    _store[resource][item_id] = item
    return item


def _get(resource: str, item_id: str) -> dict[str, Any]:
    if item_id not in _store[resource]:
        raise KeyError(f"{resource} item not found")
    return _store[resource][item_id]


def _updated(resource: str, item_id: str, payload: dict[str, Any]) -> dict[str, Any]:
    item = _get(resource, item_id).copy()
    item.update(payload)
    item["updated_at"] = _now()
    _store[resource][item_id] = item
    return item


def handle_request(method: str, path: str, body: dict[str, Any] | None = None, query: dict[str, str] | None = None) -> tuple[int, Json]:
    """Dispatch a request to the in-process API router."""

    for route_method, pattern, handler in ROUTES:
        match = pattern.match(path)
        if route_method == method.upper() and match:
            try:
                return handler(match.groupdict(), body or {}, query or {})
            except KeyError as exc:
                return HTTPStatus.NOT_FOUND, {"detail": str(exc).strip("'")}
    return HTTPStatus.NOT_FOUND, {"detail": "Route not found"}


@route("POST", "/api/auth/register")
def register_user(_params: dict[str, str], body: dict[str, Any], _query: dict[str, str]) -> tuple[int, Json]:
    if "email" not in body or "password" not in body:
        return HTTPStatus.BAD_REQUEST, {"detail": "email and password are required"}
    user_id = str(len(_store["users"]) + 1)
    profile = {"id": user_id, "email": body["email"], "name": body.get("name"), "created_at": _now()}
    _store["users"][user_id] = profile
    return HTTPStatus.CREATED, {"user": profile, "access_token": f"access-{user_id}", "refresh_token": f"refresh-{user_id}"}


@route("POST", "/api/auth/login")
def login(_params: dict[str, str], body: dict[str, Any], _query: dict[str, str]) -> tuple[int, Json]:
    user = next((user for user in _store["users"].values() if user["email"] == body.get("email")), None)
    if user is None:
        return HTTPStatus.UNAUTHORIZED, {"detail": "Invalid credentials"}
    return HTTPStatus.OK, {"access_token": f"access-{user['id']}", "refresh_token": f"refresh-{user['id']}"}


@route("POST", "/api/auth/refresh")
def refresh_token(_params: dict[str, str], body: dict[str, Any], _query: dict[str, str]) -> tuple[int, Json]:
    refresh_token_value = str(body.get("refresh_token", ""))
    if not refresh_token_value.startswith("refresh-"):
        return HTTPStatus.UNAUTHORIZED, {"detail": "Invalid refresh token"}
    return HTTPStatus.OK, {"access_token": refresh_token_value.replace("refresh-", "access-", 1)}


@route("GET", "/api/user/profile")
def get_profile(_params: dict[str, str], _body: dict[str, Any], _query: dict[str, str]) -> tuple[int, Json]:
    profile = next(iter(_store["users"].values()), {"id": "demo", "email": "demo@example.com", "name": "Demo User"})
    return HTTPStatus.OK, profile


@route("PUT", "/api/user/profile")
def update_profile(_params: dict[str, str], body: dict[str, Any], _query: dict[str, str]) -> tuple[int, Json]:
    _status, current = get_profile({}, {}, {})
    profile = dict(current or {})
    profile.update({key: value for key, value in body.items() if value is not None})
    _store["users"][profile["id"]] = profile
    return HTTPStatus.OK, profile


@route("GET", "/api/pigeon")
def list_pigeons(_params: dict[str, str], _body: dict[str, Any], _query: dict[str, str]) -> tuple[int, Json]:
    return HTTPStatus.OK, list(_store["pigeons"].values())


@route("POST", "/api/pigeon")
def create_pigeon(_params: dict[str, str], body: dict[str, Any], _query: dict[str, str]) -> tuple[int, Json]:
    return HTTPStatus.CREATED, _created("pigeons", _payload(body))


@route("GET", "/api/pigeon/{id}")
def get_pigeon(params: dict[str, str], _body: dict[str, Any], _query: dict[str, str]) -> tuple[int, Json]:
    return HTTPStatus.OK, _get("pigeons", params["id"])


@route("PUT", "/api/pigeon/{id}")
def update_pigeon(params: dict[str, str], body: dict[str, Any], _query: dict[str, str]) -> tuple[int, Json]:
    return HTTPStatus.OK, _updated("pigeons", params["id"], _payload(body))


@route("DELETE", "/api/pigeon/{id}")
def delete_pigeon(params: dict[str, str], _body: dict[str, Any], _query: dict[str, str]) -> tuple[int, Json]:
    _get("pigeons", params["id"])
    del _store["pigeons"][params["id"]]
    return HTTPStatus.NO_CONTENT, None


@route("POST", "/api/pedigree/generate")
def generate_pedigree(_params: dict[str, str], body: dict[str, Any], _query: dict[str, str]) -> tuple[int, Json]:
    payload = _payload(body)
    return HTTPStatus.OK, {"pigeon_id": payload.get("pigeon_id"), "status": "generated", "generated_at": _now()}


@route("GET", "/api/pedigree/{pigeonId}")
def get_pedigree(params: dict[str, str], _body: dict[str, Any], _query: dict[str, str]) -> tuple[int, Json]:
    return HTTPStatus.OK, {"pigeon_id": params["pigeonId"], "ancestors": [], "descendants": []}


@route("GET", "/api/pedigree/tree/{pigeonId}")
def get_pedigree_tree(params: dict[str, str], _body: dict[str, Any], _query: dict[str, str]) -> tuple[int, Json]:
    pigeon_id = params["pigeonId"]
    return HTTPStatus.OK, {"pigeon_id": pigeon_id, "tree": {"id": pigeon_id, "parents": []}}


@route("POST", "/api/breeding")
def create_breeding(_params: dict[str, str], body: dict[str, Any], _query: dict[str, str]) -> tuple[int, Json]:
    return HTTPStatus.CREATED, _created("breeding", _payload(body))


@route("GET", "/api/breeding")
def list_breeding(_params: dict[str, str], _body: dict[str, Any], _query: dict[str, str]) -> tuple[int, Json]:
    return HTTPStatus.OK, list(_store["breeding"].values())


@route("POST", "/api/breeding/recommendation")
def breeding_recommendation(_params: dict[str, str], body: dict[str, Any], _query: dict[str, str]) -> tuple[int, Json]:
    return HTTPStatus.OK, {"recommendations": [], "criteria": _payload(body), "generated_at": _now()}


@route("POST", "/api/health")
def create_health_record(_params: dict[str, str], body: dict[str, Any], _query: dict[str, str]) -> tuple[int, Json]:
    return HTTPStatus.CREATED, _created("health", _payload(body))


@route("GET", "/api/health/{pigeonId}")
def get_health_records(params: dict[str, str], _body: dict[str, Any], _query: dict[str, str]) -> tuple[int, Json]:
    return HTTPStatus.OK, [record for record in _store["health"].values() if record.get("pigeon_id") == params["pigeonId"]]


@route("PUT", "/api/health/{recordId}")
def update_health_record(params: dict[str, str], body: dict[str, Any], _query: dict[str, str]) -> tuple[int, Json]:
    return HTTPStatus.OK, _updated("health", params["recordId"], _payload(body))


@route("POST", "/api/race")
def create_race(_params: dict[str, str], body: dict[str, Any], _query: dict[str, str]) -> tuple[int, Json]:
    return HTTPStatus.CREATED, _created("race", _payload(body))


@route("GET", "/api/race")
def list_races(_params: dict[str, str], _body: dict[str, Any], _query: dict[str, str]) -> tuple[int, Json]:
    return HTTPStatus.OK, list(_store["race"].values())


@route("GET", "/api/race/statistics")
def race_statistics(_params: dict[str, str], _body: dict[str, Any], _query: dict[str, str]) -> tuple[int, Json]:
    return HTTPStatus.OK, {"total_races": len(_store["race"]), "generated_at": _now()}


for _analysis_path in (
    "/api/ai/chat",
    "/api/ai/voice",
    "/api/ai/image-analysis",
    "/api/ai/excel-analysis",
    "/api/ai/pedigree-analysis",
    "/api/ai/breeding-analysis",
    "/api/ai/health-analysis",
):

    @route("POST", _analysis_path)
    def ai_endpoint(_params: dict[str, str], body: dict[str, Any], _query: dict[str, str], path: str = _analysis_path) -> tuple[int, Json]:
        return HTTPStatus.OK, {"endpoint": path, "analysis": {}, "input": _payload(body)}


@route("GET", "/api/weather/current")
def current_weather(_params: dict[str, str], _body: dict[str, Any], query: dict[str, str]) -> tuple[int, Json]:
    return HTTPStatus.OK, {"location": query.get("location", "loft"), "temperature_c": None, "conditions": "unavailable", "observed_at": _now()}


@route("GET", "/api/weather/forecast")
def weather_forecast(_params: dict[str, str], _body: dict[str, Any], query: dict[str, str]) -> tuple[int, Json]:
    return HTTPStatus.OK, {"location": query.get("location", "loft"), "forecast": []}


@route("POST", "/api/upload")
def upload_file(_params: dict[str, str], body: dict[str, Any], _query: dict[str, str]) -> tuple[int, Json]:
    return HTTPStatus.CREATED, _created("files", _payload(body))


@route("GET", "/api/files")
def list_files(_params: dict[str, str], _body: dict[str, Any], _query: dict[str, str]) -> tuple[int, Json]:
    return HTTPStatus.OK, list(_store["files"].values())


@route("DELETE", "/api/files/{id}")
def delete_file(params: dict[str, str], _body: dict[str, Any], _query: dict[str, str]) -> tuple[int, Json]:
    _get("files", params["id"])
    del _store["files"][params["id"]]
    return HTTPStatus.NO_CONTENT, None


@route("GET", "/api/knowledge/articles")
def knowledge_articles(_params: dict[str, str], _body: dict[str, Any], _query: dict[str, str]) -> tuple[int, Json]:
    return HTTPStatus.OK, list(_store["knowledge"].values())


@route("GET", "/api/knowledge/search")
def knowledge_search(_params: dict[str, str], _body: dict[str, Any], query: dict[str, str]) -> tuple[int, Json]:
    term = query.get("q", "").lower()
    return HTTPStatus.OK, [article for article in _store["knowledge"].values() if term in article["title"].lower() or term in article["content"].lower()]


@route("GET", "/api/knowledge/{id}")
def get_knowledge_article(params: dict[str, str], _body: dict[str, Any], _query: dict[str, str]) -> tuple[int, Json]:
    return HTTPStatus.OK, _get("knowledge", params["id"])


@route("POST", "/api/admin/announcement")
def create_announcement(_params: dict[str, str], body: dict[str, Any], _query: dict[str, str]) -> tuple[int, Json]:
    return HTTPStatus.CREATED, _created("announcements", _payload(body))


@route("GET", "/api/admin/users")
def admin_users(_params: dict[str, str], _body: dict[str, Any], _query: dict[str, str]) -> tuple[int, Json]:
    return HTTPStatus.OK, list(_store["users"].values())


@route("GET", "/api/admin/statistics")
def admin_statistics(_params: dict[str, str], _body: dict[str, Any], _query: dict[str, str]) -> tuple[int, Json]:
    return HTTPStatus.OK, {resource: len(items) for resource, items in _store.items()}


def application(environ: dict[str, Any], start_response: Callable[..., Any]) -> list[bytes]:
    method = environ["REQUEST_METHOD"]
    path = environ.get("PATH_INFO", "/")
    query = dict(pair.split("=", 1) if "=" in pair else (pair, "") for pair in filter(None, environ.get("QUERY_STRING", "").split("&")))
    length = int(environ.get("CONTENT_LENGTH") or 0)
    raw_body = environ["wsgi.input"].read(length) if length else b"{}"
    try:
        body = json.loads(raw_body.decode("utf-8") or "{}")
    except json.JSONDecodeError:
        body = {}
    status_code, response_body = handle_request(method, path, body, query)
    response_bytes = b"" if response_body is None else json.dumps(response_body).encode("utf-8")
    start_response(f"{status_code} {HTTPStatus(status_code).phrase}", [("Content-Type", "application/json"), ("Content-Length", str(len(response_bytes)))])
    return [response_bytes]


if __name__ == "__main__":
    with make_server("127.0.0.1", 8000, application) as server:
        print("Serving Pigeon AI API on http://127.0.0.1:8000")
        server.serve_forever()
