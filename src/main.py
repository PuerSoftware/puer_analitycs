from fastapi                   import FastAPI
from fastapi.responses         import JSONResponse
from fastapi.requests          import Request
from loguru                    import logger
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

@app.get('/healthcheck', include_in_schema=False)
async def healthcheck() -> dict[str, str]:
    return {'status': 'ok'}


@app.middleware('http')
async def log_exceptions(request: Request, call_next):
    try:
        response = await call_next(request)
    except Exception as e:
        logger.error(f'Exception occurred: {e}')
        return JSONResponse(
            status_code=500,
            content={'message': 'Internal Server Error'},
        )
    return response


app.include_router(tracking_router, prefix='/tracking', tags=['Tracking'])