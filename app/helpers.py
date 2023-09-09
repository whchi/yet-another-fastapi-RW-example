import os
from typing import Any, List


def base_path(*args: str) -> str:
    """Get base path of projectroot
    Returns:
        str: /path/to/projectroot
    """
    return os.path.join(os.path.dirname(os.path.dirname(__file__)), *args)


def app_path(*args: str) -> str:
    """Get base path of app
    Returns:
        str: /path/to/projectroot/app
    """
    # return os.path.join(os.path.dirname(os.path.dirname(__file__)), *args)
    return os.path.join(base_path(), 'app', *args)


def storage_path(*args: str) -> str:
    """Get base path of storage
    Returns:
        str: /path/to/projectroot/storage
    """

    return os.path.join(base_path(), 'storage', *args)


def is_blank(ipt: str | List[Any] | None) -> bool:
    """Check if input is blank
    Returns:
        bool: False if input is not blank
    """
    if ipt is None:
        return True
    if isinstance(ipt, str):
        return not ipt.strip()
    if isinstance(ipt, list):
        return not ipt
    return False
