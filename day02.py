from typing import Iterable


TEST_INPUT = """forward 5
down 5
forward 8
up 3
down 8
forward 2""".splitlines()


def part_one(puzzle_input: Iterable[str]) -> int:
    x = 0
    y = 0
    for line in puzzle_input:
        direction, str_amount = line.split()
        amount = int(str_amount.strip())
        if direction == "forward":
            x += amount
        elif direction == "down":
            y += amount
        elif direction == "up":
            y -= amount
        else:
            raise ValueError(f"unknown instruction {line}")
    return x * y


def part_two(puzzle_input: Iterable[str]) -> int:
    x = 0
    y = 0
    aim = 0
    for line in puzzle_input:
        direction, str_amount = line.split()
        amount = int(str_amount.strip())
        if direction == "forward":
            y += aim * amount
            x += amount
        elif direction == "down":
            aim += amount
        elif direction == "up":
            aim -= amount
        else:
            raise ValueError(f"unknown instruction {line}")
    return x * y


def main():
    part_one_result = part_one(TEST_INPUT)
    assert part_one_result == 150, part_one_result
    part_two_result = part_two(TEST_INPUT)
    assert part_two_result == 900, part_two_result
    with open("day02.txt") as infile:
        puzzle_input = [line.strip() for line in infile]
    print(part_one(puzzle_input))
    print(part_two(puzzle_input))


if __name__ == "__main__":
    main()
