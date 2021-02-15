from collections import defaultdict
from statistics import mean
from typing import Iterator, Dict, List

import pyshark


def strip_rtp_header(packet: pyshark.packet.packet.Packet) -> bytes:
    """
    Extracts the payload of a given packet.
    """
    return packet.rtp.payload.binary_value


def detect_payload_type(packet: pyshark.packet.packet.Packet) -> int:
    """
    Returns the integer represents the payload type of the given RTP packet.
    for more information about payload types, please refer to https://en.wikipedia.org/wiki/RTP_payload_formats.
    """
    return int(packet.rtp.p_type)


def get_ssrc_to_length(rtp_packet_iterator: Iterator[pyshark.packet.packet.Packet]) -> Dict[str, List[int]]:
    """
    Maps between ssrc to lengths of packets.
    """
    ssrc_to_packet_length = defaultdict(list)
    for packet in rtp_packet_iterator:
        ssrc_to_packet_length[packet.rtp.ssrc].append(int(packet.captured_length))
    return ssrc_to_packet_length


def get_avg_length_to_ssrc(ssrc_to_packet_length: Dict[str, List[int]]) -> Dict[float, str]:
    """
    Calculates the average packet length of each ssrc.
    :param ssrc_to_packet_length: Mapping between ssrc to lengths of packets.
    :return: Mapping between average packet length to ssrc
    """
    return {
        mean(packet_lengthes): ssrc
        for ssrc, packet_lengthes in ssrc_to_packet_length.items()
    }


def get_audio_ssrc(rtp_packet_generator: Iterator[pyshark.packet.packet.Packet]) -> str:
    """
    Reads all the packets in the iterator given, and maps each ssrc to its average packet length.
    Then returns the ssrc Whom his average is lower.
    :return: the audio ssrc
    """
    ssrc_to_packet_length = get_ssrc_to_length(rtp_packet_generator)
    avg_length_to_ssrc = get_avg_length_to_ssrc(ssrc_to_packet_length)
    return avg_length_to_ssrc[min(avg_length_to_ssrc.keys())]
