from .base_loader import BaseLoader
from .mp3_loader import MP3Loader

_rtp_type_to_decoder = {
    14: MP3Loader,
}


def get_loader_from_payload_type(data_type: int) -> BaseLoader:
    """
    returns the Loader class that can handle the given file format.
    """
    if data_type not in _rtp_type_to_decoder.keys():
        raise NotImplementedError(f"The payload type {data_type} is not supported yet")
    decoder_cls = _rtp_type_to_decoder[data_type]
    return decoder_cls()
