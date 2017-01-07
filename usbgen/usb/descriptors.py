from .constants import DESCRIPTOR_TYPE
from .formatters import UInt8Formatter, UInt16Formatter, BCD16Formatter, StringFormatter
from .defaults import defaults


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
        else:
            for i, langid in enumerate(args):
                self.append(UInt16Formatter(langid, 'Language Identifier {}'.format(i)))


class DeviceDescriptor(Descriptor):
    def __init__(self, **kwargs):
        super(DeviceDescriptor, self).__init__(DESCRIPTOR_TYPE.DEVICE)

        self.append(BCD16Formatter(defaults.get('usb_version', kwargs, 2.0), "USB Version"))
        self.append(UInt8Formatter(defaults.get('device_class', kwargs, 0), "Device Class"))
        self.append(UInt8Formatter(defaults.get('device_subclass', kwargs, 0), "Device Sub-class"))
        self.append(UInt8Formatter(defaults.get('device_protocol', kwargs, 0), "Device Protocol"))
        self.append(UInt8Formatter(defaults.get('max_packet_size', kwargs, 8), "Max packet size for EP0"))
        self.append(UInt16Formatter(defaults.get('vendor_id', kwargs, 0), "Vendor ID"))
        self.append(UInt16Formatter(defaults.get('product_id', kwargs, 0), "Product ID"))
        self.append(UInt16Formatter(defaults.get('device_release_number', kwargs, 0), "Device release number"))
        self.append(UInt8Formatter(defaults.get('manufacturer_string', kwargs, 0), "Manufacturer string index"))
        self.append(UInt8Formatter(defaults.get('product_string', kwargs, 0), "Product string index"))
        self.append(UInt8Formatter(defaults.get('serial_number_string', kwargs, 0), "Serial string index"))
        self.append(UInt8Formatter(defaults.get('number_of_configurations', kwargs, 1), "Number of configurations"))


class DeviceQualifierDescriptor(Descriptor):
    def __init__(self, **kwargs):
        super(DeviceQualifierDescriptor, self).__init__(DESCRIPTOR_TYPE.DEVICE_QUALIFIER)

        self.append(BCD16Formatter(defaults.get('usb_version', kwargs, 2.0), "USB Version"))
        self.append(UInt8Formatter(defaults.get('device_class', kwargs, 0), "Device Class"))
        self.append(UInt8Formatter(defaults.get('device_subclass', kwargs, 0), "Device Sub-class"))
        self.append(UInt8Formatter(defaults.get('device_protocol', kwargs, 0), "Device Protocol"))
        self.append(UInt8Formatter(defaults.get('max_packet_size', kwargs, 8), "Max packet size for EP0"))
        self.append(UInt8Formatter(defaults.get('number_of_configurations', kwargs, 1), "Number of configurations"))
        self.append(UInt8Formatter(0, "Reserved"))
