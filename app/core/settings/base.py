from pydantic import BaseSettings


class BaseAppSettings(BaseSettings):

    class Config:
        env_file = '.env'
