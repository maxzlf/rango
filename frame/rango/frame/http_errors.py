from django.utils.translation import ugettext_lazy as _
from rest_framework import status
from rest_framework.exceptions import APIException



class BadRequest(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = _('Bad request.')



class Unauthorized(APIException):
    status_code = status.HTTP_401_UNAUTHORIZED
    default_detail = _('Unauthorized.')



class PermissionDenied(APIException):
    status_code = status.HTTP_403_FORBIDDEN
    default_detail = _('You do not have permission to perform this action.')



class NotFound(APIException):
    status_code = status.HTTP_404_NOT_FOUND
    default_detail = _('Not found.')



class MethodNotAllowed(APIException):
    status_code = status.HTTP_405_METHOD_NOT_ALLOWED
    default_detail = _('Method not allowed.')



class Timeout(APIException):
    status_code = status.HTTP_408_REQUEST_TIMEOUT
    default_detail = _('Request timeout.')



class Conflict(APIException):
    status_code = status.HTTP_409_CONFLICT
    default_detail = _('Data conflict.')



class RequestTooLarge(APIException):
    status_code = status.HTTP_413_REQUEST_ENTITY_TOO_LARGE
    default_detail = _('Request entity too large.')



class UrlTooLarge(APIException):
    status_code = status.HTTP_414_REQUEST_URI_TOO_LONG
    default_detail = _('Request url too long.')



class UnsupportMediaType(APIException):
    status_code = status.HTTP_415_UNSUPPORTED_MEDIA_TYPE
    default_detail = _('Unsupport media type.')



class TooFrequent(APIException):
    status_code = status.HTTP_429_TOO_MANY_REQUESTS
    default_detail = _('Request too frequent.')



class ServerError(APIException):
    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    default_detail = _('Server error.')



class NotImplementError(APIException):
    status_code = status.HTTP_501_NOT_IMPLEMENTED
    default_detail = _('Not implement error.')



class BadGateway(APIException):
    status_code = status.HTTP_502_BAD_GATEWAY
    default_detail = _('Bad gateway.')



class ServerUnavailable(APIException):
    status_code = status.HTTP_503_SERVICE_UNAVAILABLE
    default_detail = _('Server unavailable.')
