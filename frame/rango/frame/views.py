import json
import logging
import traceback
from uuid import uuid4
from functools import wraps
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from rest_framework.views import APIView, set_rollback
from rest_framework.utils.encoders import JSONEncoder

from . import errors
from .consts import BaseConst
from .utils.ipware import get_ip
from .serializers import APISerializer
from .contrib.token import AbstractToken
from .permissions import DenyAny, AllowAny
from .contrib.constant import AbstractConstant
from .processor import RequestProcessor, RequestPermProcessor, ResponseProcessor



class LoggedAPIView(APIView):
    authentication_classes = ()         # don't touch this line
    permission_classes = (AllowAny, )   # don't touch this line
    api_logger = logging.getLogger('API')
    common_permission_classes = (DenyAny, )
    post_permission_classes = (DenyAny, )
    put_permission_classes = (DenyAny, )
    get_permission_classes = (DenyAny, )
    delete_permission_classes = (DenyAny, )
    serializer_classes = None


    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._log_id = str(uuid4())
        self.const_accessor = AbstractConstant()
        self.token_accessor = AbstractToken()


    def initialize_request(self, request, *args, **kwargs):
        self._log_raw_request(request)
        return super().initialize_request(request, *args, **kwargs)


    def initial(self, request, *args, **kwargs):
        self._log_request(request)
        super().initial(request, *args, **kwargs)
        self._log_authentication(request)
        request.validated_data = self.get_validated_data(request)


    def finalize_response(self, request, response, *args, **kwargs):
        response = super().finalize_response(request, response, *args, **kwargs)
        self._log_response(response)
        return response


    @property
    def default_serializer_class(self):
        return APISerializer


    def get_serializer_class(self):
        serializer_class = getattr(self, 'serializer_class', None)
        if serializer_class:
            return serializer_class

        method = self.request.method
        if not self.serializer_classes or method not in self.serializer_classes:
            return self.default_serializer_class

        serializer_class = self.serializer_classes[method]
        assert issubclass(serializer_class, self.default_serializer_class)
        return serializer_class


    def get_validated_data(self, request):
        data = request.GET if request.method in ('GET', 'DELETE') \
            else request.data
        request.request_data = data
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        return serializer.validated_data


    def _log_raw_request(self, request):
        msg = '{}|{}|{}'.format(self._log_id, 'RAW_REQUEST',
                                self._extract_raw_request_info(request))
        self.api_logger.info(msg)


    def _log_request(self, request):
        info = {
            'method': request.method.upper(),
            'uri': request.build_absolute_uri(),
            'content_type': request.content_type,
            'authorization': request.META.get('HTTP_AUTHORIZATION'),
            'data': str(request.data),
        }
        info_str = self.json_dump(info)
        msg = '{}|{}|{}'.format(self._log_id, 'REQUEST', info_str)
        self.api_logger.info(msg)


    def _log_authentication(self, request):
        info = {
            'user_type': type(request.user).__name__,
            'id': request.user.id,
            'detail': str(request.user),
        }
        info_str = self.json_dump(info)
        msg = '{}|{}|{}'.format(self._log_id, 'AUTH', info_str)
        self.api_logger.info(msg)


    def _log_response(self, response):
        info = {
            'status': (response.status_code, response.status_text),
            'content': response.data,
        }
        info_str = self.json_dump(info)
        msg = '{}|{}|{}'.format(self._log_id, 'RESPONSE', info_str)
        self.api_logger.info(msg)


    def _extract_raw_request_info(self, request):
        info = {
            'method': request.method,
            'uri': request.build_absolute_uri(),
            'content_type': request.META.get('CONTENT_TYPE', ''),
            'remote_addr': get_ip(request),
        }
        return info


    def json_dump(self, data):
        return json.dumps(data, sort_keys=True, cls=JSONEncoder)



class StaticView(LoggedAPIView):
    content = {'message': 'Hello, MSA.'}


    def get(self, request, format=None):
        return Response(self.content)


def exception_handler(exc, context):
    """
    Returns the response that should be used for any given exception.

    By default we handle the REST framework `APIException`, and also
    Django's built-in `Http404` and `PermissionDenied` exceptions.

    Any unhandled exceptions may return `unknown error`,
    which will cause a 500 error to be raised.
    """
    api_logger = logging.getLogger('API')

    try:
        if isinstance(exc, errors.BaseError):
            raise exc
        elif isinstance(exc, ValidationError):
            raise errors.ParamError(msg=exc.detail)
        else:
            raise errors.ServerUnknownError
    except errors.BaseError as exc:
        data = dict(code=exc.code, msg=exc.msg, details=traceback.format_exc())
        const_accessor = context['view'].const_accessor
        api_logger.error(data)
        base_const = BaseConst(const_accessor)
        if not base_const.debug_mode:
            del data['details']
        set_rollback()
        return Response(data, status=exc.status_code)


def request_wrapper(func):
    """
    Decorate a view method, pre-process params of a request
    :param func:
    :return:
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        view = args[0]
        request = args[1]
        assert isinstance(view, LoggedAPIView)
        assert isinstance(request, Request)

        valid_data = view.get_validated_data(request)
        valid_data = RequestProcessor(view, request, valid_data).process()
        valid_data = RequestPermProcessor(view, request, valid_data).process()
        res_data = func(*args, **kwargs, valid_data=valid_data)
        res_data = res_data if res_data is not None else {}
        res_data = ResponseProcessor(view, request, res_data).process()
        return Response(res_data)

    return wrapper
