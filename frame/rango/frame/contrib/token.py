from .. import errors
from .. import object_accessor
from .models import SToken



class AbstractToken(object_accessor.ObjectAccessor):


    def get(self, token, **kwargs):
        raise NotImplementedError


    def add(self, **kwargs):
        raise NotImplementedError


    def update(self, **kwargs):
        raise NotImplementedError


    def delete(self, token, **kwargs) -> None:
        pass


    def list(self, filters=None, options=None):
        raise NotImplementedError



class DBToken(AbstractToken):


    def get(self, token, **kwargs):
        try:
            return SToken.objects.get(token=token)
        except SToken.DoesNotExist:
            msg = 'Token {} not found.'.format(token)
            raise errors.DataNotFoundError(msg)


    def add(self, user, expiry_time, host=None):
        params = dict(user=user, expiry_time=expiry_time, host=host)
        params = {k: v for k, v in params.items() if v is not None}
        return SToken.objects.create(**params)


    def update(self, **kwargs):
        raise NotImplementedError


    def delete(self, token, **kwargs):
        self.get(token).delete()


    def list(self, filters=None, options=None):
        raise NotImplementedError



class DBTokenFactory(object_accessor.AccessorFactory):


    def create(self, **kwargs):
        return DBToken()
