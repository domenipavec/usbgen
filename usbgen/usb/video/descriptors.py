from .constants import DESCRIPTOR_TYPE, DESCRIPTOR_SUBTYPE, TERMINAL_TYPE

from usbgen.usb import DescriptorWithChildren, Descriptor
from usbgen.usb.formatters import UInt8Formatter, UInt16Formatter, UInt32Formatter, BCD16Formatter
from usbgen.usb.defaults import defaults


class VideoClassInterfaceDescriptor(DescriptorWithChildren):
    def __init__(self, *children, **kwargs):
        super(VideoClassInterfaceDescriptor, self).__init__(DESCRIPTOR_TYPE.CS_INTERFACE, *children)

        self.append(UInt8Formatter(DESCRIPTOR_SUBTYPE.VC_HEADER, "Descriptor Sub-type"))

        self.append(BCD16Formatter(defaults.get('video_class_specification', kwargs, 1.5), "Video class specification"))

        self.append(self._size_formatter)

        self.append(UInt32Formatter(defaults.get('clock_frequency', kwargs, 48000000), "Video class specification"))

        video_streaming_interfaces = defaults.get('video_streaming_interfaces', kwargs, [])

        self.append(UInt8Formatter(len(video_streaming_interfaces), "Number of video streaming interfaces"))
        for i, video_streaming_interface in enumerate(video_streaming_interfaces):
            self.append(UInt8Formatter(video_streaming_interface, "Number of {}-th video streaming interface".format(i+1)))


class TerminalDescriptor(Descriptor):
    def __init__(self, subtype, terminal_id):
        super(TerminalDescriptor, self).__init__(DESCRIPTOR_TYPE.CS_INTERFACE)

        self.append(UInt8Formatter(subtype, "Descriptor Sub-type"))

        self.append(UInt8Formatter(terminal_id, "Terminal ID"))


class InputTerminalDescriptor(TerminalDescriptor):
    def __init__(self, terminal_id, **kwargs):
        super(InputTerminalDescriptor, self).__init__(DESCRIPTOR_SUBTYPE.VC_INPUT_TERMINAL, terminal_id)

        self.append(UInt16Formatter(defaults.get('input_terminal_type', kwargs, TERMINAL_TYPE.ITT_VENDOR_SPECIFIC), "Input terminal type"))
        self.append(UInt8Formatter(defaults.get('associated_terminal_id', kwargs, 0), "Associated Terminal ID"))
        self.append(UInt8Formatter(defaults.get('terminal_string', kwargs, 0), "Terminal String"))


class OutputTerminalDescriptor(TerminalDescriptor):
    def __init__(self, terminal_id, **kwargs):
        super(OutputTerminalDescriptor, self).__init__(DESCRIPTOR_SUBTYPE.VC_OUTPUT_TERMINAL, terminal_id)

        self.append(UInt16Formatter(defaults.get('output_terminal_type', kwargs, TERMINAL_TYPE.OTT_VENDOR_SPECIFIC), "Output terminal type"))
        self.append(UInt8Formatter(defaults.get('associated_terminal_id', kwargs, 0), "Associated Terminal ID"))
        self.append(UInt8Formatter(defaults.get('source_id', kwargs, 0), "Source ID"))
        self.append(UInt8Formatter(defaults.get('terminal_string', kwargs, 0), "Terminal String"))
