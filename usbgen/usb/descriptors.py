from .constants import DESCRIPTOR_TYPE
from .formatters import UInt8Formatter, StringFormatter


class Descriptor(object):
    def __init__(self, descriptor_type):
        self._data = []
        self._size = 0
        self.append(UInt8Formatter(descriptor_type, 'Descriptor Type'))

    def append(self, formatter):
        self._data.append(formatter)
        self._size += len(formatter)

    def prepend(self, formatter):
        self._data.prepend(formatter)
        self._size += len(formatter)

    def get_data(self):
        return [UInt8Formatter(self._size + 1, 'Descriptor Size')] + self._data

    def __call__(*args):
        raise Exception(args)

    def __str__(self):
        return '{\n' + ''.join('\t{}\n'.format(formatter) for formatter in self.get_data()) + '}'


class StringDescriptor(Descriptor):
    def __init__(self, *args):
        super(StringDescriptor, self).__init__(DESCRIPTOR_TYPE.STRING)
        if len(args) == 1 and (type(args[0]) == str or type(args[0]) == unicode):
            self.append(StringFormatter(args[0], 'String'))
