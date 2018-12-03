import copy
import json
import datetime
from rest_framework import exceptions
from .utils.json import JsonEncoder
from .utils.time import delta_seconds
from . import errors
from . import consts



class Processor:


    def __init__(self, view, request, data):
        self.view = view
        self.request = request
        self.data = data


    def process(self):
        """
        handle data and return data
        """
        raise NotImplementedError



class RequestValidateOnlyProcessor(Processor):


    def process(self):
        """
        Process validate_only field.
        """
        data_copy = copy.deepcopy(self.data)
        if data_copy.pop('validate_only', False):
            raise errors.Success
        return data_copy



class RequestOutputOnlyProcessor(Processor):


    def process(self):
        """
        Process output only field, they don't need to be verified.
        """
        data_copy = copy.deepcopy(self.data)
        output_only_fields = self.view.get_serializer_class().output_only
        output_only_fields = output_only_fields if output_only_fields else ()
        for field in self.data.keys():
            if field in output_only_fields:
                del data_copy[field]
        return data_copy



class RequestListOptionsProcessor(Processor):


    def process(self):
        data_copy = copy.deepcopy(self.data)
        options = ('offset', 'limit', 'order_by')
        if all(o in data_copy for o in options):
            offset = data_copy.pop('offset')
            limit = data_copy.pop('limit')
            order_by = data_copy.pop('order_by')
            data_copy['options'] = dict(offset=offset, limit=limit,
                                        order_by=order_by)
        elif not any(o in data_copy for o in options):
            pass
        else:
            assert False

        return data_copy



class RequestFieldMaskProcessor(Processor):


    def process(self):
        """
        Field mask field is used in response data processor, should be deleted
        during request processing.
        """
        data_copy = copy.deepcopy(self.data)
        data_copy.pop('field_mask', None)
        return data_copy



class RequestProcessor(Processor):
    """
    Use filter pattern to process request data in many ways.
    """


    def process(self):
        view = self.view
        request = self.request
        data = self.data

        data = RequestValidateOnlyProcessor(view, request, data).process()
        data = RequestOutputOnlyProcessor(view, request, data).process()
        data = RequestListOptionsProcessor(view, request, data).process()
        data = RequestFieldMaskProcessor(view, request, data).process()

        return data



class ResponseCheckProcessor(Processor):
    """
    Verify response data
    """


    def process(self):
        data_copy = copy.deepcopy(self.data)
        try:
            serializer = self.view.get_serializer_class()(data=data_copy)
            _declared_fields = serializer._declared_fields
            _declared_fields_copy = copy.deepcopy(_declared_fields)

            for field in _declared_fields:
                if field in serializer.input_only:
                    del _declared_fields_copy[field]

            serializer._declared_fields = _declared_fields_copy
            serializer.is_valid(raise_exception=True)
            return data_copy
        except exceptions.ValidationError as e:
            raise errors.DataInValidError(msg=e.detail)



class ResponseMaskFieldsProcessor(Processor):
    """
    Mask fields of response data according to field_mask in serializer.
    """


    def _mask_fields(self, field_mask, data, level=0):
        if isinstance(data, dict):
            data_copy = copy.deepcopy(data)
            for k in data:
                result = self._mask_fields(field_mask, data[k], level + 1)
                data_copy[k] = result

                field = k if level == 0 else str(level) + k
                if field in field_mask:
                    del data_copy[k]
            return data_copy
        elif isinstance(data, list):
            data_copy = []
            for i in data:
                result = self._mask_fields(field_mask, i, level + 1)
                data_copy.append(result)
            return data_copy
        else:
            return data


    def process(self):
        data_copy = copy.deepcopy(self.data)
        validate_data = self.view.get_validated_data(self.request)
        field_mask = validate_data.get('field_mask', ())
        data_copy = self._mask_fields(field_mask, data_copy)
        return data_copy



class ResponseProcessor(Processor):
    """
    Use filter pattern to process response data in many ways.
    """


    def process(self):
        view = self.view
        request = self.request
        data = self.data

        data = ResponseCheckProcessor(view, request, data).process()
        data = ResponseMaskFieldsProcessor(view, request, data).process()
        return data



class RequestAuthProcessor(Processor):
    """
    Check request authentication.
    """


    def _get_auth_fields(self, data):
        token = self.request.META.get('HTTP_TOKEN', None)
        signature = self.request.META.get('HTTP_SIGNATURE', None)
        request_time = data.get('request_time', None)

        if token and signature and request_time:
            return token, signature, request_time
        else:
            return None


    def _check_time(self, request_time):
        const_accessor = self.view.const_accessor
        base_const = consts.BaseConst(const_accessor)

        request_time = request_time.replace(tzinfo=None)
        replay_tolerance = base_const.replay_tolerance
        delta = delta_seconds(request_time)
        if delta > replay_tolerance:
            raise errors.ReplayAttackSuspected


    def _get_token(self, token):
        token_accessor = self.view.token_accessor
        try:
            return token_accessor.get(token)
        except errors.DataNotFoundError:
            raise errors.NeedLogin


    def _check_expired(self, stoken):
        if stoken.expiry_time < datetime.datetime.now():
            raise errors.TokenExpired


    def _check_signature(self, stoken, signature, data):
        print(json.dumps(data))


    def process(self):
        data_copy = copy.deepcopy(self.data)

        auth_fields = self._get_auth_fields(data_copy)
        if not auth_fields:
            return data_copy

        token, signature, request_time = auth_fields
        self._check_time(request_time)

        stoken = self._get_token(token)
        self._check_expired(stoken)
        self._check_signature(stoken, signature, data_copy)

        data_copy.pop("request_time", None)
        return data_copy



class RequestPermProcessor(Processor):
    """
    Use filter pattern to process response data in many ways.
    """


    def process(self):
        view = self.view
        request = self.request
        data = self.data

        data = RequestAuthProcessor(view, request, data).process()
        return data
