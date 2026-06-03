from http import HTTPStatus

from app.main import handle_request


def _payload(**data):
    return {"data": data}


def test_auth_and_profile_flow():
    status, body = handle_request(
        "POST",
        "/api/auth/register",
        {"email": "racer@example.com", "password": "secret", "name": "Racer"},
    )
    assert status == HTTPStatus.CREATED
    assert body["access_token"].startswith("access-")

    status, body = handle_request("POST", "/api/auth/login", {"email": "racer@example.com", "password": "secret"})
    assert status == HTTPStatus.OK
    refresh_token = body["refresh_token"]

    status, body = handle_request("POST", "/api/auth/refresh", {"refresh_token": refresh_token})
    assert status == HTTPStatus.OK
    assert body["access_token"].startswith("access-")

    status, _body = handle_request("GET", "/api/user/profile")
    assert status == HTTPStatus.OK
    status, body = handle_request("PUT", "/api/user/profile", {"name": "Champion Loft"})
    assert status == HTTPStatus.OK
    assert body["name"] == "Champion Loft"


def test_pigeon_crud_flow():
    status, pigeon = handle_request("POST", "/api/pigeon", _payload(ring_number="BE-123", name="Blue Star"))
    assert status == HTTPStatus.CREATED

    status, _body = handle_request("GET", "/api/pigeon")
    assert status == HTTPStatus.OK
    status, body = handle_request("GET", f"/api/pigeon/{pigeon['id']}")
    assert status == HTTPStatus.OK
    assert body["ring_number"] == "BE-123"

    status, body = handle_request("PUT", f"/api/pigeon/{pigeon['id']}", _payload(name="Blue Ace"))
    assert status == HTTPStatus.OK
    assert body["name"] == "Blue Ace"

    status, body = handle_request("DELETE", f"/api/pigeon/{pigeon['id']}")
    assert status == HTTPStatus.NO_CONTENT
    assert body is None


def test_requested_collection_and_analysis_routes():
    post_routes = [
        "/api/pedigree/generate",
        "/api/breeding",
        "/api/breeding/recommendation",
        "/api/health",
        "/api/race",
        "/api/ai/chat",
        "/api/ai/voice",
        "/api/ai/image-analysis",
        "/api/ai/excel-analysis",
        "/api/ai/pedigree-analysis",
        "/api/ai/breeding-analysis",
        "/api/ai/health-analysis",
        "/api/upload",
        "/api/admin/announcement",
    ]
    for path in post_routes:
        status, _body = handle_request("POST", path, _payload(pigeon_id="42", message="hello"))
        assert status in {HTTPStatus.OK, HTTPStatus.CREATED}, path

    get_routes = [
        ("/api/pedigree/42", {}),
        ("/api/pedigree/tree/42", {}),
        ("/api/breeding", {}),
        ("/api/health/42", {}),
        ("/api/race", {}),
        ("/api/race/statistics", {}),
        ("/api/weather/current", {}),
        ("/api/weather/forecast", {}),
        ("/api/files", {}),
        ("/api/knowledge/articles", {}),
        ("/api/knowledge/search", {"q": "pigeon"}),
        ("/api/knowledge/1", {}),
        ("/api/admin/users", {}),
        ("/api/admin/statistics", {}),
    ]
    for path, query in get_routes:
        status, _body = handle_request("GET", path, query=query)
        assert status == HTTPStatus.OK, path


def test_health_record_and_file_update_delete_routes():
    _status, health = handle_request("POST", "/api/health", _payload(pigeon_id="99", status="ok"))
    status, body = handle_request("PUT", f"/api/health/{health['id']}", _payload(status="recovered"))
    assert status == HTTPStatus.OK
    assert body["status"] == "recovered"

    _status, uploaded = handle_request("POST", "/api/upload", _payload(filename="loft.csv"))
    status, body = handle_request("DELETE", f"/api/files/{uploaded['id']}")
    assert status == HTTPStatus.NO_CONTENT
    assert body is None
