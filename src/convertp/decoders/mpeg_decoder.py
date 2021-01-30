from .base_decoder import BaseDecoder

MPEG_HEADER_SIZE = 4  # bytes


class MPEGDecoder(BaseDecoder):
    def decode(self, rtp_payload):
        return rtp_payload[MPEG_HEADER_SIZE:]
