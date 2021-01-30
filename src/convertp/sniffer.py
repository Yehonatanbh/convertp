import pyshark


class Sniffer:
    def __init__(self, display_filter, path=None, interface=None):
        self._validate_input(path=path, interface=interface)
        self._from_file = bool(path)
        self._setup_capture(display_filter, interface, path)

    @staticmethod
    def _validate_input(path, interface):
        if not (path or interface):
            raise ValueError("You must specify either a path to a cap file or an interface to sniff on.")

    def __iter__(self):
        if self._from_file:
            return self._cap.__iter__()
        return self._cap.sniff_continuously()

    def __next__(self):
        return next(self.__iter__())

    def _setup_capture(self, display_filter, interface, path):
        if self._from_file:
            self._cap = self._get_file_capture(display_filter, path)
        else:
            self._cap = self._get_live_capture(display_filter, interface)

    def _get_file_capture(self, display_filter, path):
        return pyshark.FileCapture(path, display_filter=display_filter)

    def _get_live_capture(self, display_filter, interface):
        return pyshark.LiveCapture(interface=interface, display_filter=display_filter)
