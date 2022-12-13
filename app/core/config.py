from functools import lru_cache

from app.core.settings import AppSettings, DBSettings


@lru_cache
def get_app_settings() -> AppSettings:
    return AppSettings()


@lru_cache
def get_db_settings() -> DBSettings:
    return DBSettings()
