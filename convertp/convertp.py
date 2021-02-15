import os
from itertools import islice
from tempfile import gettempdir

from convertp.rtp_pcap_reader import RTPPcapReader
from convertp.saver import Saver
from convertp.rtp_utils import detect_payload_type, strip_rtp_header, get_audio_ssrc
from convertp.windows_utils import get_pcap_file_windows
from convertp.loaders import get_loader_from_payload_type


class ConveRTP:
    """
    Convert RTP streams to playable audio files.

    Example:
        convertor = ConveRTP(dst_file='my_song.mp3', pcap_path='/path/to/my/sniff.pcap')
        convertor.convert()

    The supported file types are .mp3, .wav, .ogg and .raw.
    """

    def __init__(self, dst_file, pcap_path=None, from_video=False):
        """
        :param dst_file: Path to the file that the audio will be exported to after running convert().
        :type dst_file: str
        :param pcap_path: Path to the sniffeed packets file. Must be with either .pcap or .pcapng extension.
        :type pcap_path: str
        :param from_video: Weather the sniffed data was video or plane audio.
        :type from_video: bool
        """
        self.from_video = from_video

        self.dst_path = dst_file
        self._tmp_raw_file = os.path.join(gettempdir(), 'convertp_temp_audio.raw')
        self._raw_buffer = bytes()

        pcap_path = pcap_path or get_pcap_file_windows()
        self.pcap_reader = self.get_pcap_reader(pcap_path)
        self._loader = self.get_loader()

        self.saver = Saver(self._tmp_raw_file)

    def convert(self):
        """
        Perform the actual conversion.
        """
        self.load_all_packets()
        self.write_raw()
        self.saver.save(dst_path=self.dst_path)

    def get_pcap_reader(self, pcap_path):
        """
        Initialize an RTPPcapReader object, with the given `pcap_path`.
        In case of a video sniff, sets up the object's display filter to get only the audio rtp packets.

        :param pcap_path: Path to pcap file
        :type pcap_path: str
        :rtype: RTPPcapReader
        """
        pcap_reader = RTPPcapReader(path=pcap_path)
        if self.from_video:
            self.update_reader_to_point_audio_ssrc(pcap_reader)
        return pcap_reader

    def get_loader(self):
        """
        Detects the payload type in the rtp stream, and returns a proper Loader.
        :rtype: loaders.BaseLoader
        """
        payload_type = detect_payload_type(next(self.pcap_reader))
        return get_loader_from_payload_type(payload_type)

    def load_all_packets(self):
        """
        strip all the RTP headers, loads the data from the pcap files, and saves the raw data to a buffer.
        """
        payloads = bytes().join([strip_rtp_header(packet) for packet in self.pcap_reader])
        if payloads:
            self._raw_buffer += self._loader.load(payloads)
        else:
            raise ValueError('No packets found :(')

    def write_raw(self):
        """
        Writes the data in the buffer to a temp file in the file system.
        """
        if not self._raw_buffer:
            return False
        with open(self._tmp_raw_file, 'wb') as f:
            f.write(self._raw_buffer)

    @classmethod
    def update_reader_to_point_audio_ssrc(cls, pcap_reader: RTPPcapReader):
        """"
        Finds the audio ssrc, based on the first 100 packets, and updates the pcap_reader to filter out everything else.
        """
        audio_ssrc = get_audio_ssrc(islice(pcap_reader, 100))
        pcap_reader.display_filter += f' and rtp.ssrc == {audio_ssrc}'
        pcap_reader.reset_capture()
