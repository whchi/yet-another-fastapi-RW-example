import os

from app.core.filesystem.contracts.file_system_manager import (
    FileSystemManager,
)
from app.core.filesystem.file_util import FileUtil
from app.helpers import storage_path


class LocalProvider(FileSystemManager):

    def __init__(self) -> None:
        self.root = storage_path('app')

    @classmethod
    def register(cls) -> 'LocalProvider':
        return cls()

    def read(self, filepath: str) -> str | None:
        return FileUtil.read(f'{self.root}{self._prepend_slash(filepath)}')

    def write(self, filepath: str, content: str | bytes, **kwargs: str | None) -> None:
        dir_path = os.path.sep.join(filepath.split(os.path.sep)[0:-1])
        FileUtil.make_dirs(self.root + self._prepend_slash(dir_path))
        if isinstance(content, str):
            content = content.encode('utf-8')
        FileUtil.write(
            f'{self.root}{self._prepend_slash(filepath)}',
            content,
        )

    def exists(self, filepath: str) -> bool:
        return FileUtil.exists(f'{self.root}{self._prepend_slash(filepath)}')

    def url(self, filename: str) -> str:
        return ''

    def make_dirs(self, filepath: str) -> None:
        FileUtil.make_dirs(f'{self.root}{self._prepend_slash(filepath)}')

    def remove_file(self, filepath: str) -> None:
        FileUtil.remove_file(filepath)

    def remove_dir(self, dir_path: str) -> None:
        FileUtil.remove_dir(dir_path)

    def _prepend_slash(self, filepath: str) -> str:
        if not filepath:
            return ''

        return filepath if filepath[0] == os.path.sep else f'{os.path.sep}{filepath}'
