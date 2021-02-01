import os
from itertools import islice
from tempfile import gettempdir

from .rtp_pcap_reader import RTPPcapReader
from .saver import Saver
from .rtp_utils import detect_payload_type, strip_rtp_header, get_audio_ssrc
from .windows_utils import get_pcap_file_windows
from .loaders.type_to_loader import get_loader_from_payload_type


class ConveRTP:
    def __init__(self, dst_file, pcap_path=None, from_video=False):
        self.from_video = from_video

        self.dst_path = dst_file
        self._tmp_raw_file = os.path.join(gettempdir(), 'convertp_temp_audio.raw')
        self._raw_buffer = bytes()

        pcap_path = pcap_path or get_pcap_file_windows()
        self.pcap_reader = self.get_pcap_reader(pcap_path)
        self._loader = self.get_loader()

        self.saver = Saver(self._tmp_raw_file)

    def get_pcap_reader(self, pcap_path):
        pcap_reader = RTPPcapReader(path=pcap_path)
        if self.from_video:
            self.update_reader_to_point_audio_ssrc(pcap_reader)
        return pcap_reader

    def get_loader(self):
        payload_type = detect_payload_type(next(self.pcap_reader))
        return get_loader_from_payload_type(payload_type)

    def convert(self):
        self.load_all_packets()
        self.write_raw()
        self.saver.save(dst_path=self.dst_path)

    def load_all_packets(self):
        payloads = bytes().join([strip_rtp_header(packet) for packet in self.pcap_reader])
        if payloads:
            self._raw_buffer += self._loader.load(payloads)
        else:
            raise ValueError('No packets found :(')

    def write_raw(self):
        if not self._raw_buffer:
            return False
        with open(self._tmp_raw_file, 'wb') as f:
            f.write(self._raw_buffer)

    @classmethod
    def update_reader_to_point_audio_ssrc(cls, pcap_reader: RTPPcapReader):
        audio_ssrc = get_audio_ssrc(islice(pcap_reader, 100))
        pcap_reader.display_filter += f' and rtp.ssrc == {audio_ssrc}'
        pcap_reader.reset_capture()
