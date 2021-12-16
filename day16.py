from typing import Optional


class Packet:
    def __init__(self, data: str, mode: str = "hex") -> None:
        self.binary = ""
        self.version: int = -1
        self.packet_type: int = -1
        self.packet_is_literal_value = True
        self.literal_value: Optional[int] = None
        self.subpackets: list[Packet] = []
        self.length_is_number_of_packets = False
        self.parse_packet(data, mode)

    @property
    def packet_value(self) -> int:
        if self.packet_is_literal_value:
            result = self.literal_value
        else:
            operator_map = {
                0: self.sum,
                1: self.product,
                2: self.min,
                3: self.max,
                5: self.gt,
                6: self.lt,
                7: self.eq,
            }
            result = operator_map[self.packet_type]()
        if result is None:
            raise ValueError("oh no you forgot to return something")
        return result

    def sum(self):
        return sum(packet.packet_value for packet in self.subpackets)

    def product(self):
        result = 1
        for packet in self.subpackets:
            result *= packet.packet_value
        return result

    def min(self):
        return min(packet.packet_value for packet in self.subpackets)

    def max(self):
        return max(packet.packet_value for packet in self.subpackets)

    def gt(self):
        assert len(self.subpackets) == 2
        return int(self.subpackets[0].packet_value > self.subpackets[1].packet_value)

    def lt(self):
        assert len(self.subpackets) == 2
        return int(self.subpackets[0].packet_value < self.subpackets[1].packet_value)

    def eq(self):
        assert len(self.subpackets) == 2
        return int(self.subpackets[0].packet_value == self.subpackets[1].packet_value)

    def parse_packet(self, data: str, mode: str) -> str:
        if mode == "hex":
            self.binary = bin(int(data, 16))[2:].zfill(4 * len(data))
        elif mode == "bin":
            self.binary = data
        else:
            raise NotImplementedError()
        self.version = int(self.binary[:3], 2)
        self.packet_type = int(self.binary[3:6], 2)

        if self.packet_type == 4:
            # literal value
            self.binary = self.binary[:6] + self.parse_literal_value(self.binary[6:])
        else:
            self.packet_is_literal_value = False
            self.binary = self.binary[:6] + self.parse_operator_packet(self.binary[6:])

    def parse_literal_value(self, binary: str) -> str:
        result = ""
        for index in range(0, len(binary), 5):
            prefix = binary[index : index + 1]
            result += binary[index + 1 : index + 5]
            if prefix == "0":
                break
        else:
            raise ValueError("No breakpoint found??")
        self.literal_value = int(result, 2)
        # return the part of the packet we actually used
        return binary[: index + 5]

    def parse_operator_packet(self, binary: str) -> str:
        self.length_is_number_of_packets = bool(int(binary[0], 2))
        if not self.length_is_number_of_packets:
            # next 15 bits are the length
            packet_length = int(binary[1:16], 2)
            return binary[:16] + self.parse_subpackets(binary[16 : packet_length + 16])
        else:
            # next 11 bits are number of packets
            number_of_packets = int(binary[1:12], 2)
            return binary[:12] + self.parse_subpackets(binary[12:], number_of_packets)

    def parse_subpackets(
        self, binary: str, number_of_packets: Optional[int] = None
    ) -> str:
        result = binary
        while binary and (
            number_of_packets is None or len(self.subpackets) != number_of_packets
        ):
            if set(binary) == {"0"}:
                # nothing left to read
                break
            subpacket = Packet(binary, mode="bin")
            self.subpackets.append(subpacket)
            binary = binary[len(subpacket.binary) :]
        return result[: -len(binary) if binary else len(result)]

    @property
    def version_sum(self) -> int:
        return self.version + sum(packet.version_sum for packet in self.subpackets)


def main():
    # part 1 checks
    packet = Packet("38006F45291200")
    assert packet.version == 1
    assert packet.packet_type == 6

    packet = Packet("EE00D40C823060")
    assert packet.version == 7
    assert packet.packet_type == 3

    packet = Packet("8A004A801A8002F478")
    assert packet.version == 4
    assert packet.version_sum == 16

    packet = Packet("620080001611562C8802118E34")
    assert packet.version == 3
    assert packet.version_sum == 12

    packet = Packet("C0015000016115A2E0802F182340")
    assert packet.version_sum == 23

    packet = Packet("A0016C880162017C3686B18A3D4780")
    assert packet.version_sum == 31

    # part 2: the return of intcode
    packet = Packet("C200B40A82")
    assert packet.packet_value == 3

    packet = Packet("04005AC33890")
    assert packet.packet_value == 54

    packet = Packet("880086C3E88112")
    assert packet.packet_value == 7

    packet = Packet("CE00C43D881120")
    assert packet.packet_value == 9

    packet = Packet("D8005AC2A8F0")
    assert packet.packet_value == 1

    packet = Packet("F600BC2D8F")
    assert packet.packet_value == 0

    packet = Packet("9C005AC2F8F0")
    assert packet.packet_value == 0

    packet = Packet("9C0141080250320F1802104A08")
    assert packet.packet_value == 1

    with open("day16.txt") as infile:
        puzzle = infile.read().strip()

    packet = Packet(puzzle)
    print(packet.version_sum)
    print(packet.packet_value)


if __name__ == "__main__":
    main()
