class BaseDecoder:
    def decode(self, rtp_payload):
        """
        converts the data given to raw audio data
        """
        raise NotImplementedError
