from rango.frame import errors
from rango.frame.consts import BaseConstKey, BaseConst



class DemoConstKey(BaseConstKey):


    @property
    def expiry_seconds(self):
        return "EXPIRY_SECONDS"


    @property
    def tuple(self):
        lst = super().tuple
        lst.append(self.expiry_seconds)
        return tuple(lst)


    def default_value(self, key):
        default = dict(EXPIRY_SECONDS=1800)
        value = super().default_value(key)
        if value is None:
            value = default.get(key, None)
        return value



class DemoConst(BaseConst):


    @property
    def expiry_seconds(self):
        try:
            value = self._constant.get(self._const_key.replay_tolerance)
            return int(value)
        except errors.DataNotFoundError:
            key = self._const_key.replay_tolerance
            return self._const_key.default_value(key)
