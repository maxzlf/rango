from django.db import IntegrityError
from django.contrib.auth.hashers import check_password, make_password
from .. import errors
from ..utils import pagination
from .models import User as UserM



class User:


    def get(self, user_id=None, account=None):
        if not (user_id or account):
            assert False

        params = dict(user_id=user_id, account=account)
        params = {k: v for k, v in params.items() if v is not None}

        try:
            return UserM.objects.get(**params)
        except UserM.DoesNotExist:
            msg = 'User of user_id {} not found.'.format(user_id)
            raise errors.DataNotFoundError(msg)


    def add(self, account, password, is_activated=False):
        password = make_password(password)
        params = dict(account=account, password=password,
                      is_activated=is_activated)
        params = {k: v for k, v in params.items() if v is not None}
        return UserM.objects.create(**params)


    def update(self, user_id, account, password, is_activated=False):
        password = make_password(password)

        user = self.get(user_id=user_id)
        if account:
            user.account = account
        if password:
            user.password = password
        if is_activated:
            user.is_activated = is_activated
        try:
            user.save()
            return user
        except IntegrityError:
            raise errors.ConflictError


    def check_password(self, password, user_id=None, account=None):
        user = self.get(user_id=user_id, account=account)
        return check_password(password, user.password)


    def delete(self, user_id=None, account=None):
        self.get(user_id=user_id, account=account).delete()


    def list(self, filters=None, options=None):
        query_set = UserM.objects.all()
        if filters:
            params = {k: v for k, v in filters.items() if v is not None}
            query_set = set.filter(**params)
        total = len(query_set)
        query_set = pagination.order_and_pagination(query_set, options)
        return total, query_set
