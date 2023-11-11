from typing import TypeAlias

from app.core import get_app_settings

from .providers import FileProvider, SlackProvider

TA: TypeAlias = FileProvider | SlackProvider


class Log:
    providers = {'file': FileProvider, 'slack': SlackProvider}

    @classmethod
    def default(cls) -> TA:
        return cls.providers[get_app_settings().LOG_CHANNEL]()  # type: ignore

    @classmethod
    def channel(cls, driver: str) -> TA:
        return cls.providers[driver]()  # type: ignore


if __name__ == '__main__':
    Log.default().debug('called')
    Log.channel('file').info('called')
    Log.channel('slack').info('called')
