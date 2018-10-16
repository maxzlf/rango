from rest_framework import status
from rest_framework.exceptions import APIException



class BaseError(APIException):
    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    code = 1
    msg = 'Base error'
    details = ''


    def __init__(self, msg='', details=''):
        self.msg = msg if msg else self.msg
        self.details = details if details else self.details



################################################################################
class ServerError(BaseError):
    """
    Base class of server error
    """
    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    code = 1
    msg = 'Server error'



class ServerUnknownError(ServerError):
    """
    Unknown error, maybe caused by framework or third party library, or just an
    unhandled bug.
    """
    code = 1
    msg = 'Server unknown error'



class ServerFailedError(ServerError):
    """
    Server knows what the error is, can't handle it but to fail. This may
    because server entered an invalid status for example.
    """
    code = 2
    msg = 'Server failed error'



class ServerNotImplementedError(ServerError):
    """
    The feature not implemented by server yet.
    """
    status_code = status.HTTP_501_NOT_IMPLEMENTED
    code = 3
    msg = 'Server not implemented error'



class ServerBadGatewayError(ServerError):
    """
    If server depends on a third party server, then if it fails get response
    from third party server, raise bad gateway error.
    """
    status_code = status.HTTP_502_BAD_GATEWAY
    code = 4
    msg = 'Server bad gateway error'



class ServerUnavailableError(ServerError):
    """
    If server stopped for upgrade or other reasons, raise unavailable error
    """
    status_code = status.HTTP_503_SERVICE_UNAVAILABLE
    code = 5
    msg = 'Server unavailable'



################################################################################
class ParamError(BaseError):
    """
    Base class of param error
    """
    status_code = status.HTTP_400_BAD_REQUEST
    code = 100
    msg = 'Param error'



class ParamValidationError(ParamError):
    """
    Request param failed validation.
    """
    code = 101
    msg = 'Param validation error'



class ParamFormatError(ParamError):
    """
    The request entity has a media type which the server or resource does not
    support. For example, the client uploads an image as image/svg+xml,
    but the server requires that images use a different format.
    """
    status_code = status.HTTP_415_UNSUPPORTED_MEDIA_TYPE
    code = 102
    msg = 'Unsupport param media format type'



class ParamUnsupportError(ParamError):
    """
    Enum type in param not support yet.
    """
    code = 103
    msg = 'Param unsupport error'



class RestrictError(BaseError):
    """

    """
    status_code = status.HTTP_400_BAD_REQUEST
    code = 110
    msg = 'Api is restrict for access'



class TooFrequent(BaseError):
    """

    """
    status_code = status.HTTP_429_TOO_MANY_REQUESTS
    code = 111
    msg = 'Request too frequent'
