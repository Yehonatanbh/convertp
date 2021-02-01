import os
from itertools import islice
from tempfile import gettempdir

from .rtp_sniffer import RTPSniffer
from .saver import Saver
from .rtp_utils import detect_payload_type, strip_rtp_header, get_audio_ssrc
from .loaders.type_to_loader import get_loader


class ConveRTP:
    def __init__(self, dst_path, pcap_path=None, from_video=False):
        self.from_video = from_video

        self.dst_path = dst_path
        self._tmp_raw_file = os.path.join(gettempdir(), 'temp_audio.raw')
        self._raw_buffer = bytes()

        self.sniffer = RTPSniffer(path=pcap_path)
        self._loader = None

        self.saver = Saver(self._tmp_raw_file)

    def setup_loader(self):
        payload_type = detect_payload_type(next(self.sniffer))
        self._loader = get_loader(payload_type)

    def convert(self):
        self.load_all_packets()
        self.write_raw()
        self.saver.save(dst_path=self.dst_path)

    def load_all_packets(self):
        if self.from_video:
            self.update_sniffer_to_point_audio_ssrc()
        self._load_all_packets_from_sniffer()

    def _load_all_packets_from_sniffer(self):
        self.setup_loader()
        # TODO: bytes().join([list comprehension])
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

    def update_sniffer_to_point_audio_ssrc(self):
        audio_ssrc = get_audio_ssrc(islice(self.sniffer, 100))
        self.sniffer.display_filter += f' and rtp.ssrc == {audio_ssrc}'
        self.sniffer.reset_capture()

