from rest_framework import serializers
from rest_framework.generics import GenericAPIView
from rest_framework.viewsets import ModelViewSet
from rango.frame.permissions import DenyAny
from rango.frame.views import LoggedAPIView



class DemoAPISerializer(serializers.Serializer):
    pass



class DemoViewMixin(LoggedAPIView):
    authentication_classes = ()
    permission_classes = (DenyAny, )
    serializer_classes = None


    @property
    def default_serializer_class(self):
        return DemoAPISerializer


    def get_serializer_class(self):
        serializer_class = getattr(self, 'serializer_class', None)
        if serializer_class:
            return serializer_class

        method = self.request.method
        if not self.serializer_classes or method not in self.serializer_classes:
            return self.default_serializer_class

        serializer_class = self.serializer_classes[method]
        assert issubclass(serializer_class, self.default_serializer_class)
        return serializer_class


    def get_validated_data(self, request):
        data = request.GET if request.method == 'GET' else request.data
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        return serializer.validated_data



class DemoAPIView(DemoViewMixin, GenericAPIView):
    pass



class DemoModelViewSet(DemoViewMixin, ModelViewSet):
    pass
