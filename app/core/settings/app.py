import logging
import sys
from typing import Any, Dict, Tuple

from loguru import logger

from app.core.logging import InterceptHandler

from .base import BaseAppSettings


class AppSettings(BaseAppSettings):
    APP_NAME: str
    APP_ENV: str
    APP_URL: str
    APP_DEBUG: bool = True
    LOG_LEVEL: str = 'debug'
    DOCS_URL: str = '/docs'
    OPENAPI_URL: str = '/openapi.json'
    REDOC_URL: str = '/redoc'
    LOGGERS: Tuple[str, str] = ('uvicorn.asgi', 'uvicorn.access')
    SLACK_WEBHOOK_URL: str | None = None
    LOG_CHANNEL: str = 'file'
    AWS_ACCESS_KEY_ID: str | None = None
    AWS_SECRET_ACCESS_KEY: str | None = None
    AWS_S3_BUCKET: str | None = None
    AWS_S3_REGION: str | None = None

    _enable_debug: bool = True
    _log_level_map: Dict[str, int] = {
        'critical': logging.CRITICAL,
        'fatal': logging.FATAL,
        'error': logging.ERROR,
        'warn': logging.WARNING,
        'warning': logging.WARNING,
        'info': logging.INFO,
        'debug': logging.DEBUG,
        'notset': logging.NOTSET
    }

    @property
    def fastapi_kwargs(self) -> Dict[str, Any]:
        return {
            'debug':
                self._enable_debug,
            'docs_url':
                None if self.APP_ENV != 'local' else '/docs',
            'openapi_prefix':
                '',
            'openapi_url':
                None if self.APP_ENV != 'local' else '/openapi.json',
            'redoc_url':
                None if self.APP_ENV != 'local' else '/redoc',
            'openapi_tags':
                None if self.APP_ENV != 'local' else [{
                    'name': 'monitor',
                    'description': 'uptime monitor endpoints'
                }]
        }

    @property
    def log_level(self) -> int:
        try:
            return self._log_level_map[self.LOG_LEVEL]
        except KeyError:
            return self._log_level_map['debug']

    def configure_logging(self) -> None:
        log_level = self._log_level_map[self.LOG_LEVEL]
        logging.getLogger().handlers = [InterceptHandler()]

        for logger_name in self.LOGGERS:
            logging_logger = logging.getLogger(logger_name)
            logging_logger.handlers = [InterceptHandler(level=log_level)]

        logger.configure(handlers=[{'sink': sys.stderr, 'level': log_level}])
