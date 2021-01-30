import os
from tempfile import gettempdir

from .sniffer import Sniffer
from .saver import Saver
from .rtp_utils import detect_payload_type, strip_rtp_header
from .loaders.type_to_loader import get_loader


class ConveRTP:
    # The amount of packet to buffer together before decoding it as mp3
    packet_buffer_size = 50

    def __init__(self, dst_path, pcap_path=None, interface=None):
        self.dst_path = dst_path
        self._tmp_raw_file = os.path.join(gettempdir(), 'temp_audio.raw')
        self._raw_buffer = bytes()

        self.sniffer = Sniffer(display_filter='rtp.payload', path=pcap_path, interface=interface)
        payload_type = detect_payload_type(next(self.sniffer))
        self._loader = get_loader(payload_type)

        self._setup_audio_buffer()
        self.saver = Saver(self._tmp_raw_file)

    def _setup_audio_buffer(self):
        self._audio_buffer = bytes()

    def convert(self):
        self.load_all_packets()
        self.write_raw()
        self.saver.save(dst_path=self.dst_path)

    # def get_rtp_payloads(self, amount=1):
    #     payloads_buffer = bytes()
    #     for _ in range(amount):
    #         try:
    #             packet = next(self.sniffer)
    #         except StopIteration:
    #             break
    #         payloads_buffer += strip_rtp_header(packet)
    #     return payloads_buffer

    def load_all_packets(self):
        """
        loads the next packet in the cap given, process it and return the raw audio data.
        :return:
        """
        # payloads = self.get_rtp_payloads(amount=50)
        # while payloads:
        #     self._audio_buffer += self._loader.load(payloads)
        #     payloads = self.get_rtp_payloads(amount=50)
        for packet in self.sniffer:
            self._audio_buffer += strip_rtp_header(packet)
        self._raw_buffer += self._loader.load(self._audio_buffer)

    def write_raw(self):
        if not self._raw_buffer:
            return False
        with open(self._tmp_raw_file, 'wb') as f:
            f.write(self._raw_buffer)
