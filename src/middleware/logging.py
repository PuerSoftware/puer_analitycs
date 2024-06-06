from fastapi.requests          import Request
from fastapi.responses         import JSONResponse
from loguru                    import logger
from starlette.middleware.base import BaseHTTPMiddleware


class LoggingMiddleware(BaseHTTPMiddleware):
	async def dispatch(self, request: Request, call_next):
		try:
			response = await call_next(request)
		except Exception as e:
			logger.error(f'Exception occurred: {e}')
			return JSONResponse(
				status_code=500,
				content={'message': 'Internal Server Error'},
			)
		return response
