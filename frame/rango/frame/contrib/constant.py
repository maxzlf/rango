from django.db import IntegrityError
from .. import errors
from .. import object_accessor
from ..utils import pagination
from . import models



class AbstractConstant(object_accessor.ObjectAccessor):


    def get(self, key, **kwargs):
        raise NotImplementedError


    def add(self, **kwargs):
        raise NotImplementedError


    def update(self, **kwargs):
        raise NotImplementedError


    def add_or_update(self, **kwargs):
        raise NotImplementedError


    def delete(self, key, **kwargs):
        raise NotImplementedError


    def list(self, filters=None, options=None):
        raise NotImplementedError



class DBConstant(AbstractConstant):


    def _get(self, key):
        try:
            return models.YConstant.objects.get(key=key)
        except models.YConstant.DoesNotExist:
            msg = 'Constant {} not found.'.format(key)
            raise errors.DataNotFoundError


    def get(self, key, **kwargs):
        return self._get(key).value


    def add(self, key, value, description=''):
        assert value is not None
        value = str(value)
        params = dict(key=key, value=value, description=description)
        params = {k: v for k, v in params.items() if v is not None}

        try:
            return models.YConstant.objects.create(**params)
        except IntegrityError:
            raise errors.ConflictError


    def update(self, key, value=None, description=None):
        constant = self._get(key)

        if value is not None:
            constant.value = str(value)
        if description is not None:
            constant.description = description
        constant.save()

        return constant


    def add_or_update(self, key, value, description=None):
        try:
            return self.add(key, value, description)
        except errors.ConflictError:
            return self.update(key, value, description)


    def delete(self, key, **kwargs):
        self._get(key).delete()


    def list(self, filters=None, options=None):
        query_set = models.YConstant.objects.all()
        total = len(query_set)
        query_set = pagination.order_and_pagination(query_set, options)
        return total, query_set



class DBConstantFactory(object_accessor.AccessorFactory):


    def create(self, **kwargs):
        return DBConstant()
