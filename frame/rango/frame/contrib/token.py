from .. import errors
from .models import SToken



class Token:


    def get(self, token):
        try:
            return SToken.objects.get(token=token)
        except SToken.DoesNotExist:
            msg = 'Token {} not found.'.format(token)
            raise errors.DataNotFoundError(msg)


    def add(self, user, expiry_date, host=None):
        params = dict(user=user, expiry_date=expiry_date, host=host)
        params = {k: v for k, v in params.items() if v is not None}
        return SToken.objects.create(**params)


    def delete(self, token):
        self.get(token).delete()
