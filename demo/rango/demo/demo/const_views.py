import datetime
from rest_framework.generics import GenericAPIView
from rango.frame.views import LoggedAPIView
from rango.frame.views import request_wrapper
from rango.frame.permissions import AllowAny
from rango.frame.contrib.token import DBTokenFactory
from rango.frame.contrib.constant import DBConstantFactory
from . import config_serializers



class ConfigViewMixin(LoggedAPIView):
    common_permission_classes = (AllowAny, )


    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.const_accessor = DBConstantFactory().create()
        self.token_accessor = DBTokenFactory().create()



class ConfigAPIView(ConfigViewMixin, GenericAPIView):
    pass



class PingView(ConfigAPIView):
    get_permission_classes = ()


    @request_wrapper
    def get(self, request, valid_data):
        return dict(time=datetime.datetime.now())



class ConstantsView(ConfigAPIView):
    get_permission_classes = ()
    post_permission_classes = ()
    serializer_classes = {'POST': config_serializers.ConstantsPostSerializer}


    @request_wrapper
    def post(self, request, valid_data):
        const = self.const_accessor.add(**valid_data)
        result = dict(key=const.key, value=const.value,
                      description=const.description)
        return result


    @request_wrapper
    def get(self, request, valid_data=None):
        total, constants = self.const_accessor.list()
        result = dict(total=total, entries=[])

        for const in constants:
            result['entries'].append(dict(key=const.key,
                                          value=const.value,
                                          description=const.description))
        return result



class ConstantView(ConfigAPIView):
    get_permission_classes = ()
    put_permission_classes = ()
    delete_permission_classes = ()
    serializer_classes = {'PUT': config_serializers.ConstantPutSerializer}


    @request_wrapper
    def get(self, request, key, valid_data=None):
        value = self.const_accessor.get(key)
        result = dict(key=key, value=value)
        return result


    @request_wrapper
    def put(self, request, key, valid_data=None):
        const = self.const_accessor.update(key, **valid_data)
        result = dict(key=const.key, value=const.value,
                      description=const.description)
        return result


    @request_wrapper
    def delete(self, request, key, valid_data=None):
        self.const_accessor.delete(key)
        return dict()
