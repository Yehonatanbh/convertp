from typing import Type

from .base_decoder import BaseDecoder
from .mpeg_decoder import MPEGDecoder

_rtp_type_to_decoder = {
    14: MPEGDecoder,
}


def get_decoder_for_data_type(data_type: int) -> Type[BaseDecoder]:
    if data_type not in _rtp_type_to_decoder.keys():
        raise NotImplementedError(f"The payload type {data_type} is not supported yet")
    return _rtp_type_to_decoder[data_type]
