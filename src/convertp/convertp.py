import os
from tempfile import gettempdir

from .sniffer import Sniffer
from .saver import Saver
from .rtp_utils import detect_payload_type, strip_rtp_header
from .loaders.type_to_loader import get_loader


class ConveRTP:
    def __init__(self, dst_path, pcap_path=None):
        self.dst_path = dst_path
        self._tmp_raw_file = os.path.join(gettempdir(), 'temp_audio.raw')
        self._raw_buffer = bytes()

        self.sniffer = Sniffer(display_filter='rtp.payload', path=pcap_path)
        payload_type = detect_payload_type(next(self.sniffer))
        self._loader = get_loader(payload_type)

        self.saver = Saver(self._tmp_raw_file)

    def convert(self):
        self.load_all_packets()
        self.write_raw()
        self.saver.save(dst_path=self.dst_path)

    def load_all_packets(self):
        payloads = bytes()
        for packet in self.sniffer:
            payloads += strip_rtp_header(packet)
        if payloads:
            self._raw_buffer += self._loader.load(payloads)

    def write_raw(self):
        if not self._raw_buffer:
            return False
        with open(self._tmp_raw_file, 'wb') as f:
            f.write(self._raw_buffer)
