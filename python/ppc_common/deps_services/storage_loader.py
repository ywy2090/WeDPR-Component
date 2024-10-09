from ppc_common.deps_services.storage_api import StorageType
from ppc_common.deps_services.hdfs_storage import HdfsStorage
from ppc_common.deps_services.local_storage import LocalStorage
from ppc_common.ppc_utils import common_func


def load(config: dict, logger):
    storage_type = config['STORAGE_TYPE']
    if storage_type == StorageType.HDFS.value:
        hdfs_user = common_func.get_config_value(
            'HDFS_USER', None, config, False)
        hdfs_home = common_func.get_config_value(
            "HDFS_HOME", None, config, False)
        hdfs_url = config['HDFS_URL']
        return HdfsStorage(hdfs_url, hdfs_user, hdfs_home)
    elif storage_type == StorageType.LOCAL.value:
        local_home = common_func.get_config_value(
            "LOCAL_HOME", None, config, False)
        return LocalStorage(local_home)
    else:
        raise Exception('unsupported storage type')
