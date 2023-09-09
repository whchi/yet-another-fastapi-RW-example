from typing import Any

from app.core import get_app_settings


class ProviderContract:
    _instance: Any = None
    app_config = get_app_settings()

    def __new__(cls, *args: Any) -> 'ProviderContract':
        if not cls._instance:
            cls._instance = super(ProviderContract, cls).__new__(cls)
        return cls._instance

    def debug(self, msg: str, *args: Any, **kwargs: Any) -> None:
        self._instance.logger.debug(msg, *args, **kwargs)

    def info(self, msg: str, *args: Any, **kwargs: Any) -> None:
        self._instance.logger.info(msg, *args, **kwargs)

    def warn(self, msg: str, *args: Any, **kwargs: Any) -> None:
        self._instance.logger.warn(msg, *args, **kwargs)

    def error(self, msg: str, *args: Any, **kwargs: Any) -> None:
        self._instance.logger.error(msg, *args, **kwargs)
