import logging
import logging.config
import os
from contextlib import contextmanager

import yaml
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from ppc_common.deps_services import storage_loader
from ppc_common.ppc_config.file_chunk_config import FileChunkConfig
from ppc_common.ppc_utils import common_func

class Initializer:
    def __init__(self):
        self.config_data = None
        self.config_data = None
        self.sql_session = None
        self.sql_engine = None
        self.file_chunk = None
        self.storage_client = None

    def init_all(self, config_data):
        self.config_data = config_data
        
        # self.init_log()
        # self.init_config()
        # self.init_cache()
        self.init_sql_client()
        self.init_storage_client()
        self.init_file_chunk_config()
    
    @staticmethod    
    def init_config(config_path: str):
        with open(config_path, 'rb') as f:
            config_data = yaml.safe_load(f.read())
            return config_data
        
    @staticmethod
    def init_log(log_config_path: str):
        logging.config.fileConfig(log_config_path)

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
    
    def init_file_chunk_config(self):
        self.file_chunk = FileChunkConfig(self.config_data)

    def update_thread_event_manager(self, thread_event_manager):
        self.thread_event_manager = thread_event_manager

    @staticmethod
    def logger(name=None):
        return logging.getLogger(name)
