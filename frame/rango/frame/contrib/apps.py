from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _


class ContribConfig(AppConfig):
    name = 'rango.frame.contrib'
    verbose_name = _("Contrib")
