import abc
from typing import Any

from app.core import get_app_settings


class FileSystemManager(abc.ABC):
    _instance: Any = None
    storage_config = get_app_settings()

    def __new__(cls, *args: Any) -> 'FileSystemManager':
        if not cls._instance:
            cls._instance = super(FileSystemManager, cls).__new__(cls)
        return cls._instance

    @classmethod
    @abc.abstractmethod
    def register(cls) -> 'FileSystemManager':
        raise NotImplementedError

    @abc.abstractmethod
    def read(self, filepath: str) -> Any:
        raise NotImplementedError

    @abc.abstractmethod
    def write(self, filepath: str, content: Any, **kwargs: str | None) -> None:
        raise NotImplementedError

    @abc.abstractmethod
    def exists(self, filepath: str) -> bool:
        raise NotImplementedError

    @abc.abstractmethod
    def url(self, filename: str) -> str:
        raise NotImplementedError

    @abc.abstractmethod
    def make_dirs(self, filepath: str) -> None:
        raise NotImplementedError

    @abc.abstractmethod
    def remove_file(self, filepath: str) -> None:
        raise NotImplementedError

    @abc.abstractmethod
    def remove_dir(self, dir_path: str) -> None:
        raise NotImplementedError
