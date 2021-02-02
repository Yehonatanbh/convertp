from pydub import AudioSegment


class Saver:
    SUPPORTED_FORMATS = ['mp3', 'wav', 'raw', 'ogg']

    def __init__(self, src_raw_file: str, frame_rate=44100, sample_width=2, n_channels=2):
        self.src_path = src_raw_file

        self.n_channels = n_channels
        self.sample_width = sample_width
        self.frame_rate = frame_rate

    def _save_as(self, dst_path: str, file_format=None) -> None:
        raw_audio = AudioSegment.from_raw(self.src_path, format="raw", frame_rate=self.frame_rate,
                                          channels=self.n_channels, sample_width=self.sample_width)
        raw_audio.export(f'{dst_path}', format=file_format)

    def save(self, dst_path: str, file_format=None):
        """
        Converts raw audio data into a specific file type and saves it on the file system.
        """
        if not file_format:
            file_format = self.get_format_from_path(dst_path)
        self.validate_file_format(file_format)
        if not dst_path.endswith(f'.{file_format}'):
            dst_path += f'.{file_format}'
        return self._save_as(dst_path, file_format)

    @classmethod
    def get_format_from_path(cls, file_path):
        """
        Returns the file extension of a given file.
        :param file_path:
        :rtype: str
        """
        splitted_path = file_path.split('.')
        if len(splitted_path) <= 1:
            raise ValueError("No file format was specified, and no file extension was found.")
        file_format = splitted_path[-1]
        return file_format

    @classmethod
    def validate_file_format(cls, file_format):
        """
        Validates that the given file fotmat iS supported.
        """
        if file_format not in cls.SUPPORTED_FORMATS:
            raise ValueError(f'The format {file_format} is not supported yet.')
