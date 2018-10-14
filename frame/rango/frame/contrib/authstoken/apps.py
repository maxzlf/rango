from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _


class AuthSTokenConfig(AppConfig):
    name = 'rango.frame.contrib.authstoken'
    verbose_name = _("Auth SToken")
