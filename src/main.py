from fastapi                   import FastAPI
from starlette.middleware.cors import CORSMiddleware


from src.config          import app_configs, settings
from src.tracking.router import router as tracking_router

app = FastAPI(**app_configs)

app.add_middleware(
    CORSMiddleware,
    allow_origins      = settings.CORS_ORIGINS,
    allow_origin_regex = settings.CORS_ORIGINS_REGEX,
    allow_credentials  = True,
    allow_methods      = ('GET', 'POST', 'PUT', 'PATCH', 'DELETE', 'OPTIONS'),
    allow_headers      = settings.CORS_HEADERS,
)

@app.get("/healthcheck", include_in_schema=False)
async def healthcheck() -> dict[str, str]:
    return {"status": "ok"}

app.include_router(tracking_router, prefix='tracking', tags=['Tracking'])