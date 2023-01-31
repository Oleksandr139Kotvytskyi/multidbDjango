from db.src.interfaces.db_interface import DbBaseInterface
from db.src.utils.constants import DB_CONNECTION_USER, DB_CONNECTION_PASS, DB_CONNECTION_HOST, DB_CONNECTION_DATABASE, DB_CONNECTION_PORT
from db.src.utils.utils import Singleton


class ExasolDbManager(DbBaseInterface, Singleton):
    import pyexasol as exasol_connector

    @staticmethod
    def get_manager_name():
        return "ExasolDb"

    def __init__(self, cnf_file):
        super(ExasolDbManager, self).__init__(cnf_file)
        self.get_cursor = self.get_connect

    def check_connection(self):
        self._make_connection().close()

    def _make_connection(self):
        connection_user = self._connection_settings[DB_CONNECTION_USER]
        connection_password = self._connection_settings[DB_CONNECTION_PASS]
        connection_host = self._connection_settings[DB_CONNECTION_HOST]
        connection_database = self._connection_settings[DB_CONNECTION_DATABASE]
        connection = self.exasol_connector.connect(
            user=connection_user,
            password=connection_password,
            dsn=connection_host,
            schema=connection_database,
            encryption=False,
            fetch_dict=True,
        )
        return connection

    def _close_db_connection(self, connection):
        connection.close()

    def _commit_db_connection(self, connection):
        connection.commit()

    def _roolback_db_connection(self, connection):
        connection.rollback()

    def _get_connection_cursor(self, connection):
        return connection

    def execute_get_query(self, query):
        with self.get_cursor() as cur:
            exa_statement = cur.execute(query)
            uppercase_base_data = exa_statement.fetchall()
            base_data = []
            for i in uppercase_base_data:
                base_data.append({k.lower(): v for k, v in i.items()})
        return base_data
