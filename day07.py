"""Day 7: The treachery of whales"""

TEST_INPUT = "16,1,2,0,4,2,7,1,2,14"


def part_one(puzzle_input: str) -> int:
    starts = sorted([int(i) for i in puzzle_input.split(",")])
    fuel_used = 1e100
    for candidate_meeting in range(starts[0], starts[-1] + 1):
        fuel = sum(abs(candidate_meeting - pos) for pos in starts)
        if fuel < fuel_used:
            fuel_used = fuel
    return fuel_used


def part_two(puzzle_input: str) -> int:
    starts = sorted([int(i) for i in puzzle_input.split(",")])
    fuel_used = 1e100
    for candidate_meeting in range(starts[0], starts[-1] + 1):
        # sum of all values from 1 to n, inclusive is n * (n + 1) / 2 or (n**2 + n) / 2
        fuel = sum(
            (abs(candidate_meeting - pos) ** 2 + abs(candidate_meeting - pos)) / 2
            for pos in starts
        )
        if fuel < fuel_used:
            fuel_used = fuel
    return int(fuel_used)


def main():
    assert part_one(TEST_INPUT) == 37, part_one(TEST_INPUT)
    assert part_two(TEST_INPUT) == 168, part_two(TEST_INPUT)
    with open("day07.txt") as infile:
        puzzle = infile.read().strip()
    print(part_one(puzzle))
    print(part_two(puzzle))


if __name__ == "__main__":
    main()
