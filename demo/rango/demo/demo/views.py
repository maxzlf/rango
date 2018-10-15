import datetime
from rest_framework.response import Response
from rango.frame import errors
from .common import DemoAPIView
from .permissions import AllowAny



class PingView(DemoAPIView):
    permission_classes = (AllowAny,)


    def get(self, request, format= None):
        result = dict(time=datetime.datetime.now())
        raise errors.ServerError
