from io import BytesIO
import os
from pathlib import Path
import shutil
from typing import List, Type


class FileUtil:

    @staticmethod
    def convert_content_type(
        content: str | bytes,
        to_type: Type[str | bytes | BytesIO]) -> str | bytes | BytesIO:
        to = f'{to_type.__module__}.{to_type.__name__}'
        match to:
            case 'builtins.str':
                if isinstance(content, bytes):
                    return content.decode('utf-8', errors='ignore')
                return content
            case 'builtins.bytes':
                if isinstance(content, str):
                    return content.encode('utf-8')
                return content
            case '_io.BytesIO':
                if isinstance(content, str):
                    return BytesIO(content.encode('utf-8'))
                return BytesIO(content)
            case _:
                raise TypeError('Unsupported target type')

    @staticmethod
    def read(filepath: str) -> str | None:
        with open(filepath, 'r') as f:
            result = f.read()
        return result

    @classmethod
    def write(cls, filepath: str, content: str | bytes) -> None:
        mode = 'w' if isinstance(content, str) else 'wb'
        if not cls.exists(filepath):
            mode = 'w+' if isinstance(content, str) else 'wb+'
        with open(filepath, mode=mode) as f:
            f.write(content)

    @classmethod
    def exists(cls, filepath: str) -> bool:
        return Path(filepath).exists()

    @classmethod
    def make_dirs(cls, filepath: str) -> None:
        if cls.exists(filepath):
            return

        Path(filepath).mkdir(parents=True)

    @classmethod
    def remove_file(cls, filepath: str) -> None:
        if os.path.isfile(filepath):
            os.remove(filepath)

    @classmethod
    def remove_dir(cls, dir_path: str) -> None:
        if os.path.isdir(dir_path):
            shutil.rmtree(dir_path)

    @staticmethod
    def get_all_files(src_dir: str,
                      depth: int = 0,
                      exclude_files: List[str] = [],
                      exclude_dirs: List[str] = []) -> List[str]:
        """Get list of all files in a directory and it's subdirectories

        Args:
            src_dir: directory to scan
            depth: depth of directories
                0 - same
                1 - all
            exclude_files: files to exclude
            exclude_dirs: directories to exclude
        Returns:
            list: ['/path/to/file.py', '/path/to/folder/file.py']
        """

        exclude_files.extend(['__init__.py', 'README'])
        exclude_dirs.extend(['__pycache__'])

        skip_dirs = set(exclude_dirs)
        skip_files = set(exclude_files)

        result = []

        if depth < 0:
            for root, subs, filenames in os.walk(src_dir,
                                                 topdown=True,
                                                 followlinks=False):
                subs[:] = list(set(subs) - skip_dirs)
                filenames[:] = list(set(filenames) - skip_files)
                for f in filenames:
                    result.append(os.path.join(root, f))

        else:
            base_depth = src_dir.rstrip(os.path.sep).count(os.path.sep)

            for root, subs, filenames in os.walk(src_dir,
                                                 topdown=True,
                                                 followlinks=False):
                subs[:] = list(set(subs) - skip_dirs)
                cur_depth = root.count(os.path.sep)

                if base_depth + depth <= cur_depth:
                    del subs[:]

                filenames[:] = list(set(filenames) - skip_files)
                for f in filenames:
                    result.append(os.path.join(root, f))

        return result
