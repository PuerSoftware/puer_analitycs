from pydantic          import PostgresDsn
from pydantic_settings import BaseSettings
from dotenv            import load_dotenv

from src.constants     import Environment


class Config(BaseSettings):
	DEBUG: bool = False

	DATABASE_URL: PostgresDsn

	ENVIRONMENT: Environment = Environment.PRODUCTION


	FP_TABLE     : str = 't_fingerprint'
	ACTION_TABLE : str = 't_action'
	LOG_TABLE    : str = 't_log'

	CORS_ORIGINS       : list[str]
	CORS_ORIGINS_REGEX : str | None = None
	CORS_HEADERS       : list[str]

	APP_VERSION: str = '1'

load_dotenv()
settings = Config()

app_configs = {
	'title': 'Analytics app API',
	'debug': settings.DEBUG,
}

if settings.ENVIRONMENT.is_deployed:
    app_configs['root_path'] = f'/v{settings.APP_VERSION}'

if not settings.ENVIRONMENT.is_debug:
    app_configs['openapi_url'] = None  # hide docs
