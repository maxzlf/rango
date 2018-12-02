class ObjectAccessor:


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



class AccessorFactory:


    def create(self, **kwargs) -> ObjectAccessor:
        raise NotImplementedError
