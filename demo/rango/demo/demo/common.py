from rest_framework.generics import GenericAPIView
from rest_framework.viewsets import ModelViewSet
from rango.frame.views import LoggedAPIView
from rango.frame.contrib.token import DBTokenFactory
from rango.frame.contrib.constant import DBConstantFactory
from rango.frame.serializers import APISerializer, ListSerializer



class DemoAPISerializer(APISerializer):
    pass



class DemoListSerializer(ListSerializer):
    pass



class DemoViewMixin(LoggedAPIView):


    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.const_accessor = DBConstantFactory().create()
        self.token_accessor = DBTokenFactory().create()



class DemoAPIView(DemoViewMixin, GenericAPIView):
    pass



class DemoModelViewSet(DemoViewMixin, ModelViewSet):
    pass
