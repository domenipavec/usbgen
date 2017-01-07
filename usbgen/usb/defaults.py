
class Defaults(object):
    def __init__(self):
        self._data = {}

    def set(self, **kwargs):
        self._data.update(kwargs)
        return ''

    def get(self, key, kwargs={}, default=None):
        return kwargs.get(key, self._data.get(key, default))


defaults = Defaults()
