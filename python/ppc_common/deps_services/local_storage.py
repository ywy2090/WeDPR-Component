import os
import shutil
from typing import AnyStr

from ppc_common.deps_services.storage_api import StorageApi, StorageType

class LocalStorage(StorageApi):
    
    def __init__(self, home_path: str = None):
        self.home_path = home_path
    
    def download_file(self, storage_path: str, local_file_path: str, enable_cache=False):
        shutil.copy(storage_path, local_file_path)

    def upload_file(self, local_file_path: str, storage_path: str):
        shutil.copy(local_file_path, storage_path)

    def make_file_path(self, storage_path: str):
        os.makedirs(os.path.dirname(storage_path), exist_ok=True)

    def delete_file(self, storage_path: str):
        if os.path.exists(storage_path):
            os.remove(storage_path)

    def save_data(self, data: AnyStr, storage_path: str):
        with open(storage_path, 'wb') as f:
            f.write(data)

    def get_data(self, storage_path: str) -> AnyStr:
        with open(storage_path, 'rb') as f:
            return f.read()

    def mkdir(self, storage_path: str):
        os.makedirs(storage_path, exist_ok=True)

    def file_existed(self, storage_path: str) -> bool:
        return os.path.exists(storage_path)

    def file_rename(self, old_storage_path: str, storage_path: str):
        shutil.move(old_storage_path, storage_path)

    def storage_type(self):
        return StorageType.LOCAL

    def get_home_path(self):
        return os.path.expanduser("~")