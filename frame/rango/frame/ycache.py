class AbstractCache:


    def get(self, key):
        raise NotImplementedError


    def set(self, key, value, **kwargs):
        raise NotImplementedError


    def delete(self, key):
        raise NotImplementedError


    def hset(self, name, key, value):
        raise NotImplementedError


    def flush(self):
        raise NotImplementedError



class CacheFactory:


    def __init__(self, **kwargs):
        raise NotImplementedError


    def create(self, **kwargs) -> AbstractCache:
        raise NotImplementedError
