from typing import TypeAlias

from app.core import get_app_settings

from .providers import LocalProvider, PublicProvider, S3Provider

TA: TypeAlias = LocalProvider | S3Provider | PublicProvider


class Storage:
    providers = {'local': LocalProvider, 's3': S3Provider, 'public': PublicProvider}

    @classmethod
    def default(cls) -> TA:
        return cls.providers[
            get_app_settings().FILESYSTEM_DISK].register()  # type: ignore

    @classmethod
    def disk(cls, driver: str = 'local') -> TA:
        return cls.providers[driver].register()  # type: ignore


if __name__ == '__main__':
    Storage.default().write('default-file-test', 'default content')
    print(Storage.default().read('default-file-test'))
    Storage.default().remove_file('default-file-test')
    Storage.disk('local').write('file-test', 'content')
    print(Storage.disk('local').read('file-test'))
    Storage.disk('local').remove_file('file-test')
    Storage.disk('s3').write('file-test', 'aws-content')
    print(Storage.disk('s3').read('file-test'))
    Storage.disk('s3').remove_file('file-test')
