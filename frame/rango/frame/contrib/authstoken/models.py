import uuid
from django.db import models
from django.conf import settings



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
        return self.uid



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
        abstract = ('rango.frame.contrib.authstoken'
                    not in settings.INSTALLED_APPS)
        verbose_name = 'SToken'
        verbose_name_plural = 'STokens'


    def __str__(self):
        return self.token
