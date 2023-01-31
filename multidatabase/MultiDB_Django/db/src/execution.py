from MultiDatabaseDjango.settings import database_connection_factory
from prototype.serializers import PrototypeSerializer
from db.sql_scripts.sql_statesment import get_proto_query
from db.src.utils.decoratos import retry_request
import logging

logger = logging.getLogger('root')


class ExecutionModule:

    @staticmethod
    @retry_request()
    def get_prototype_data(db_manager_name):
        logger.info('start work')
        manager = database_connection_factory.get_manager_by_name(db_manager_name)
        logger.info('manager gotted')
        try:
            logger.info('try to run with cursor')
            base_data = manager.execute_get_query(get_proto_query())
            logger.info(base_data)
            serialized_data = [PrototypeSerializer().run_validation(obj) for obj in base_data]
        except Exception as e:
            logger.error(e)
            raise e
        return serialized_data

