from .convertors.mp3_convertor import MP3Convertor
from .sniffer import Sniffer
from .rtp_handler import detect_payload_type, strip_rtp_header
from .decoders.type_to_decoder_map import get_decoder_for_data_type
from tempfile import gettempdir
import os


class ConveRTP:
    def __init__(self, dst_path, src_path=None, interface=None):
        self.dst_path = dst_path
        self._tmp_raw_file = os.path.join(gettempdir(), 'temp_audio.raw')

        self.sniffer = Sniffer(display_filter='rtp.payload',
                               path=src_path,
                               interface=interface)
        self.convertor = MP3Convertor(src_path=self._tmp_raw_file,
                                      dst_path=dst_path)
        payload_type = detect_payload_type(next(self.sniffer))
        self.decoder = get_decoder_for_data_type(payload_type)()

    def convert(self):
        self._write_raw()
        self.convertor.convert()

    def _write_raw(self):
        raw_audio_packets = [self.decoder.decode(strip_rtp_header(packet)) for packet in self.sniffer]
        raw_audio = bytes().join(raw_audio_packets)
        with open(self._tmp_raw_file, 'wb') as f:
            f.write(raw_audio)
