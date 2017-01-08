from .constants import DESCRIPTOR_SUBTYPE

from usbgen.usb import Descriptor, DESCRIPTOR_TYPE
from usbgen.usb.formatters import UInt8Formatter, UInt16Formatter, UInt32Formatter, BCD16Formatter, BitMapFormatter, GUIDFormatter
from usbgen.usb.defaults import defaults


class FunctionalDescriptor(Descriptor):
    def __init__(self, descriptor_subtype):
        super(FunctionalDescriptor, self).__init__(DESCRIPTOR_TYPE.CLASS_SPECIFIC_INTERFACE)

        self.append(UInt8Formatter(descriptor_subtype, "Descriptor Sub-type"))


class HeaderFunctionalDescriptor(FunctionalDescriptor):
    def __init__(self, **kwargs):
        super(HeaderFunctionalDescriptor, self).__init__(DESCRIPTOR_SUBTYPE.HEADER_FUNCTIONAL_DESCRIPTOR)

        self.append(BCD16Formatter(defaults.get('communication_class_specification', kwargs, 1.2), "Communication Class Specification Version"))


class UnionInterfaceFunctionalDescriptor(FunctionalDescriptor):
    def __init__(self, **kwargs):
        super(UnionInterfaceFunctionalDescriptor, self).__init__(DESCRIPTOR_SUBTYPE.UNION_FUNCTIONAL_DESCRIPTOR)

        self.append(UInt8Formatter(defaults.get('control_interface', kwargs, 0), "Control Interface"))

        for i, interface in enumerate(defaults.get('subordinate_interfaces', kwargs, [])):
            self.append(UInt8Formatter(interface, "Subordinate Interface {}".format(i)))


class AbstractControlManagementFunctionalDescriptor(FunctionalDescriptor):
    def __init__(self, **kwargs):
        super(AbstractControlManagementFunctionalDescriptor, self).__init__(DESCRIPTOR_SUBTYPE.ABSTRACT_CONTROL_MANAGEMENT_FUNCTIONAL_DESCRIPTOR)

        self.append(BitMapFormatter(
            1,
            [
                defaults.get('comm_feature', kwargs, False),
                defaults.get('line_coding_state', kwargs, False),
                defaults.get('send_break', kwargs, False),
                defaults.get('network_connection', kwargs, False),
            ],
            "Capabilities"
        ))


class CallManagementFunctionalDescriptor(FunctionalDescriptor):
    def __init__(self, **kwargs):
        super(CallManagementFunctionalDescriptor, self).__init__(DESCRIPTOR_SUBTYPE.CALL_MANAGEMENT_FUNCTIONAL_DESCRIPTOR)

        self.append(BitMapFormatter(
            1,
            [
                defaults.get('device_handles_call_management', kwargs, False),
                defaults.get('management_over_data_interface', kwargs, False),
            ],
            "Capabilities"
        ))

        self.append(UInt8Formatter(defaults.get('data_interface', kwargs, 0), "Data Interface"))
