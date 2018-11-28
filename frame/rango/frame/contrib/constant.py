from django.db import IntegrityError
from .. import errors
from . import models



class Constant:
    __cache = None    # class level cache


    def __init__(self, cache=None):
        self._cache = None
        if cache:
            self._cache = cache
        elif Constant.__cache:
            self._cache = Constant.__cache
        else:
            pass


    @classmethod
    def set_catch(cls, cache):
        Constant.__cache = cache


    def _get_constant(self, key):
        try:
            return models.YConstant.objects.get(key=key)
        except models.YConstant.DoesNotExist:
            raise errors.DataNotFoundError


    def compose_constant_cache_key(self, key):
        return 'CONSTANT_' + key


    def get(self, key):
        """
        get constant value by specified key
        1. try get from cache
        2. if it's in cache, just return from cache
        3. if not in cache, return from database and reset cache
        :exception: ConstantNotFound
        """
        value = None
        cache_key = self.compose_constant_cache_key(key)

        if self._cache:
            value = self._cache.get(cache_key)

        if value is None:
            constant = self._get_constant(key)
            value = constant.value
            if self._cache:
                self._cache.set(cache_key, value)
        else:
            pass

        return value


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
        """
        1. turn value to str
        2. update to database
        3. update to cache
        """
        constant = self._get_constant(key)
        if value is not None:
            value = str(value)
            constant.value = value
        if description:
            constant.description = description
        constant.save()

        if self._cache and value is not None:
            cache_key = self.compose_constant_cache_key(key)
            self._cache.set(cache_key, value)

        return constant


    def add_or_update(self, key, value, description=None):
        try:
            return self.add(key, value, description)
        except errors.ConflictError:
            return self.update(key, value, description)


    def delete(self, key):
        """
        1. delete from cache
        2. delete from database
        """
        if self._cache:
            cache_key = self.compose_constant_cache_key(key)
            self._cache.delete(cache_key)

        constant = self._get_constant(key)
        constant.delete()


    def list(self):
        query_set = models.YConstant.objects.all()
        total = len(query_set)
        return total, query_set
