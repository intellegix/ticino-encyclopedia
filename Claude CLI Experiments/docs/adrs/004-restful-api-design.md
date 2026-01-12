# ADR-004: RESTful API Design Pattern

Date: 2025-10-24

## Status
Accepted

## Context

The ASR Ops Dashboard requires a standardized API design pattern for communication between the React frontend and FastAPI backend. The application serves multiple client types:
- Web browser (primary)
- Mobile devices (future consideration)
- Potential third-party integrations (internal tools)

The API must support:
- CRUD operations on 40+ entities
- Complex queries and filtering
- File uploads (receipts, documents)
- Authentication and authorization
- Real-time-ish data updates (via polling currently)
- Background job status tracking

## Decision

We will use **REST (Representational State Transfer)** as our API design pattern with the following standards:

### API Design Principles

**Resource-Based URLs:**
```
/api/projects/              # Collection
/api/projects/{id}          # Single resource
/api/projects/{id}/dailies  # Nested resource
```

**HTTP Methods:**
- `GET` - Retrieve resource(s)
- `POST` - Create new resource
- `PUT` - Update entire resource
- `PATCH` - Partial update
- `DELETE` - Remove resource

**Status Codes:**
```
200 OK - Successful GET, PUT, PATCH
201 Created - Successful POST
204 No Content - Successful DELETE
400 Bad Request - Invalid input
401 Unauthorized - Missing/invalid auth
403 Forbidden - Insufficient permissions
404 Not Found - Resource doesn't exist
422 Unprocessable Entity - Validation error
429 Too Many Requests - Rate limit exceeded
500 Internal Server Error - Server error
```

**Request/Response Format:**
- Content-Type: `application/json`
- Character encoding: `UTF-8`
- Date format: ISO 8601 (`2025-10-24T10:30:00Z`)

### API Versioning Strategy

**URL-Based Versioning:**
```
/api/v1/projects/
/api/v2/projects/
```

**Version Lifecycle:**
- v1: Current version (no version prefix = v1)
- Future versions: Explicit v2, v3, etc.
- Deprecated versions: Marked with X-API-Deprecated header
- Version support: Maintain N and N-1 versions

**Migration Path:**
```python
# Current (implicit v1)
@app.get("/api/projects/")

# When v2 needed:
@app.get("/api/v1/projects/")  # Explicitly mark v1
@app.get("/api/v2/projects/")  # New version
@app.get("/api/projects/")      # Redirect to latest

# Version selection:
# - Default: /api/projects/ → latest stable
# - Explicit: /api/v1/projects/ → specific version
# - Header: Accept: application/vnd.asr.v2+json (future)
```

### Pagination Strategy

**Query Parameters:**
```
GET /api/projects?skip=0&limit=100
```

**Response Format:**
```json
{
  "items": [...],
  "total": 523,
  "skip": 0,
  "limit": 100,
  "has_more": true
}
```

**Headers:**
```
X-Total-Count: 523
Link: </api/projects?skip=100&limit=100>; rel="next"
```

### Filtering and Sorting

**Filter Syntax:**
```
GET /api/projects?status=ACTIVE
GET /api/projects?start_date_gte=2025-01-01
GET /api/projects?search=foundation
```

**Sort Syntax:**
```
GET /api/projects?sort=name
GET /api/projects?sort=-created_at  # Descending
GET /api/projects?sort=status,name  # Multiple fields
```

### Error Response Format

**Standardized Error Response:**
```json
{
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Invalid project data",
    "details": [
      {
        "field": "start_date",
        "issue": "Date cannot be in the past"
      }
    ],
    "request_id": "abc-123-def"
  }
}
```

### Authentication & Authorization

**Bearer Token Authentication:**
```
Authorization: Bearer <jwt_token>
```

**Token Types:**
- Access Token: 30 minutes (short-lived)
- Refresh Token: 7 days (stored securely)

**Auth Endpoints:**
```
POST /api/auth/login
POST /api/auth/refresh
POST /api/auth/logout
GET  /api/auth/me
```

### File Upload Endpoints

**Multipart Form Data:**
```
POST /api/receipts/upload
Content-Type: multipart/form-data

{
  file: <binary data>
  metadata: { user_id, project_id }
}
```

**Response:**
```json
{
  "file_id": 123,
  "file_name": "receipt_2025-10-24.pdf",
  "file_url": "/api/files/123/download",
  "uploaded_at": "2025-10-24T10:30:00Z"
}
```

### Background Job Endpoints

**Job Submission:**
```
POST /api/wc-processing/jobs
{
  "asr_file": <file>,
  "armorpro_file": <file>
}

Response:
{
  "job_id": "uuid-123",
  "status": "pending",
  "status_url": "/api/wc-processing/jobs/uuid-123/status"
}
```

**Job Status Polling:**
```
GET /api/wc-processing/jobs/{job_id}/status

Response:
{
  "job_id": "uuid-123",
  "status": "processing",
  "progress": 45,
  "message": "Generating ASR report...",
  "current_step": 3,
  "total_steps": 6
}
```

### Health Check Endpoint

```
GET /api/health

Response:
{
  "status": "healthy",
  "version": "2.0.0",
  "timestamp": "2025-10-24T10:30:00Z",
  "services": {
    "database": "connected",
    "raken_api": "connected",
    "scheduler": "running"
  }
}
```

### OpenAPI Documentation

**Automatic Documentation Generation:**
- FastAPI generates OpenAPI 3.0 spec automatically
- Accessible at `/docs` (Swagger UI)
- Alternative at `/redoc` (ReDoc UI)
- JSON spec at `/openapi.json`

**Documentation Standards:**
```python
@app.get(
    "/api/projects/{project_id}",
    response_model=schemas.Project,
    summary="Get single project",
    description="Retrieve detailed information for a specific project by ID",
    responses={
        200: {"description": "Project found"},
        404: {"description": "Project not found"},
        401: {"description": "Unauthorized"}
    },
    tags=["Projects"]
)
async def get_project(
    project_id: int = Path(..., description="The project ID"),
    current_user: int = Depends(get_current_user_id),
    db: Session = Depends(get_db)
):
    ...
```

### CORS Configuration

**Allowed Origins:**
```python
# Development
origins = ["http://localhost:3000", "http://localhost:3003"]

# Production
origins = os.getenv("ALLOWED_ORIGINS").split(",")
```

**Allowed Methods:**
```
GET, POST, PUT, PATCH, DELETE, OPTIONS
```

**Allowed Headers:**
```
Authorization, Content-Type, Accept, X-Requested-With
```

### Rate Limiting

**Tiers:**
```
Login endpoints: 5 requests / minute
Read endpoints: 100 requests / minute
Write endpoints: 30 requests / minute
Admin endpoints: 10 requests / minute
```

**Headers:**
```
X-RateLimit-Limit: 100
X-RateLimit-Remaining: 73
X-RateLimit-Reset: 1635234567
```

### Caching Headers

**Cache-Control:**
```
GET /api/projects/ → Cache-Control: private, max-age=300
GET /api/static/   → Cache-Control: public, max-age=86400
POST /api/         → Cache-Control: no-cache
```

**ETag Support (Future):**
```
GET /api/projects/123
Response:
  ETag: "33a64df551425fcc55e4d42a148795d9f25f89d4"

Subsequent request:
  If-None-Match: "33a64df551425fcc55e4d42a148795d9f25f89d4"
Response:
  304 Not Modified
```

## Consequences

### Positive Consequences

**Standardization:**
- Well-understood pattern across industry
- Easy for new developers to learn
- Extensive tooling support
- Clear HTTP semantics

**Caching:**
- HTTP caching works out of the box
- CDN support for static endpoints
- Browser caching reduces bandwidth

**Simplicity:**
- Simple to implement with FastAPI
- No complex query language to learn
- Straightforward testing
- Easy to debug with browser dev tools

**Documentation:**
- FastAPI auto-generates OpenAPI spec
- Interactive API docs with Swagger UI
- Easy for frontend developers to consume

**Tooling:**
- Postman, Insomnia support
- OpenAPI code generation
- API testing frameworks
- Monitoring tools (Datadog, New Relic)

### Negative Consequences

**Over-fetching:**
- Fixed response shapes may include unnecessary data
- Multiple requests needed for related data
- No field selection (unlike GraphQL)

**Under-fetching:**
- May need multiple requests for complete data
- N+1 query problem in some cases
- Increased network roundtrips

**Versioning Complexity:**
- Need to maintain multiple API versions
- Version migration can be challenging
- Deprecation requires client updates

**Limited Real-Time:**
- Polling required for updates (no native push)
- Websockets needed for true real-time (separate concern)

### Risks and Mitigation

**Risk: Over-fetching causes performance issues**
- **Mitigation:** Implement field selection query param (sparse fieldsets)
- **Mitigation:** Create specialized endpoints for common use cases
- **Mitigation:** Use GZIP compression (already implemented)

**Risk: API versioning becomes unwieldy**
- **Mitigation:** Keep changes backward compatible when possible
- **Mitigation:** Version only when breaking changes required
- **Mitigation:** Maintain clear deprecation timeline (6-12 months)

**Risk: Endpoint explosion (too many endpoints)**
- **Mitigation:** Use query parameters for filtering/sorting
- **Mitigation:** Consolidate related operations
- **Mitigation:** Follow resource-oriented design

## Alternatives Considered

### Alternative 1: GraphQL

**Pros:**
- Client specifies exact data needed (no over/under-fetching)
- Single endpoint for all queries
- Strong typing with schema
- Real-time with subscriptions
- Better for complex data relationships

**Cons:**
- More complex to implement
- Requires GraphQL knowledge for frontend team
- Caching more complex (no HTTP caching)
- Query complexity can impact performance
- Requires additional tooling (Apollo, Relay)
- Harder to debug without specialized tools

**Why not chosen:**
- Overkill for current use cases
- Team not familiar with GraphQL
- REST pattern adequate for current data relationships
- HTTP caching benefits important
- Simpler debugging and monitoring with REST

### Alternative 2: gRPC

**Pros:**
- Binary protocol (faster than JSON)
- Bi-directional streaming
- Strong typing with Protocol Buffers
- Better performance for microservices

**Cons:**
- Not browser-compatible (requires gRPC-Web)
- Harder to debug (binary format)
- Limited tooling compared to REST
- Requires code generation
- Overkill for monolithic architecture

**Why not chosen:**
- Browser compatibility issues
- Unnecessary complexity for monolith
- Team not familiar with Protocol Buffers
- REST performance adequate

### Alternative 3: JSON-RPC or XML-RPC

**Pros:**
- Simple procedure-call semantics
- Single endpoint

**Cons:**
- Less standardized than REST
- Poor HTTP caching support
- Doesn't leverage HTTP verbs
- Less tooling support

**Why not chosen:**
- REST is more standardized
- Better caching with REST
- More tooling for REST
- Industry preference for REST

## Implementation Checklist

**Completed:**
- [x] Resource-based URL structure
- [x] Standard HTTP methods
- [x] JSON request/response format
- [x] JWT authentication
- [x] Role-based authorization
- [x] Pagination (skip/limit)
- [x] Error handling
- [x] Rate limiting
- [x] CORS configuration
- [x] FastAPI automatic docs

**TODO:**
- [ ] Explicit API versioning (v1 prefix)
- [ ] Formal OpenAPI 3.0 spec file
- [ ] Standardized error response format across all endpoints
- [ ] Field selection/sparse fieldsets
- [ ] ETag support for caching
- [ ] Link headers for pagination
- [ ] Request ID tracking for debugging
- [ ] API usage metrics and monitoring
- [ ] Client SDK generation from OpenAPI spec

## Related Decisions

- ADR-002: Monolithic Architecture (establishes REST as appropriate pattern)
- ADR-003: Dual Data Model Strategy (affects API endpoint design)
- Future ADR: Websocket Integration (for real-time features)

## References

- [REST API Best Practices](https://restfulapi.net/)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [OpenAPI Specification](https://swagger.io/specification/)
- [HTTP Status Codes](https://httpstatuses.com/)

---

**Next Review Date:** 2026-04-24 (6 months)
**Owner:** Backend Team
**Stakeholders:** Frontend Team, API Consumers
