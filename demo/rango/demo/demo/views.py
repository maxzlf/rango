import datetime
from rest_framework.response import Response
from .common import DemoAPIView



class PingView(DemoAPIView):


    def get(self, request, format= None):
        result = dict(time=datetime.datetime.now())
        return Response(result)
