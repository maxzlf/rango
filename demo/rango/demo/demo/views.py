import datetime
from rest_framework.response import Response
from rango.frame import errors
from .common import DemoAPIView
from .permissions import AllowAny
from . import serializers



class PingView(DemoAPIView):
    permission_classes = (AllowAny,)


    def get(self, request, format= None):
        result = dict(time=datetime.datetime.now())
        return Response(result)



class ExampleView(DemoAPIView):
    permission_classes = (AllowAny,)
    serializer_classes = {'POST': serializers.ExampleSerializer,
                          'PUT': serializers.ExampleSerializer}


    def post(self, request):
        data = self.get_validated_data(request)
        return Response(data)


    def put(self, request):
        data = self.get_validated_data(request)
        return Response(data)
