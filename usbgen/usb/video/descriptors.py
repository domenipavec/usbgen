import math

from .constants import DESCRIPTOR_SUBTYPE, TERMINAL_TYPE, FORMAT_GUID

from usbgen.usb import DescriptorWithChildren, Descriptor, DESCRIPTOR_TYPE
from usbgen.usb.formatters import UInt8Formatter, UInt16Formatter, UInt32Formatter, BCD16Formatter, BitMapFormatter, GUIDFormatter
from usbgen.usb.defaults import defaults


class VideoClassControlInterfaceDescriptor(DescriptorWithChildren):
    def __init__(self, *children, **kwargs):
        super(VideoClassControlInterfaceDescriptor, self).__init__(DESCRIPTOR_TYPE.CLASS_SPECIFIC_INTERFACE, *children)

        self.append(UInt8Formatter(DESCRIPTOR_SUBTYPE.VC_HEADER, "Descriptor Sub-type"))

        self.append(BCD16Formatter(defaults.get('video_class_specification', kwargs, 1.5), "Video class specification"))

        self.append(self._size_formatter)

        self.append(UInt32Formatter(defaults.get('clock_frequency', kwargs, 48000000), "Video class specification"))

        video_streaming_interfaces = defaults.get('video_streaming_interfaces', kwargs, [])

        self.append(UInt8Formatter(len(video_streaming_interfaces), "Number of video streaming interfaces"))
        for i, video_streaming_interface in enumerate(video_streaming_interfaces):
            self.append(UInt8Formatter(video_streaming_interface, "Number of {}-th video streaming interface".format(i+1)))


class VideoClassStreamInInterfaceDescriptor(DescriptorWithChildren):
    def __init__(self, *children, **kwargs):
        super(VideoClassStreamInInterfaceDescriptor, self).__init__(DESCRIPTOR_TYPE.CLASS_SPECIFIC_INTERFACE, *children)

        self.append(UInt8Formatter(DESCRIPTOR_SUBTYPE.VS_INPUT_HEADER, "Descriptor Sub-type"))

        self.append(self._number_formatter)
        self.append(self._size_formatter)

        endpoint_number = defaults.get('video_data_endpoint', kwargs, 0)
        self.append(BitMapFormatter(
            1,
            BitMapFormatter.uint_parse(4, endpoint_number) +
            [
                0, 0, 0,
                1,
            ],
            "Video Data Endpoint"
        ))

        self.append(BitMapFormatter(
            1,
            [
                defaults.get('dynamic_format_change', kwargs, False),
            ],
            "Video Streaming Interface Capabilities"
        ))

        self.append(UInt8Formatter(defaults.get('output_terminal_id', kwargs, 0), "Output Terminal ID"))
        self.append(UInt8Formatter(defaults.get('still_capture_method', kwargs, 0), "Still Capture Method"))
        self.append(UInt8Formatter(defaults.get('trigger_support', kwargs, 0), "Trigger Support"))
        self.append(UInt8Formatter(defaults.get('trigger_usage', kwargs, 0), "Trigger Usage"))
        self.append(UInt8Formatter(1, "Control Size"))

        for i, child in enumerate(children):
            self.append(BitMapFormatter(
                1,
                [
                    child.key_frame_rate,
                    child.p_frame_rate,
                    child.comp_quality,
                    child.comp_window_size,
                    child.generate_key_frame,
                    child.update_frame_segment,
                ],
                "BMA Controls {}".format(i+1)
            ))


class VideoClassInterruptEndpointDescriptor(Descriptor):
    def __init__(self, **kwargs):
        super(VideoClassInterruptEndpointDescriptor, self).__init__(DESCRIPTOR_TYPE.CLASS_SPECIFIC_ENDPOINT)

        self.append(UInt8Formatter(DESCRIPTOR_SUBTYPE.EP_INTERRUPT, "Descriptor Sub-type"))
        self.append(UInt16Formatter(defaults.get('max_packet_size', kwargs, 0), "Max packet size"))


class TerminalDescriptor(Descriptor):
    def __init__(self, subtype, terminal_id):
        super(TerminalDescriptor, self).__init__(DESCRIPTOR_TYPE.CLASS_SPECIFIC_INTERFACE)

        self.append(UInt8Formatter(subtype, "Descriptor Sub-type"))

        self.append(UInt8Formatter(terminal_id, "Terminal ID"))


class InputTerminalDescriptor(TerminalDescriptor):
    def __init__(self, terminal_id, **kwargs):
        super(InputTerminalDescriptor, self).__init__(DESCRIPTOR_SUBTYPE.VC_INPUT_TERMINAL, terminal_id)

        self.append(UInt16Formatter(defaults.get('input_terminal_type', kwargs, TERMINAL_TYPE.ITT_VENDOR_SPECIFIC), "Input terminal type"))
        self.append(UInt8Formatter(defaults.get('associated_terminal_id', kwargs, 0), "Associated Terminal ID"))
        self.append(UInt8Formatter(defaults.get('terminal_string', kwargs, 0), "Terminal String"))


class CameraTerminalDescriptor(InputTerminalDescriptor):
    def __init__(self, terminal_id, **kwargs):
        super(CameraTerminalDescriptor, self).__init__(terminal_id, input_terminal_type=TERMINAL_TYPE.ITT_CAMERA, **kwargs)

        self.append(UInt16Formatter(defaults.get('objective_focal_length_min', kwargs, 0), "Objective Focal Length Min"))
        self.append(UInt16Formatter(defaults.get('objective_focal_length_max', kwargs, 0), "Objective Focal Length Max"))
        self.append(UInt16Formatter(defaults.get('occular_focal_length', kwargs, 0), "Occular Focal Length"))

        self.append(UInt8Formatter(3, "Size of Controls"))

        self.append(BitMapFormatter(
            3,
            [
                defaults.get('scanning_mode', kwargs, False),
                defaults.get('auto_exposure_mode', kwargs, False),
                defaults.get('exposure_time_absolute', kwargs, False),
                defaults.get('exposure_time_relative', kwargs, False),
                defaults.get('focus_absolute', kwargs, False),
                defaults.get('focus_relative', kwargs, False),
                defaults.get('iris_absolute', kwargs, False),
                defaults.get('iris_relative', kwargs, False),
                defaults.get('zoom_absolute', kwargs, False),
                defaults.get('zoom_relative', kwargs, False),
                defaults.get('pan_tilt_absolute', kwargs, False),
                defaults.get('pan_tilt_relative', kwargs, False),
                defaults.get('roll_absolute', kwargs, False),
                defaults.get('roll_relative', kwargs, False),
                0, 0,
                defaults.get('focus_auto', kwargs, False),
                defaults.get('privacy', kwargs, False),
                defaults.get('focus_simple', kwargs, False),
                defaults.get('window', kwargs, False),
                defaults.get('region_of_interest', kwargs, False),
            ],
            "Controls"
        ))


class OutputTerminalDescriptor(TerminalDescriptor):
    def __init__(self, terminal_id, **kwargs):
        super(OutputTerminalDescriptor, self).__init__(DESCRIPTOR_SUBTYPE.VC_OUTPUT_TERMINAL, terminal_id)

        self.append(UInt16Formatter(defaults.get('output_terminal_type', kwargs, TERMINAL_TYPE.OTT_VENDOR_SPECIFIC), "Output terminal type"))
        self.append(UInt8Formatter(defaults.get('associated_terminal_id', kwargs, 0), "Associated Terminal ID"))
        self.append(UInt8Formatter(defaults.get('source_id', kwargs, 0), "Source ID"))
        self.append(UInt8Formatter(defaults.get('terminal_string', kwargs, 0), "Terminal String"))


class UncompressedVideoFormatDescriptor(DescriptorWithChildren):
    def __init__(self, *children, **kwargs):
        super(UncompressedVideoFormatDescriptor, self).__init__(DESCRIPTOR_TYPE.CLASS_SPECIFIC_INTERFACE)

        self.key_frame_rate = defaults.get('key_frame_rate', kwargs, False)
        self.p_frame_rate = defaults.get('p_frame_rate', kwargs, False)
        self.comp_quality = defaults.get('comp_quality', kwargs, False)
        self.comp_window_size = defaults.get('comp_window_size', kwargs, False)
        self.generate_key_frame = defaults.get('generate_key_frame', kwargs, False)
        self.update_frame_segment = defaults.get('update_frame_segment', kwargs, False)

        self.append(UInt8Formatter(DESCRIPTOR_SUBTYPE.VS_FORMAT_UNCOMPRESSED, "Descriptor Sub-type"))

        self.append(UInt8Formatter(defaults.get('format_index', kwargs, 0), "Format Index"))

        self.append(self._number_formatter)

        self.append(GUIDFormatter(defaults.get('format_guid', kwargs, FORMAT_GUID.YUY2), "Format GUID"))

        bits_per_pixel = defaults.get('bits_per_pixel', kwargs, 0)
        self.append(UInt8Formatter(bits_per_pixel, "Bits Per Pixel"))
        self.append(UInt8Formatter(defaults.get('default_frame_index', kwargs, 0), "Default Frame Index"))
        self.append(UInt8Formatter(defaults.get('aspect_ratio_x', kwargs, 0), "Aspect Ratio X"))
        self.append(UInt8Formatter(defaults.get('aspect_ratio_y', kwargs, 0), "Aspect Ratio Y"))
        self.append(BitMapFormatter(
            1,
            [
                defaults.get('interlaced', kwargs, False),
                defaults.get('fields_per_frame', kwargs, False),
                defaults.get('field_1_first', kwargs, False),
                0,
            ] +
            BitMapFormatter.uint_parse(2, defaults.get('field_pattern', kwargs, 0)),
            "Interlace Flags"
        ))
        self.append(UInt8Formatter(defaults.get('copy_protect', kwargs, 0), "Copy Protect"))

        for child in children:
            child.set(bits_per_pixel)
            self.add(child)


class UncompressedVideoFrameDescriptor(Descriptor):
    def __init__(self, **kwargs):
        super(UncompressedVideoFrameDescriptor, self).__init__(DESCRIPTOR_TYPE.CLASS_SPECIFIC_INTERFACE)

        self.append(UInt8Formatter(DESCRIPTOR_SUBTYPE.VS_FRAME_UNCOMPRESSED, "Descriptor Sub-type"))

        self.append(UInt8Formatter(defaults.get('frame_index', kwargs, 0), "Frame Index"))

        self.append(BitMapFormatter(
            1,
            [
                defaults.get('still_image_supported', kwargs, False),
                defaults.get('fixed_frame_rate', kwargs, False),
            ],
            "Capabilities"
        ))

        self.width = defaults.get('width', kwargs, 0)
        self.height = defaults.get('height', kwargs, 0)

        self.min_frame_interval = defaults.get('min_frame_interval', kwargs, None)
        self.max_frame_interval = defaults.get('max_frame_interval', kwargs, None)
        self.frame_interval_step = defaults.get('frame_interval_step', kwargs, None)

        from_frame_rates = [int(round(1e7/frame_rate)) for frame_rate in defaults.get('frame_rates', kwargs, [])]
        self.frame_intervals = defaults.get('frame_intervals', kwargs, from_frame_rates)

        if len(self.frame_intervals) > 0:
            default_default_frame_interval = self.frame_intervals[0]
        else:
            default_default_frame_interval = self.min_frame_interval

        self.default_frame_interval = defaults.get('default_frame_interval', kwargs, default_default_frame_interval)

    def set(self, bits_per_pixel):
        if len(self.frame_intervals) > 0:
            self.min_frame_interval = min(self.frame_intervals)
            self.max_frame_interval = max(self.frame_intervals)

        bits_per_frame = bits_per_pixel * self.width * self.height

        self.append(UInt16Formatter(self.width, "Width"))
        self.append(UInt16Formatter(self.height, "Height"))

        self.append(UInt32Formatter(int(math.ceil(bits_per_frame / (1e-7*self.max_frame_interval))), "Minimum bit rate"))
        self.append(UInt32Formatter(int(math.ceil(bits_per_frame / (1e-7*self.min_frame_interval))), "Maximum bit rate"))

        self.append(UInt32Formatter(int(math.ceil(bits_per_frame / 8)), "Max video Frame Buffer Size"))

        self.append(UInt32Formatter(self.default_frame_interval, "Default Frame Interval"))

        self.append(UInt8Formatter(len(self.frame_intervals), "Frame Interval Type"))

        if len(self.frame_intervals) > 0:
            for i, frame_interval in enumerate(self.frame_intervals):
                self.append(UInt32Formatter(frame_interval, "Frame Interval {}".format(i)))
        else:
            self.append(UInt32Formatter(self.min_frame_interval, "Min Frame Interval"))
            self.append(UInt32Formatter(self.max_frame_interval, "Max Frame Interval"))
            self.append(UInt32Formatter(self.frame_interval_step, "Frame Interval Step"))
