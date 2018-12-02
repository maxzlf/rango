from rango.frame.consts import ConstKey



class DemoConstKey(ConstKey):


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
