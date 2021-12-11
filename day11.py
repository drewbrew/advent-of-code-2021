from typing import Iterable


TEST_INPUT = """5483143223
2745854711
5264556173
6141336146
6357385478
4167524645
2176841721
6882881134
4846848554
5283751526""".splitlines()


def parse_input(puzzle: Iterable[str]) -> dict[tuple[int, int], int]:
    grid = {}
    for y, row in enumerate(puzzle):
        for x, char in enumerate(row):
            grid[x, y] = int(char)

    return grid


def flash_spot(
    grid: dict[tuple[int, int], int],
    pos: tuple[int, int],
    flashed: set[tuple[int, int]],
) -> None:
    if grid[pos] > 9 and pos not in flashed:
        flashed.add(pos)
        x, y = pos
        neighbors = [
            (x + 1, y + 1),
            (x + 1, y),
            (x + 1, y - 1),
            (x, y + 1),
            (x, y - 1),
            (x - 1, y + 1),
            (x - 1, y),
            (x - 1, y - 1),
        ]
        for dx, dy in neighbors:
            try:
                energy = grid[dx, dy]
            except KeyError:
                continue
            energy += 1
            grid[dx, dy] = energy
            if energy > 9:
                flash_spot(grid, (dx, dy), flashed)


def execute_flash(
    grid: dict[tuple[int, int], int]
) -> tuple[dict[tuple[int, int], int], int]:
    flashed = set()
    grid = {pos: value + 1 for pos, value in grid.items()}
    for pos in [pos for pos, value in grid.items() if value > 9]:
        flash_spot(grid, pos, flashed)
    grid = {pos: value if value < 10 else 0 for pos, value in grid.items()}
    return grid, len(flashed)


def part_one(puzzle_input: Iterable[str], iterations: int = 100) -> int:
    flashed_total = 0
    grid = parse_input(puzzle_input)
    for _ in range(iterations):
        grid, flashed = execute_flash(grid)
        flashed_total += flashed
    return flashed_total


def part_two(puzzle_input: Iterable[str]) -> int:
    iterations = 0
    grid = parse_input(puzzle_input)
    while any(grid.values()):
        grid, _ = execute_flash(grid)
        iterations += 1
    return iterations


def main():
    part_one_result = part_one(TEST_INPUT)
    assert part_one_result == 1656, part_one_result
    part_two_result = part_two(TEST_INPUT)
    assert part_two_result == 195, part_two_result
    with open("day11.txt") as infile:
        puzzle = [line.strip() for line in infile]
    print(part_one(puzzle))
    print(part_two(puzzle))


if __name__ == "__main__":
    main()
