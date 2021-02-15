from typing import Iterator

import pyshark


class RTPPcapReader:
    """
    Filter rtp packets from a pcap file or from a live sniff.
    """
    def __init__(self, display_filter='rtp.payload', path=None, interface=None):
        self._validate_input(path=path, interface=interface)
        self._from_file = bool(path)

        self.display_filter = display_filter
        self.path = path
        self.interface = interface

        self._setup_capture()

    @staticmethod
    def _validate_input(path, interface):
        """
        Validates that the user specify either path or interface.
        """
        if not (path or interface):
            raise ValueError("You must specify either a path to a cap file or an interface to sniff on.")

    def __iter__(self):
        """
        :rtype: Iterator[pyshark.packet.packet.Packet]
        """
        iterator = self._cap.__iter__() if self._from_file else self._cap.sniff_continuously()
        for packet in iterator:
            # For some reason the display_filter includes more packets than it needs.
            if hasattr(packet, "rtp") and hasattr(packet.rtp, "payload") and hasattr(packet.rtp, "ssrc"):
                yield packet

    def __next__(self):
        return next(self.__iter__())

    def reset_capture(self):
        """
        Resets the capture.
        Ignores all the data captured, or seeks to the start of the pcap file.
        """
        self._setup_capture()

    def _setup_capture(self):
        self._cap = self._get_file_capture() if self._from_file else self._get_live_capture()

    def _get_file_capture(self):
        return pyshark.FileCapture(self.path, display_filter=self.display_filter)

    def _get_live_capture(self):
        return pyshark.LiveCapture(interface=self.interface, display_filter=self.display_filter)
