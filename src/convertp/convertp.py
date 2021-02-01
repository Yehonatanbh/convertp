import os
from itertools import islice
from tempfile import gettempdir

from .rtp_sniffer import RTPSniffer
from .saver import Saver
from .rtp_utils import detect_payload_type, strip_rtp_header, get_audio_ssrc
from .loaders.type_to_loader import get_loader_from_payload_type


class ConveRTP:
    def __init__(self, dst_path, pcap_path=None, from_video=False):
        self.from_video = from_video

        self.dst_path = dst_path
        self._tmp_raw_file = os.path.join(gettempdir(), 'temp_audio.raw')
        self._raw_buffer = bytes()

        self.sniffer = self.get_sniffer(pcap_path)
        self._loader = self.get_loader()

        self.saver = Saver(self._tmp_raw_file)

    def get_sniffer(self, pcap_path):
        sniffer = RTPSniffer(path=pcap_path)
        if self.from_video:
            self.update_sniffer_to_point_audio_ssrc(sniffer)
        return sniffer

    def get_loader(self):
        payload_type = detect_payload_type(next(self.sniffer))
        return get_loader_from_payload_type(payload_type)

    def convert(self):
        self.load_all_packets()
        self.write_raw()
        self.saver.save(dst_path=self.dst_path)

    def load_all_packets(self):
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

    @classmethod
    def update_sniffer_to_point_audio_ssrc(cls, sniffer: RTPSniffer):
        audio_ssrc = get_audio_ssrc(islice(sniffer, 100))
        sniffer.display_filter += f' and rtp.ssrc == {audio_ssrc}'
        sniffer.reset_capture()
