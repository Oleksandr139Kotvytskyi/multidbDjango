import configparser
import threading


class Singleton:
    _instance = None
    _lock = threading.Lock()

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            with cls._lock:
                if not cls._instance:
                    cls._instance = super(Singleton, cls).__new__(cls)
        return cls._instance


def get_config(config_path):
    '''
    Function for getting configs.
    :return: conf_dict dict of configs from file
    '''
    conf_dict = {}
    conf = configparser.ConfigParser()
    conf.read(config_path)
    for i in conf.sections():
        conf_dict[i] = {}
        for j in conf.options(i):
            param = conf.get(i, j)
            if param.startswith('eval'):
                param = eval(param[5:-1])
            conf_dict[i][j] = param
    return conf_dict


def fill_cnf_file(filename, database, user, password, host, port, delay, lifetime, poolsize,):
    with open(filename, 'w') as cnf_file:
        cnf_file.write(
            "[client]\n"
            f"database = {database}\n"
            f"user = {user}\n"
            f"password = {password}\n"
            f"host = {host}\n"
            f"port = {port}\n"
            f"delay = {delay}\n"
            f"lifetime = {lifetime}\n"
            f"poolsize = {poolsize}\n"
        )
