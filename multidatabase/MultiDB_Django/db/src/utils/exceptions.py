class DBManagerError(Exception):
    """
    Error of DB or pool manager.
    """

    def __str__(self):
        return repr("Some troubles with database database")


class IsNotDbManager(Exception):

    def __str__(self):
        return repr("This class is not DB manager")


class ManagerDoesNotExist(Exception):

    def __str__(self):
        return repr("Such manager does not registered")