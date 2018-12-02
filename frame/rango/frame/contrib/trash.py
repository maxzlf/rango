# -*- coding: utf-8 -*-
import json
import copy
import logging
from .. import object_accessor
from ..utils import pagination
from ..utils.json import JsonEncoder
from .models import Trash as TrashM


app_logger = logging.getLogger('APP')



class AbstractTrash(object_accessor.ObjectAccessor):


    def get(self, object_id, **kwargs):
        raise NotImplementedError


    def add(self, **kwargs):
        raise NotImplementedError


    def update(self, **kwargs):
        raise NotImplementedError


    def delete(self, object_id, **kwargs) -> None:
        raise NotImplementedError


    def list(self, filters=None, options=None):
        raise NotImplementedError



class DBTrash(AbstractTrash):


    def add(self, model, content, comment=''):
        return TrashM.objects.create(model=model,
                                     content=content,
                                     comment=comment)


    def list(self, filters=None, options=None):
        query_set = TrashM.objects.all()
        if filters:
            params = {k: v for k, v in filters.items() if v is not None}
            query_set = query_set.filter(**params)
        total = len(query_set)
        query_set = pagination.order_and_pagination(query_set, options)
        return total, query_set



def move2trash(obj):
    content = copy.copy(obj.__dict__)
    content.pop('_state', None)
    content = json.dumps(content, cls=JsonEncoder)
    DBTrash().add(obj.__class__.__name__, content)
