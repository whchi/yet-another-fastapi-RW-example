from app.core import get_app_settings
from app.core.filesystem.providers import LocalProvider
from app.helpers import storage_path


class PublicProvider(LocalProvider):

    def __init__(self) -> None:
        self.root = storage_path('app/public')

    def url(self, filename: str) -> str:
        return f'{get_app_settings().APP_URL}/public/{filename}'
