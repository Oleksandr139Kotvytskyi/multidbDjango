from db.src.interfaces.db_interface import DbBaseInterface
from db.src.utils.constants import DB_CONNECTION_USER, DB_CONNECTION_PASS, DB_CONNECTION_HOST, DB_CONNECTION_DATABASE
from db.src.utils.utils import Singleton


class PostgresDbManager(DbBaseInterface, Singleton):
    import psycopg2 as postgres_connector

    @staticmethod
    def get_manager_name():
        return "PostgresDb"

    def check_connection(self):
        self._make_connection().close()

    def _make_connection(self):
        connection_user = self._connection_settings[DB_CONNECTION_USER]
        connection_password = self._connection_settings[DB_CONNECTION_PASS]
        connection_host = self._connection_settings[DB_CONNECTION_HOST]
        connection_database = self._connection_settings[DB_CONNECTION_DATABASE]
        connection = self.postgres_connector.connect(
            user=connection_user,
            password=connection_password,
            host=connection_host,
            database=connection_database
        )
        return connection

    def _close_db_connection(self, connection):
        connection.close()

    def _commit_db_connection(self, connection):
        connection.commit()

    def _roolback_db_connection(self, connection):
        connection.rollback()

    def _get_connection_cursor(self, connection):
        return connection.cursor(cursor_factory=self.postgres_connector.extras.RealDictCursor)

    def execute_get_query(self, query):
        with self.get_cursor() as cur:
            cur.execute(query)
            base_data = cur.fetchall()
        return base_data