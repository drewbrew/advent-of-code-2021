"""Day 3: binary diagnostic"""

from collections import Counter
from typing import Iterable

TEST_INPUT = """00100
11110
10110
10111
10101
01111
00111
11100
10000
11001
00010
01010""".splitlines()


def gamma_rate(puzzle: Iterable[str]) -> str:
    iterators = [list() for _ in range(len(puzzle[0]))]
    for line in puzzle:
        for index, char in enumerate(line):
            iterators[index].append(char)
    digit_counters = [Counter(group) for group in iterators]
    assert len(digit_counters) == len(puzzle[0]), digit_counters
    result = ""
    for counter in digit_counters:
        max_value = [
            key for key, _ in sorted(counter.items(), key=lambda k: k[1], reverse=True)
        ][0]
        result += max_value
    return result


def epsilon_rate(puzzle: Iterable[str]) -> str:
    iterators = [list() for _ in range(len(puzzle[0]))]
    for line in puzzle:
        for index, char in enumerate(line):
            iterators[index].append(char)
    digit_counters = [Counter(group) for group in iterators]
    assert len(digit_counters) == len(puzzle[0]), digit_counters
    result = ""
    for counter in digit_counters:
        max_value = [key for key, _ in sorted(counter.items(), key=lambda k: k[1])][0]
        result += max_value
    return result


def o2_gen_rating(puzzle: Iterable[str]) -> str:
    candidates = set(puzzle)
    value_so_far = ""
    for bit_pos in range(len(puzzle[0])):
        iterators = [list() for _ in range(len(puzzle[0]))]
        for line in candidates:
            for index, char in enumerate(line):
                iterators[index].append(char)
        digit_counters = [Counter(group) for group in iterators]

        counter = digit_counters[bit_pos]
        candidate_chars = [
            key for key, val in counter.items() if val == max(counter.values())
        ]
        if len(candidate_chars) == 1:
            char = candidate_chars[0]
        elif not candidate_chars:
            raise ValueError("huh?")
        else:
            # it's a tie. Default to 1
            char = "1"
        value_so_far += char
        candidates = set(
            candidate for candidate in candidates if candidate.startswith(value_so_far)
        )
        if len(candidates) == 1:
            return candidates.pop()
        elif not candidates:
            raise ValueError(f"this should not happen, {value_so_far}")
    raise ValueError(f"did not find a match? {value_so_far}")


def co2_scrub_rating(puzzle: Iterable[str]) -> str:
    candidates = set(puzzle)
    value_so_far = ""

    for bit_pos in range(len(puzzle[0])):
        iterators = [list() for _ in range(len(puzzle[0]))]
        for line in candidates:
            for index, char in enumerate(line):
                iterators[index].append(char)
        digit_counters = [Counter(group) for group in iterators]
        counter = digit_counters[bit_pos]
        candidate_chars = [
            key for key, val in counter.items() if val == min(counter.values())
        ]
        if len(candidate_chars) == 1:
            char = candidate_chars[0]
        elif not candidate_chars:
            raise ValueError("huh?")
        else:
            # it's a tie. Default to 0
            char = "0"
        value_so_far += char
        candidates = set(
            candidate for candidate in candidates if candidate.startswith(value_so_far)
        )
        if len(candidates) == 1:
            return candidates.pop()
        elif not candidates:
            raise ValueError(f"this should not happen, {value_so_far}")
    raise ValueError(f"did not find a match? {value_so_far}")


def part_two(puzzle: Iterable[str]) -> int:
    o2 = o2_gen_rating(puzzle)
    co2 = co2_scrub_rating(puzzle)
    return int(o2, 2) * int(co2, 2)


def part_one(puzzle: Iterable[str]) -> int:
    gamma = gamma_rate(puzzle)
    epsilon = epsilon_rate(puzzle)
    return int(gamma, 2) * int(epsilon, 2)


def main():
    assert gamma_rate(TEST_INPUT) == "10110", gamma_rate(TEST_INPUT)
    assert epsilon_rate(TEST_INPUT) == "01001", epsilon_rate(TEST_INPUT)
    assert o2_gen_rating(TEST_INPUT) == "10111", o2_gen_rating(TEST_INPUT)
    assert co2_scrub_rating(TEST_INPUT) == "01010", co2_scrub_rating(TEST_INPUT)
    with open("day03.txt") as infile:
        puzzle = [line.strip() for line in infile]

    print(part_one(puzzle))
    print(part_two(puzzle))


if __name__ == "__main__":
    main()
