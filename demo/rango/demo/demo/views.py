import datetime
from rest_framework.response import Response
from rango.frame.views import pre_request
from .common import DemoAPIView
from .permissions import AllowAny
from . import serializers



class PingView(DemoAPIView):
    permission_classes = (AllowAny,)


    @pre_request()
    def get(self, request, valid_data):
        result = dict(time=datetime.datetime.now())
        return Response(result)



class ExampleView(DemoAPIView):
    permission_classes = (AllowAny,)
    serializer_classes = {'POST': serializers.ExampleSerializer,
                          'PUT': serializers.ExampleSerializer}


    @pre_request()
    def post(self, request, valid_data):
        return Response(valid_data)


    @pre_request()
    def put(self, request, valid_data):
        return Response(valid_data)
