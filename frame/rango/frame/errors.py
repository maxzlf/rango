from . import http_errors



class BaseError(http_errors.APIException):
    code = 1
    msg = 'Base error'


    def __init__(self, msg=''):
        self.msg = msg if msg else self.msg



################################################################################
class ServerError(http_errors.ServerError, BaseError):
    """
    Base class of server error
    """
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
    code = 3
    msg = 'Server not implemented error'



class ServerBadGatewayError(ServerError):
    """
    If server depends on a third party server, then if it fails get response
    from third party server, raise bad gateway error.
    """
    code = 4
    msg = 'Server bad gateway error'



class ServerUnavailableError(ServerError):
    """
    If server stopped for upgrade or other reasons, raise unavailable error
    """
    code = 5
    msg = 'Server unavailable'



################################################################################
class ParamError(http_errors.BadRequest, BaseError):
    """
    Base class of param error
    """
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

    """