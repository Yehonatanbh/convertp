from tempfile import SpooledTemporaryFile

from pydub import AudioSegment

from .base_loader import BaseLoader


class MP3Loader(BaseLoader):
    def load(self, rtp_payload):
        # The default MTU is 1500 bytes
        with SpooledTemporaryFile(max_size=1500) as temp_file:
            temp_file.write(rtp_payload)
            temp_file.seek(0)
            loaded_audio = AudioSegment.from_mp3(temp_file)
            return loaded_audio.raw_data
