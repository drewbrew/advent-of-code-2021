from typing import Iterable

TEST_INPUT = """199
200
208
210
200
207
240
269
260
263""".splitlines()


def parse_input(input_text: Iterable[str]) -> list[int]:
    return [int(i.strip()) for i in input_text]


def part_one(puzzle_input: list[int]) -> int:
    zipped = zip(puzzle_input[:-1], puzzle_input[1:])
    return sum(b > a for a, b in zipped)


def part_two(puzzle_input: list[int]) -> int:
    index_range = range(4, len(puzzle_input) + 1)
    return sum(
        # so first comparison is sum([199, 200, 208]) < sum([200, 208, 210])
        sum(puzzle_input[index - 4 : index - 1]) < sum(puzzle_input[index - 3 : index])
        for index in index_range
    )


def main():
    assert part_one(parse_input(TEST_INPUT)) == 7, part_one(parse_input(TEST_INPUT))
    with open("day01.txt") as infile:
        real_input = parse_input(infile)
    print(part_one(real_input))
    assert part_two(parse_input(TEST_INPUT)) == 5
    print(part_two(real_input))


if __name__ == "__main__":
    main()
