from django.utils.translation import ugettext_lazy as _

from rest_framework.authentication import BaseAuthentication
from rest_framework.authentication import get_authorization_header
from rest_framework.exceptions import AuthenticationFailed

from frame.rango.frame.utils.ipware import get_ip
from .models import SToken



class STokenAuthentication(BaseAuthentication):
    """
    Simple token based authentication.
    Clients should authenticate by passing the token key in the "Authorization"
    HTTP header, prepended with the string
    "401f7ac837da42b97f613d789819ff93537bee6a" for example
    """

    keyword = 'SToken'
    model = SToken


    def authenticate(self, request):
        token = get_authorization_header(request)
        try:
            token = token.decode()
        except UnicodeError:
            msg = _('Invalid token header. '
                    'Token string should not contain invalid characters.')
            raise AuthenticationFailed(msg)

        return self.authenticate_credentials(token, request)


    def authenticate_credentials(self, token, request):
        model = self.model
        try:
            stoken = model.objects.select_related('user').get(token=token)
        except model.DoesNotExist:
            raise AuthenticationFailed(_('Invalid stoken.'))

        if not self._check_host_pattern(get_ip(request), stoken.host):
            raise AuthenticationFailed(_('Unauthorized ip address.'))

        if not stoken.user.is_activated:
            raise AuthenticationFailed(_('User inactivated or deleted.'))

        return stoken.user, stoken


    def authenticate_header(self, request):
        return self.keyword


    def _check_host_pattern(self, ip_addr, pattern):
        # NOTE: This is a quick and dirty implementation.
        # TODO: Improve it asap.
        if pattern == '*':
            return True
        elif ip_addr == pattern:
            return True

        return False
