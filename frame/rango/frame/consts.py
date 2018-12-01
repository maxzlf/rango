from collections import Iterator



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



class ConstKey(YJEnum):


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
