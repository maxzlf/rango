import uuid
import json
from django.db import models
from django.conf import settings
from .trash import move2trash



class Trash(models.Model):
    """
    Store any deleted contents on any table
    """


    class Meta:
        verbose_name = 'Trash'
        verbose_name_plural = 'Trashes'


    model = models.CharField(db_index=True, max_length=64)
    content = models.TextField(default=json.dumps({}))
    comment = models.CharField(max_length=256, blank=True)
    create_time = models.DateTimeField(auto_now_add=True)


    def to_dict(self):
        return dict(model=self.model,
                    content=json.loads(self.content),
                    comment=self.comment,
                    create_time=self.create_time)



class User(models.Model):
    uid = models.UUIDField(default=uuid.uuid4, unique=True)
    name = models.CharField(max_length=64, blank=True)
    is_activated = models.BooleanField(default=False)
    create_time = models.DateTimeField(auto_now_add=True)
    update_time = models.DateTimeField(auto_now=True)


    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'


    def __str__(self):
        return str(self.uid)


    def delete(self, using=None, keep_parents=False):
        move2trash(self)
        super().delete(using, keep_parents)



class SToken(models.Model):
    """
    The default authorization token model.
    """
    token = models.UUIDField(primary_key=True, default=uuid.uuid4, unique=True)
    user = models.ForeignKey(User, related_name='auth_token',
                             on_delete=models.CASCADE)
    host = models.CharField(max_length=128, null=False, blank=True, default='*')
    create_time = models.DateTimeField(auto_now_add=True)


    class Meta:
        # Work around for a bug in Django:
        # https://code.djangoproject.com/ticket/19422
        #
        # Also see corresponding ticket:
        # https://github.com/tomchristie/django-rest-framework/issues/705
        abstract = ('rango.frame.contrib'
                    not in settings.INSTALLED_APPS)
        verbose_name = 'SToken'
        verbose_name_plural = 'STokens'


    def __str__(self):
        return str(self.token)


    def delete(self, using=None, keep_parents=False):
        move2trash(self)
        super().delete(using, keep_parents)
