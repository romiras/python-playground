from typing import Dict, Any

from credits_repository import CreditsRepository


config: Dict[str, Any] = {
    "initial_credits": 5,
    "replenish_credits": 1,
    "charge_credits": 1,
    "max_credits": 5
}
db = None # TODO: replace with actual db connection
credits_repository: CreditsRepository = CreditsRepository(db, config)

client_id = 'mock-client-id'
for i in range(10):
    allowed = credits_repository.charge(client_id=client_id)
    print(f"i: {i}, allowed: {allowed}")

# @app.middleware("http")
# async def rate_limit_middleware(request: Request, call_next):
#     """Apply rate limiting very early in the request lifecycle."""

#     # Skip rate limiting for health checks, etc.
#     if request.url.path in ["/health", "/metrics"]:
#         return await call_next(request)

#     # Apply rate limiting
#     rate_limiter = RateLimiter()  # Or get from app.state
#     try:
#         rate_limiter.enforce_limit(api_token)
#     except HTTPException as e:
#         # Early return before hitting route handler
#         return JSONResponse(
#             status_code=e.status_code,
#             content={"error": e.detail},
#             headers=dict(e.headers or {})
#         )

#     # Generate request ID for logging
#     request_id = f"req_{int(time.time()*1000)}_{hash(api_token) % 10000}"
#     request.state.request_id = request_id

#     response = await call_next(request)

#     # Add request ID to all responses for tracing
#     response.headers["X-Request-ID"] = request_id
#     return response
