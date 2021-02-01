import pyshark


class RTPSniffer:
    def __init__(self, display_filter='rtp.payload', path=None, interface=None):
        self._validate_input(path=path, interface=interface)
        self._from_file = bool(path)

        self.display_filter = display_filter
        self.path = path
        self.interface = interface

        self._setup_capture()

    @staticmethod
    def _validate_input(path, interface):
        if not (path or interface):
            raise ValueError("You must specify either a path to a cap file or an interface to sniff on.")

    def __iter__(self):
        iterator = self._cap.__iter__() if self._from_file else self._cap.sniff_continuously()
        for packet in iterator:
            # for some reason the display_filter doesn't filter all the right packets
            if hasattr(packet, "rtp") and hasattr(packet.rtp, "payload") and hasattr(packet.rtp, "ssrc"):
                yield packet

    def __next__(self):
        return next(self.__iter__())

    def _setup_capture(self):
        if self._from_file:
            self._cap = self._get_file_capture(self.display_filter, self.path)
        else:
            self._cap = self._get_live_capture(self.display_filter, self.interface)

    def reset_capture(self):
        self._setup_capture()

    def _get_file_capture(self, display_filter, path):
        return pyshark.FileCapture(path, display_filter=display_filter)

    def _get_live_capture(self, display_filter, interface):
        return pyshark.LiveCapture(interface=interface, display_filter=display_filter)
