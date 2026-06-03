# Pigeon AI OpenAPI Architecture

## 1. Purpose

This Phase 1 document defines the planned REST API surface for Pigeon AI. It is a contract-level architecture document, not generated Swagger JSON/YAML and not application source code.

## 2. API Principles

- Base path: `/api/v1`
- Content type: `application/json` for normal APIs; multipart upload endpoints for images, PDF, Excel, and audio.
- Traditional Chinese user-facing messages by default.
- Ring Number appears in URL paths for pigeon-specific operations where practical.
- APIs are tenant/user scoped through authentication and authorization.
- Long-running OCR, import, AI analysis, notification, and report jobs are asynchronous.
- All write APIs return correlation IDs for support traceability.

## 3. Authentication and Authorization

Security schemes planned for Swagger/OpenAPI in Phase 3:

- `bearerAuth`: JWT access token
- `refreshToken`: secure refresh token rotation endpoint
- `adminMfa`: MFA-ready admin routes
- Future service-to-service auth for AI/internal workers

Common roles:

- `BREEDER`
- `LOFT_MANAGER`
- `ADMIN`
- `SUPPORT`
- `KNOWLEDGE_EDITOR`
- `SYSTEM`

## 4. Common API Objects

### 4.1 Error Response

```json
{
  "error": {
    "code": "PIGEON_NOT_FOUND",
    "message": "找不到指定鴿環號碼。",
    "details": {},
    "correlationId": "req_..."
  }
}
```

### 4.2 Pagination

```json
{
  "data": [],
  "page": 1,
  "pageSize": 20,
  "total": 100
}
```

### 4.3 Ring Number Path Pattern

```text
/api/v1/pigeons/{ringNumber}
```

`ringNumber` should preserve display format and route encoding while backend normalization supports search.

## 5. Endpoint Map

### 5.1 Auth

| Method | Path | Description |
| --- | --- | --- |
| `POST` | `/auth/register` | Register breeder account |
| `POST` | `/auth/login` | Password/OTP login |
| `POST` | `/auth/refresh` | Rotate refresh token |
| `POST` | `/auth/logout` | Revoke current session |
| `POST` | `/auth/password/reset-request` | Request password reset |
| `POST` | `/auth/password/reset-confirm` | Confirm reset |
| `GET` | `/auth/me` | Current principal profile and entitlements |

### 5.2 Membership and Subscription

| Method | Path | Description |
| --- | --- | --- |
| `GET` | `/membership/plans` | List available plans |
| `GET` | `/membership/current` | Current membership and entitlements |
| `POST` | `/subscriptions/checkout` | Create provider checkout/session |
| `POST` | `/subscriptions/webhook/{provider}` | Provider webhook receiver |
| `GET` | `/subscriptions/history` | Billing/subscription history |

### 5.3 Loft Management

| Method | Path | Description |
| --- | --- | --- |
| `GET` | `/lofts` | List user lofts |
| `POST` | `/lofts` | Create loft |
| `GET` | `/lofts/{loftId}` | Get loft detail |
| `PATCH` | `/lofts/{loftId}` | Update loft |
| `DELETE` | `/lofts/{loftId}` | Soft delete loft |

### 5.4 Pigeon Management

| Method | Path | Description |
| --- | --- | --- |
| `GET` | `/pigeons` | Search/list pigeons by ring number, loft, sex, status |
| `POST` | `/pigeons` | Register pigeon by Ring Number |
| `GET` | `/pigeons/{ringNumber}` | Get pigeon profile |
| `PATCH` | `/pigeons/{ringNumber}` | Update pigeon profile |
| `POST` | `/pigeons/{ringNumber}/photos` | Upload photo |
| `GET` | `/pigeons/{ringNumber}/timeline` | Ring Number-centric timeline |
| `POST` | `/pigeons/{ringNumber}/transfer` | Transfer/co-owner workflow |
| `DELETE` | `/pigeons/{ringNumber}` | Soft delete/archive pigeon |

### 5.5 Pedigree

| Method | Path | Description |
| --- | --- | --- |
| `GET` | `/pigeons/{ringNumber}/pedigree` | Get ancestry graph |
| `PUT` | `/pigeons/{ringNumber}/pedigree/parents` | Set sire/dam |
| `GET` | `/pigeons/{ringNumber}/pedigree/descendants` | Get descendants |
| `POST` | `/pedigree/imports` | Upload PDF/Excel/image for import |
| `GET` | `/pedigree/imports/{importId}` | Import status and validation rows |
| `POST` | `/pedigree/imports/{importId}/confirm` | Confirm validated import |

### 5.6 Breeding

| Method | Path | Description |
| --- | --- | --- |
| `GET` | `/breeding/pairs` | List breeding pairs |
| `POST` | `/breeding/pairs` | Create pair using male/female Ring Numbers |
| `GET` | `/breeding/pairs/{pairId}` | Pair detail |
| `POST` | `/breeding/pairs/{pairId}/eggs` | Add egg record |
| `PATCH` | `/breeding/eggs/{eggId}` | Update hatch result/offspring Ring Number |
| `POST` | `/breeding/recommendations` | Async AI breeding recommendation |

### 5.7 Health

| Method | Path | Description |
| --- | --- | --- |
| `GET` | `/pigeons/{ringNumber}/health-records` | List health records |
| `POST` | `/pigeons/{ringNumber}/health-records` | Create health record |
| `GET` | `/health-records/{recordId}` | Detail |
| `PATCH` | `/health-records/{recordId}` | Update |
| `POST` | `/health-records/{recordId}/attachments` | Upload attachment |
| `POST` | `/pigeons/{ringNumber}/health-analysis` | Async AI health analysis |
| `GET` | `/pigeons/{ringNumber}/vaccinations/due` | Due vaccine reminders |

### 5.8 Race Management

| Method | Path | Description |
| --- | --- | --- |
| `GET` | `/races` | List race events |
| `POST` | `/races` | Create race event |
| `GET` | `/races/{raceId}` | Race detail |
| `POST` | `/races/{raceId}/entries` | Enter pigeon by Ring Number |
| `POST` | `/races/{raceId}/results/import` | Import results file |
| `GET` | `/pigeons/{ringNumber}/race-results` | Pigeon race history |
| `POST` | `/race-analysis/predict` | Async AI race prediction |

### 5.9 Weather Center

| Method | Path | Description |
| --- | --- | --- |
| `GET` | `/weather/current` | Current weather for loft/race location |
| `GET` | `/weather/forecast` | Forecast |
| `GET` | `/races/{raceId}/weather` | Race weather snapshots |
| `POST` | `/weather/alerts` | Create weather alert rule |
| `DELETE` | `/weather/alerts/{alertId}` | Delete alert rule |

### 5.10 Knowledge Base

| Method | Path | Description |
| --- | --- | --- |
| `GET` | `/knowledge/categories` | List categories |
| `GET` | `/knowledge/documents` | Search documents |
| `GET` | `/knowledge/documents/{documentId}` | Document detail |
| `POST` | `/knowledge/search` | Semantic/hybrid knowledge search |
| `POST` | `/admin/knowledge/documents` | Admin upload document |
| `POST` | `/admin/knowledge/documents/{documentId}/publish` | Publish curated content |

### 5.11 AI Assistant

| Method | Path | Description |
| --- | --- | --- |
| `POST` | `/ai/conversations` | Start conversation |
| `GET` | `/ai/conversations` | List conversations |
| `GET` | `/ai/conversations/{conversationId}` | Conversation detail |
| `POST` | `/ai/conversations/{conversationId}/messages` | Send text/image/PDF/Excel reference message |
| `POST` | `/ai/voice/transcriptions` | Upload audio for transcription |
| `POST` | `/ai/vision/analyze` | Analyze pigeon image |
| `POST` | `/ai/ocr` | OCR uploaded image/PDF |
| `GET` | `/ai/jobs/{jobId}` | Async job status/result |
| `POST` | `/ai/realtime/session` | Create ephemeral realtime voice session if enabled |

### 5.12 Notifications

| Method | Path | Description |
| --- | --- | --- |
| `GET` | `/notifications` | List in-app notifications |
| `PATCH` | `/notifications/{notificationId}/read` | Mark read |
| `POST` | `/devices` | Register push token |
| `DELETE` | `/devices/{deviceId}` | Remove push token |
| `GET` | `/notification-preferences` | Get preferences |
| `PATCH` | `/notification-preferences` | Update preferences |

### 5.13 Admin Portal

| Method | Path | Description |
| --- | --- | --- |
| `GET` | `/admin/users` | Search users |
| `GET` | `/admin/users/{userId}` | User detail |
| `PATCH` | `/admin/users/{userId}/status` | Suspend/restore user |
| `GET` | `/admin/races` | Manage race data |
| `GET` | `/admin/analytics/overview` | Platform analytics |
| `GET` | `/admin/system/health` | System health summary |
| `GET` | `/admin/audit-logs` | Audit search |

## 6. Async Job Pattern

Long-running endpoints return:

```json
{
  "jobId": "job_...",
  "status": "queued",
  "pollUrl": "/api/v1/ai/jobs/job_..."
}
```

Job statuses:

- `queued`
- `running`
- `waiting_for_user_confirmation`
- `completed`
- `failed`
- `cancelled`

## 7. Rate Limits and Quotas

- Auth endpoints: IP and device rate limits.
- AI endpoints: membership entitlement and abuse controls.
- Upload endpoints: file size, file type, antivirus/OCR queue throttling.
- Admin endpoints: stricter RBAC and audit logging.

## 8. OpenAPI Acceptance Criteria

- API covers all requested business modules.
- Ring Number is present in pigeon-specific paths and payloads.
- Async AI/import/OCR workflows are represented.
- Authentication, authorization, errors, pagination, uploads, and jobs are documented.
- Swagger generation in Phase 3 must align with this architecture.

## 9. Architecture Notes

- Public APIs expose stable business capabilities, not provider-specific model parameters.
- Ring Number remains the user-facing and API-facing pigeon business identifier.
- AI, OCR, import, notification, and analysis operations should use async job APIs when processing can exceed normal request latency.
- Swagger generation in Phase 3 must produce machine-readable OpenAPI artifacts from implementation decorators/schemas and reconcile drift against this document.
