from tests.fixtures import work_dir
from convertp import ConveRTP
from os import path
import pytest
from pydub import AudioSegment

MP3_PCAP = r'..\resources\pcaps\zot_ani.pcapng'
MP4_PCAP = r'..\resources\pcaps\englishman_in_new_york_video.pcapng'


def assert_file_format(file_path, _format):
    # Exception will be raised if the file is not there or if it's corrupted.
    AudioSegment.from_file(file=file_path, format=_format)


@pytest.mark.parametrize(
    'output_format',
    ['mp3', 'wav', 'ogg']
)
@pytest.mark.parametrize(
    'pcap_path,from_video',
    [(MP3_PCAP, False), (MP4_PCAP, True)]
)
def test_convertp(work_dir, pcap_path, output_format, from_video):
    exported = path.join(work_dir, f'exported.{output_format}')
    convertor = ConveRTP(dst_file=exported, pcap_path=pcap_path, from_video=from_video)
    convertor.convert()
    assert_file_format(exported, output_format)
