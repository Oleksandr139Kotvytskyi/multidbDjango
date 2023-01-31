import abc
import logging

import threading
import time
from contextlib import contextmanager  # pylint:disable = wrong-import-order

from db.src.utils.constants import (
    CONNECTION,
    LAST_UPDATE,
    CREATE_TIME,
    DB_CONNECTION_USER,
    DB_CONNECTION_PASS,
    DB_CONNECTION_HOST,
    DB_CONNECTION_DATABASE,
    DB_CONNECTION_PORT,
)
from db.src.utils.exceptions import DBManagerError
from db.src.utils.utils import get_config


logger = logging.getLogger('root')

class DbBaseInterface(abc.ABC):
    """
    Class for managing connections to the DB.
    """

    def __init__(self, cnf_file_name):
        self._connection_counter = 0
        self._pool = []
        self._lock = threading.RLock()
        self._config = self._get_manager_config(cnf_file_name)
        self._connection_settings = {
            DB_CONNECTION_USER: self._config['client']['user'],
            DB_CONNECTION_PASS: self._config['client']['password'],
            DB_CONNECTION_HOST: self._config['client']['host'],
            DB_CONNECTION_DATABASE: self._config['client']['database'],
            DB_CONNECTION_PORT: self._config['client']['port'],
        }
        self._lifetime = self._config['client']['lifetime']
        self._delay = self._config['client']['delay']
        self._poolsize = self._config['client']['poolsize']
        logger.info(f"DB manager {self.get_manager_name()} created with {self._config}")

    def __del__(self):
        '''Method for deleting connection from memory.'''
        for connect in self._pool:
            self._close_connection(connect)

    @staticmethod
    def _get_manager_config(cnf_file):
        return get_config(cnf_file)

    @abc.abstractmethod
    def check_connection(self):
        raise NotImplementedError("_create_connection is not implemented!")

    @staticmethod
    @abc.abstractmethod
    def get_manager_name():
        raise NotImplementedError("_create_connection is not implemented!")

    @abc.abstractmethod
    def _make_connection(self):
        raise NotImplementedError("_create_connection is not implemented!")

    @abc.abstractmethod
    def _close_db_connection(self, connection):
        raise NotImplementedError("_close_db_connection is not implemented!")

    @abc.abstractmethod
    def _commit_db_connection(self, connection):
        raise NotImplementedError("_commit_db_connection is not implemented!")

    @abc.abstractmethod
    def _roolback_db_connection(self, connection):
        raise NotImplementedError("_roolback_db_connection is not implemented!")

    @abc.abstractmethod
    def _get_connection_cursor(self, connection):
        raise NotImplementedError("_get_connection_cursor is not implemented!")

    def _create_connection(self):
        connection = self._make_connection()
        self._connection_counter += 1
        return {CONNECTION: connection,
                LAST_UPDATE: 0,
                CREATE_TIME: time.time()}

    def _get_connection(self):
        connect = None
        while not connect:
            if self._pool:
                connect = self._pool.pop()
            elif self._connection_counter < self._poolsize:
                connect = self._create_connection()
            time.sleep(self._delay)
        return connect

    def _close_connection(self, connection):
        self._close_db_connection(connection[CONNECTION])
        self._connection_counter -= 1

    def _return_connection(self, connection):
        connection[LAST_UPDATE] = time.time()
        self._pool.append(connection)

    @contextmanager
    def get_connect(self):
        """
        Context manager for getting connection.
        :yield connect: connect object from database pool
        """
        with self._lock:
            connection = self._get_connection()
        try:
            yield connection[CONNECTION]
            self._commit_db_connection(connection[CONNECTION])
        except DBManagerError as e:
            logger.error(e)
            self._roolback_db_connection(connection[CONNECTION])
            self._close_connection(connection)
            raise DBManagerError
        if connection[CREATE_TIME] + self._lifetime < time.time():
            self._return_connection(connection)
        else:
            self._close_connection(connection)

    @contextmanager
    def get_cursor(self):
        """
        Context manager for getting cursor.
        :yield: cursor object from database pool
        """
        with self._lock:
            connection = self._get_connection()
            cursor = self._get_connection_cursor(connection[CONNECTION])
        try:
            yield cursor
            cursor.close()
            self._commit_db_connection(connection[CONNECTION])
        except DBManagerError as e:
            logger.error(e)
            self._roolback_db_connection(connection[CONNECTION])
            raise DBManagerError
        if connection[CREATE_TIME] + self._lifetime < time.time():
            self._return_connection(connection)
        else:
            self._close_connection(connection)

    @abc.abstractmethod
    def execute_get_query(self, query):
        raise NotImplementedError("execute_get_query is not implemented!")