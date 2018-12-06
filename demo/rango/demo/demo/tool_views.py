import json
import hmac
import hashlib
from rest_framework.generics import GenericAPIView
from rango.frame.views import LoggedAPIView
from rango.frame.views import request_wrapper
from rango.frame.utils.json import JsonEncoder
from rango.frame.permissions import AllowAny, IsDebugMode
from rango.frame.contrib.token import DBTokenFactory
from rango.frame.contrib.constant import DBConstantFactory

from . import tool_serializers



class ToolViewMixin(LoggedAPIView):
    common_permission_classes = (IsDebugMode, )


    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.const_accessor = DBConstantFactory().create()
        self.token_accessor = DBTokenFactory().create()



class ToolView(ToolViewMixin, GenericAPIView):
    pass



class HmacView(ToolView):
    serializer_classes = {'POST': tool_serializers.HmacSerializer}
    post_permission_classes = ()


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
