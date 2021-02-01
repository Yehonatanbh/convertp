from collections import defaultdict
from statistics import mean
from typing import Iterator

import pyshark


def strip_rtp_header(packet: pyshark.packet.packet.Packet) -> bytes:
    return packet.rtp.payload.binary_value


def detect_payload_type(packet: pyshark.packet.packet.Packet) -> int:
    return int(packet.rtp.p_type)


def get_ssrc_to_length(rtp_packet_generator: Iterator[pyshark.packet.packet.Packet]):
    ssrc_to_packet_length = defaultdict(list)
    for packet in rtp_packet_generator:
        ssrc_to_packet_length[packet.rtp.ssrc].append(int(packet.captured_length))
    return ssrc_to_packet_length


def get_avg_length_to_ssrc(ssrc_to_packet_length):
    return {mean(packet_lengthes): ssrc for ssrc, packet_lengthes in ssrc_to_packet_length.items()}


def get_audio_ssrc(rtp_packet_generator: Iterator[pyshark.packet.packet.Packet]):
    ssrc_to_packet_length = get_ssrc_to_length(rtp_packet_generator)
    avg_length_to_ssrc = get_avg_length_to_ssrc(ssrc_to_packet_length)
    return avg_length_to_ssrc[min(avg_length_to_ssrc.keys())]