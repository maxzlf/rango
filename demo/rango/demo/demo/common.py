from django.db.models import QuerySet
from rest_framework.generics import GenericAPIView
from rest_framework.viewsets import ModelViewSet
from rango.frame.views import LoggedAPIView
from rango.frame.serializers import APISerializer, ListSerializer



class DemoAPISerializer(APISerializer):
    pass



class DemoListSerializer(ListSerializer):
    pass



class DemoViewMixin(LoggedAPIView):
    pass



class DemoAPIView(DemoViewMixin, GenericAPIView):
    pass



class DemoModelViewSet(DemoViewMixin, ModelViewSet):
    pass



def order_and_pagination(query_set, options):
    assert isinstance(query_set, QuerySet)
    if options and options.get('order_by', None):
        query_set = query_set.order_by(*options.get('order_by'))
        offset = options.get('offset', 0)
        limit = options.get('limit', 0)
        query_set = query_set[offset:offset + limit]
    return query_set
