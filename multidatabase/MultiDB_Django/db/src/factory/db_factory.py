from db.src.interfaces.db_interface import DbBaseInterface
from db.src.utils.exceptions import ManagerDoesNotExist, IsNotDbManager
from db.src.utils.utils import Singleton


class DbConnectorFactory(Singleton):

    def __init__(self):
        self.__db_managers = {}

    def get_awailable_managers(self):
        return [manager_name for manager_name in self.__db_managers.keys()]

    def get_manager_by_name(self, manager_name):
        try:
            return self.__db_managers[manager_name]
        except KeyError:
            raise ManagerDoesNotExist

    def register_manager(self, db_manager, cnf_file):
        if not issubclass(db_manager, DbBaseInterface):
            raise IsNotDbManager
        manager = db_manager(cnf_file)
        manager.check_connection()
        self.__db_managers[db_manager.get_manager_name()] = manager


__all__ = ['DbConnectorFactory']
