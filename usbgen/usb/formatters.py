
class Formatter(object):
    def __init__(self, main, comment='', additional=[]):
        self._main = main
        self._comment = comment
        self._additional = additional

        if not hasattr(self, '_len'):
            self._len = 0

    def __len__(self):
        return self._len

    def __str__(self):
        output = ''
        if self._comment:
            output += '{:<12} /* {} */'.format(self._main, self._comment)
        else:
            output += self._main
        if self._additional:
            output += '\n' + '\n'.join('\t{}'.format(additional) for additional in self._additional)
        return output


class UInt8Formatter(Formatter):
    def __init__(self, i, comment=''):
        if type(i) != int:
            raise Exception("Expected int")

        if i < 0 or i > 255:
            raise Exception("Int out of range")

        self._len = 1

        output = "{0:#04x},".format(i)

        super(UInt8Formatter, self).__init__(output, comment)


class StringFormatter(Formatter):
    def __init__(self, string, comment=''):
        if type(string) == unicode:
            pass
        elif type(string) == str:
            string = unicode(string)
        else:
            raise Exception("Expected string")

        if len(string) == 0:
            raise Exception("Empty string")

        self._len = len(string) * 2

        super(StringFormatter, self).__init__(self._format(string[0]), comment, [self._format(s) for s in string[1:]])

    def _format(self, char):
        encoded = char.encode('utf-16')
        return "{0}, {1},".format(self._format_byte(encoded[2]), self._format_byte(encoded[3]))

    def _format_byte(self, byte):
        if ord(' ') <= ord(byte) <= ord('~'):
            return "'%s'" % byte
        else:
            return "{0:#04x}".format(ord(byte))
