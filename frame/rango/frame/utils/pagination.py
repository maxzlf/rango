from django.db.models import QuerySet


def order_and_pagination(query_set, options):
    assert isinstance(query_set, QuerySet)
    if options and options.get('order_by', None):
        query_set = query_set.order_by(*options.get('order_by'))
        offset = options.get('offset', 0)
        limit = options.get('limit', 0)
        query_set = query_set[offset:offset + limit]
    return query_set
