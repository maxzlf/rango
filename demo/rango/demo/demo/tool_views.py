import hmac
import hashlib
from rango.frame.views import request_wrapper
from .common import DemoAPIView
from . import tool_serializers



class HmacView(DemoAPIView):
    serializer_classes = {'POST': tool_serializers.HmacSerializer}


    @request_wrapper
    def post(self, request, valid_data):
        password = valid_data['password']
        request_time = str(valid_data['request_time'])
        digest = hmac.new(password.encode(), msg=request_time.encode(),
                          digestmod=hashlib.sha256).digest().hex()
        return dict(hmac=digest)
