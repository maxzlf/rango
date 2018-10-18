from rest_framework.generics import GenericAPIView
from rest_framework.viewsets import ModelViewSet
from rango.frame.views import LoggedAPIView, APISerializer



class DemoAPISerializer(APISerializer):
    pass



class DemoViewMixin(LoggedAPIView):
    pass



class DemoAPIView(DemoViewMixin, GenericAPIView):
    pass



class DemoModelViewSet(DemoViewMixin, ModelViewSet):
    pass
