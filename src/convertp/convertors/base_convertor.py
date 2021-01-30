class BaseConvertor:
    def __init__(self, src_path: str, dst_path: str, frame_rate=44100, sample_width=2, n_channels=2):
        self.src_path = src_path
        self.dst_path = dst_path

        self.n_channels = n_channels
        self.sample_width = sample_width
        self.frame_rate = frame_rate

    def convert(self) -> None:
        """
        Converts raw audio data into a specific file type.
        """
        raise NotImplementedError
