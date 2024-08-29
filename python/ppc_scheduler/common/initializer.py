import logging
import logging.config
import os
from contextlib import contextmanager

import yaml
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from ppc_common.deps_services import storage_loader
from ppc_common.ppc_async_executor.thread_event_manager import ThreadEventManager
from ppc_common.ppc_initialize.dataset_handler_initialize import DataSetHandlerInitialize
from ppc_common.ppc_utils import common_func
from ppc_scheduler.job.job_manager import JobManager


class Initializer:
    def __init__(self, log_config_path, config_path):
        self.job_cache_dir = None
        self.log_config_path = log_config_path
        self.config_path = config_path
        self.config_data = None
        self.job_manager = None
        self.thread_event_manager = None
        self.sql_session = None
        self.sql_engine = None
        self.storage_client = None
        # 只用于测试
        self.mock_logger = None
        self.dataset_handler_initializer = None

    def init_all(self):
        self.init_log()
        self.init_cache()
        self.init_config()
        self.init_job_manager()
        self.init_sql_client()
        self.init_storage_client()
        self.init_others()

    def init_log(self):
        logging.config.fileConfig(self.log_config_path)

    def init_cache(self):
        self.job_cache_dir = common_func.get_config_value(
            "JOB_TEMP_DIR", "/tmp", self.config_data, False)
        if not os.path.exists(self.job_cache_dir):
            os.makedirs(self.job_cache_dir)

    def init_config(self):
        with open(self.config_path, 'rb') as f:
            self.config_data = yaml.safe_load(f.read())

    def init_job_manager(self):
        self.thread_event_manager = ThreadEventManager()
        self.job_manager = JobManager(
            logger=self.logger(),
            thread_event_manager=self.thread_event_manager,
            workspace=self.config_data['WORKSPACE'],
            job_timeout_h=self.config_data['JOB_TIMEOUT_H']
        )

    def init_sql_client(self):
        self.sql_engine = create_engine(self.config_data['SQLALCHEMY_DATABASE_URI'], pool_pre_ping=True)
        self.sql_session = sessionmaker(bind=self.sql_engine)

    @contextmanager
    def create_sql_session(self):
        session = self.sql_session()
        try:
            yield session
            session.commit()
        except:
            session.rollback()
            raise
        finally:
            session.close()

    def init_storage_client(self):
        self.storage_client = storage_loader.load(
            self.config_data, self.logger())

    def init_others(self):
        self.dataset_handler_initializer = DataSetHandlerInitialize(
            self.config_data, self.logger())

    def logger(self, name=None):
        if self.mock_logger is None:
            return logging.getLogger(name)
        else:
            return self.mock_logger
