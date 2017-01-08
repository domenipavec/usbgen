
class Formatter(object):
    def __init__(self):
        self._len = 0
        self._additional = []
        self._comment = ''
        self._main = ''
        self._max_main_length = 4

    def set(self, main=None, comment=None, additional=None):
        if main is not None:
            self._main = main
        if comment is not None:
            self._comment = comment
        if additional is not None:
            self._additional = additional

    def get_main_length(self):
        return len(self._main)

    def set_max_main_length(self, max_main_length):
        self._max_main_length = max_main_length

    def _parse_int(self, i):
        if type(i) == str:
            return int(i, 0)
        elif type(i) == int:
            return i
        else:
            raise Exception("Invalid type passed for int")

    def __len__(self):
        return self._len

    def __str__(self):
        output = ''
        if self._comment and self._main:
            output += '{0:<{2}}  /* {1} */'.format(self._main, self._comment, self._max_main_length)
        elif self._main:
            output += self._main
        elif self._comment:
            output += '/* {} */'.format(self._comment)
        if self._additional:
            output += '\n' + '\n'.join('\t{}'.format(additional) for additional in self._additional)
        return output


class CommentFormatter(Formatter):
    def __init__(self, comment):
        super(CommentFormatter, self).__init__()

        self.set(comment)

    def set(self, comment):
        super(CommentFormatter, self).set(comment=comment)


class UInt8Formatter(Formatter):
    def __init__(self, i, comment=''):
        super(UInt8Formatter, self).__init__()

        self._len = 1
        self.set(i, comment)

    def set(self, i, comment=None):
        i = self._parse_int(i)

        if i < 0 or i > 255:
            raise Exception("UInt8 out of range")

        output = "{0:#04x},".format(i)

        super(UInt8Formatter, self).set(output, comment)


class UInt16Formatter(Formatter):
    def __init__(self, i, comment=''):
        super(UInt16Formatter, self).__init__()

        self._len = 2
        self.set(i, comment)

    def set(self, i, comment=None):
        i = self._parse_int(i)

        if i < 0 or i > 2**16 - 1:
            raise Exception("UInt16 out of range")

        output = "{0:#04x}, {1:#04x},".format(i & 0xff, i >> 8)

        super(UInt16Formatter, self).set(output, comment)


class UInt32Formatter(Formatter):
    def __init__(self, i, comment=''):
        super(UInt32Formatter, self).__init__()

        self._len = 4
        self.set(i, comment)

    def set(self, i, comment=None):
        i = self._parse_int(i)

        if i < 0 or i > 2**32 - 1:
            raise Exception("UInt32 out of range")

        output = "{0:#04x}, {1:#04x}, {2:#04x}, {3:#04x},".format(i & 0xff, (i >> 8) & 0xff, (i >> 16) & 0xff, i >> 24)

        super(UInt32Formatter, self).set(output, comment)


class BCD16Formatter(Formatter):
    def __init__(self, n, comment=''):
        super(BCD16Formatter, self).__init__()

        self._len = 2
        self.set(n, comment)

    def set(self, n, comment=None):
        if type(n) != float:
            raise Exception("Expected float")

        if n < 0 or n >= 100:
            raise Exception("BCD16 out of range")

        output = "0x{1:02}, 0x{0:02},".format(int(n), int(round((n - int(n)) * 100)))

        super(BCD16Formatter, self).set(output, comment)


class BitMapFormatter(Formatter):
    def __init__(self, n, data, comment=''):
        super(BitMapFormatter, self).__init__()

        self.set(n, data, comment)

    def set(self, n, data, comment=None):
        self._len = n

        if type(n) != int:
            raise Exception("Expected size in int")

        if n < 0 or n > 8:
            raise Exception("Bit map size out of range")

        outdata = [0] * n
        for i in range(n):
            for j in range(8):
                outdata[i] |= (self._get_bit(data, i * 8 + j) << j)

        output = ", ".join("{0:#04x}".format(v) for v in outdata) + ","

        super(BitMapFormatter, self).set(output, comment)

    def _get_bit(self, data, i):
        if len(data) <= i:
            return False
        return data[i]

    @staticmethod
    def uint_parse(n, i):
        if type(n) != int:
            raise Exception("Expected size in int")

        if n < 0 or n > 64:
            raise Exception("uint parse size out of range")

        if type(i) != int:
            raise Exception("Expected data in int")

        if i < 0 or i > (2**n - 1):
            raise Exception("uint parse data out of range")

        data = []
        for j in range(n):
            data.append((i >> j) & 1)

        return data


class GUIDFormatter(Formatter):
    def __init__(self, guid, comment=''):
        super(GUIDFormatter, self).__init__()

        self._len = 16

        self.set(guid, comment)

    def set(self, guid, comment=None):
        if type(guid) != str:
            raise Exception("Expected guid as string")

        parts = guid.split('-')

        if len(parts) != 5:
            raise Exception("Invalid guid")

        super(GUIDFormatter, self).set(
            str(UInt32Formatter(int(parts[0], 16))),
            comment,
            [
                str(UInt16Formatter(int(parts[1], 16))),
                str(UInt16Formatter(int(parts[2], 16))),
                self._format(parts[3]),
                self._format(parts[4]),
            ]
        )

    def _format(self, part):
        return ' '.join([str(UInt8Formatter(int(part[2*i:2*i+2], 16))) for i in range(len(part)/2)])


class StringFormatter(Formatter):
    def __init__(self, string, comment=''):
        super(StringFormatter, self).__init__()

        self.set(string, comment)

    def set(self, string, comment=None):
        if type(string) == unicode:
            pass
        elif type(string) == str:
            string = unicode(string)
        else:
            raise Exception("Expected string")

        if len(string) == 0:
            raise Exception("Empty string")

        self._len = len(string) * 2

        super(StringFormatter, self).set(self._format(string[0]), comment, [self._format(s) for s in string[1:]])

    def _format(self, char):
        encoded = char.encode('utf-16')
        return "{0}, {1},".format(self._format_byte(encoded[2]), self._format_byte(encoded[3]))

    def _format_byte(self, byte):
        if ord(' ') <= ord(byte) <= ord('~'):
            return "'%s'" % byte
        else:
            return "{0:#04x}".format(ord(byte))
