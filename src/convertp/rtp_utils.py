import pyshark


def strip_rtp_header(packet: pyshark.packet.packet.Packet) -> bytes:
    return packet.rtp.payload.binary_value


def detect_payload_type(packet: pyshark.packet.packet.Packet) -> int:
    return int(packet.rtp.p_type)
