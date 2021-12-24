"""Day 24: finally, some assembly required"""
from day24_decompiled import (
    step_1,
    step_2,
    step_3,
    step_4,
    step_5,
    step_6,
    step_7,
    step_8,
    step_9,
    step_10,
    step_11,
    step_12,
    step_13,
    step_14,
)


def part_one_alt() -> int:
    digits = list(range(1, 10))
    states_seen = {(1, step_1(0, 0, 0, 0, digit)): digit for digit in digits}
    for digits_so_far in range(1, 14):
        print(f"checking digit {digits_so_far + 1} ({len(states_seen)} overall)")
        next_func = {
            1: step_2,
            2: step_3,
            3: step_4,
            4: step_5,
            5: step_6,
            6: step_7,
            7: step_8,
            8: step_9,
            9: step_10,
            10: step_11,
            11: step_12,
            12: step_13,
            13: step_14,
        }[digits_so_far]
        for (digits_seen, (w, x, y, z)), best_result in list(states_seen.items()):
            for next_digit in digits[:]:
                if digits_seen + 1 < digits_so_far:
                    try:
                        del states_seen[digits_seen, (w, x, y, z)]
                    except KeyError:
                        pass
                if digits_seen != digits_so_far:
                    continue
                next_result = next_func(w, x, y, z, next_digit=next_digit)
                dict_key = digits_seen + 1, next_result
                new_digits = best_result * 10 + next_digit
                try:
                    prev_best = states_seen[dict_key]
                except KeyError:
                    states_seen[dict_key] = new_digits
                else:
                    if new_digits > prev_best:
                        states_seen[dict_key] = new_digits
    candidates = (
        val
        for (digits_seen, (_, _, _, z)), val in states_seen.items()
        if digits_seen == 14 and not z
    )
    return max(candidates)


class CPU:
    def __init__(self, instructions: list[str]) -> None:
        self.registers = {
            "w": 0,
            "x": 0,
            "y": 0,
            "z": 0,
        }
        self.instructions = instructions

    def inp(self, destination_register: str, value: str):
        assert destination_register in "wxyz"
        self.registers[destination_register] = int(value)

    def add(self, a: str, b: str):
        assert a in "wxyz"

        if b in "wxyz":
            self.registers[a] += self.registers[b]
        else:
            self.registers[a] += int(b)

    def mul(self, a: str, b: str):
        assert a in "wxyz"

        if b in "wxyz":
            self.registers[a] *= self.registers[b]
        else:
            self.registers[a] *= int(b)

    def div(self, a: str, b: str):
        assert a in "wxyz"

        if b in "wxyz":
            self.registers[a] //= self.registers[b]
        else:
            self.registers[a] //= int(b)

    def mod(self, a: str, b: str):
        assert a in "wxyz"

        if self.registers[a] < 0:
            raise InvalidModError()
        if b in "wxyz":
            if self.registers[b] <= 0:
                raise InvalidModError()
            self.registers[a] %= self.registers[b]
        else:
            if int(b) <= 0:
                raise InvalidModError()
            self.registers[a] %= int(b)

    def eql(self, a: str, b: str):
        assert a in "wxyz"
        if b in "wxyz":
            self.registers[a] = int(self.registers[a] == self.registers[b])
        else:
            self.registers[a] = int(self.registers[a] == int(b))

    def run_p1(self) -> bool:
        input_digits = list("123456789")
        reg_states_seen = {((1, x + 6, x + 6, 1), 1): x for x in range(1, 10)}
        offsets = {
            1: 18,
            2: 36,
            3: 54,
            4: 72,
            5: 90,
            6: 109,
            7: 126,
            8: 144,
            9: 162,
            10: 180,
            11: 198,
            12: 216,
            13: 234,
        }

        for max_digits, instruction_start in offsets.items():
            print(f"checking digit {max_digits + 1} ({len(reg_states_seen)} overall)")
            if max_digits < 3:
                print(reg_states_seen)

            for ones_digit in input_digits:
                for (registers, digits_so_far), model_number in list(
                    reg_states_seen.items()
                ):
                    if digits_so_far < max_digits:
                        # clean up old stuff
                        try:
                            del reg_states_seen[(registers, digits_so_far)]
                        except KeyError:
                            continue
                        continue
                    if digits_so_far != max_digits:
                        continue
                    self.registers = {
                        "w": registers[0],
                        "x": registers[1],
                        "y": registers[2],
                        "z": registers[3],
                    }
                    input_count = 0

                    for instruction in self.instructions[instruction_start:]:
                        func = {
                            "inp": self.inp,
                            "add": self.add,
                            "mul": self.mul,
                            "div": self.div,
                            "mod": self.mod,
                            "eql": self.eql,
                        }
                        split = instruction.split()
                        if split[0] == "inp":
                            if input_count == 1:
                                dict_key = (
                                    (
                                        self.registers["w"],
                                        self.registers["x"],
                                        self.registers["y"],
                                        self.registers["z"],
                                    ),
                                    digits_so_far + input_count,
                                )
                                new_model_number = model_number * 10 + int(ones_digit)
                                try:
                                    existing_model_number = reg_states_seen[dict_key]
                                except KeyError:
                                    reg_states_seen[dict_key] = new_model_number
                                else:
                                    if new_model_number > existing_model_number:
                                        reg_states_seen[dict_key] = new_model_number
                                break
                            self.inp(split[1], ones_digit)
                            input_count += 1
                        else:
                            func[split[0]](*split[1:])
        return max(val for key, val in reg_states_seen.items() if key[0][-1] == 0)


class InvalidModError(Exception):
    """Tried to run a modulus operation with negative numbers"""


def part_one(puzzle: list[str]) -> int:
    """Find the largest 14-digit number that is a valid model number"""
    cpu = CPU(puzzle)
    cpu.run_p1()


def main():
    print(part_one_alt())
    return
    with open("day24.txt") as infile:
        instructions = [line.strip() for line in infile]
    print(part_one(instructions))


if __name__ == "__main__":
    main()
