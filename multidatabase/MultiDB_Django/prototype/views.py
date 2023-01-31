from rest_framework.views import APIView
from rest_framework.response import Response

from MultiDatabaseDjango.settings import database_connection_factory
from db.src.execution import ExecutionModule
from db.src.utils.exceptions import ManagerDoesNotExist


class ProtoView(APIView):

    def get(self, request):
        db_manager = request.GET.get('db_manager')
        if not db_manager:
            return Response(status=400, data={'error': "DB is not selected. To get available DB use ./available-db/"})
        try:
            data = ExecutionModule.get_prototype_data(db_manager)
            return Response(status=200, data=data)
        except ManagerDoesNotExist:
            return Response(status=400, data={'error': "This DB is not available. To get available DB use ./available-db/"})


class AvailableDB(APIView):

    def get(self, request):
        available_db = [{"db_name": name} for name in database_connection_factory.get_awailable_managers()]
        return Response(available_db)