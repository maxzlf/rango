import json
import hmac
import hashlib
from rango.frame.views import request_wrapper
from rango.frame.utils.json import JsonEncoder
from .common import DemoAPIView
from . import tool_serializers



class ToolView(DemoAPIView):
    pass



class HmacView(ToolView):
    serializer_classes = {'POST': tool_serializers.HmacSerializer}


    @request_wrapper
    def post(self, request, valid_data):
        password = valid_data['password']
        data = valid_data['data']
        json_data = json.dumps(data, sort_keys=True, cls=JsonEncoder,
                               ensure_ascii=False, separators=(',', ':'))
        signature = hmac.new(password.encode(),
                             json_data.encode(),
                             digestmod=hashlib.sha256).digest().hex()
        return dict(hmac=signature, json_encoded=json_data)
