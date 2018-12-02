from collections import Iterator
from . import errors
from .contrib.constant import AbstractConstant



class YJEnum(Iterator):


    def __init__(self):
        self._index = 0


    def __next__(self):
        tpl = self.tuple
        if self._index < len(tpl):
            val = tpl[self._index]
            self._index += 1
            return val
        else:
            raise StopIteration()


    def __iter__(self):
        return self


    @property
    def tuple(self):
        raise NotImplementedError


    @property
    def choices(self):
        return tuple([(k, k) for k in self.tuple])



class BaseConstKey(YJEnum):


    @property
    def token(self):
        return "TOKEN"


    @property
    def activated(self):
        return "ACTIVATED"


    @property
    def debug_mode(self):
        return "DEBUG_MODE"


    @property
    def replay_tolerance(self):
        return "REPLAY_TOLERANCE"


    @property
    def tuple(self):
        return self.token, self.activated, self.debug_mode, \
               self.replay_tolerance


    def default_value(self, key):
        default = dict(ACTIVATED=False, DEBUG_MODE=False, REPLAY_TOLERANCE=30)
        return default.get(key, None)



class BaseConst:


    def __init__(self, constant):
        assert isinstance(constant, AbstractConstant)
        self._constant = constant
        self._const_key = BaseConstKey()


    @property
    def token(self):
        try:
            return self._constant.get(self._const_key.token)
        except errors.DataNotFoundError:
            return self._const_key.default_value(self._const_key.token)


    @property
    def activated(self):
        try:
            value = self._constant.get(self._const_key.activated)
            return value in ('True', 'true', True)
        except errors.DataNotFoundError:
            return self._const_key.default_value(self._const_key.activated)



    @property
    def debug_mode(self):
        try:
            value = self._constant.get(self._const_key.debug_mode)
        except errors.DataNotFoundError:
            value = self._const_key.default_value(self._const_key.debug_mode)

        return value in ('True', 'true', True)


    @property
    def replay_tolerance(self):
        try:
            value = self._constant.get(self._const_key.replay_tolerance)
            return float(value)
        except errors.DataNotFoundError:
            key = self._const_key.replay_tolerance
            return self._const_key.default_value(key)
