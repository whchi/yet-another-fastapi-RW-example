import logging

from app.helpers import storage_path

from .provider_contract import ProviderContract


class FileProvider(ProviderContract):

    def __init__(self) -> None:
        self.logger = logging.getLogger('file-logger')
        self.logger.setLevel(super().app_config.log_level)

        path = storage_path('logs')

        fmt = '%(asctime)s %(levelname)-8s [%(pathname)s:%(lineno)d@%(funcName)s] %(message)s' if \
            super().app_config.APP_DEBUG else '%(asctime)s %(levelname)-8s %(message)s'

        handler = logging.FileHandler(f'{path}/app.log')
        handler.setFormatter(logging.Formatter(fmt))

        self.logger.addHandler(handler)
