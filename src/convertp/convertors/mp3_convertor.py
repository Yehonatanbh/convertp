from pydub import AudioSegment

from .base_convertor import BaseConvertor

FILE_EXTENTION = 'mp3'
FILE_FORMAT = 'mp3'


class MP3Convertor(BaseConvertor):
    def convert(self):
        raw_audio = AudioSegment.from_file(self.src_path, format="raw", frame_rate=self.frame_rate,
                                           channels=self.n_channels, sample_width=self.sample_width)
        raw_audio.export(f'{self.dst_path}.{FILE_EXTENTION}', format=FILE_FORMAT)
