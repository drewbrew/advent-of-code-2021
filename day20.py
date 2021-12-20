"""Day 20: an infinite grid"""

from typing import Iterable


TEST_ALGO = """..#.#..#####.#.#.#.###.##.....###.##.#..###.####..#####..#....#..#..##..##
#..######.###...####..#..#####..##..#.#####...##.#.#..#.##..#.#......#.###
.######.###.####...#.##.##..#..#..#####.....#.#....###..#.##......#.....#.
.#..#..##..#...##.######.####.####.#.#...#.......#..#.#.#...####.##.#.....
.#..#...##.#.##..#...##.#.##..###.#......#.#.......#.#.#.####.###.##...#..
...####.#..#..#.##.#....##..#.####....##...##..#...#......#.#.......#.....
..##..####..#...#.#.#...##..#.#..###..#####........#..####......#..#""".replace(
    "\n", ""
)

TEST_START_IMAGE = """#..#.
#....
##..#
..#..
..###""".splitlines()

GRID_TYPE = set[tuple[int, int]]


def parse_algorithm(algorithm: str) -> set[int]:
    return {index for index, char in enumerate(algorithm) if char == "#"}


def parse_source_image(image: str) -> GRID_TYPE:
    grid = set()
    for y, row in enumerate(image):
        for x, char in enumerate(row):
            if char == "#":
                grid.add((x, y))
    return grid


def generate_image(
    grid: GRID_TYPE,
    algorithm: set[int],
    step: int,
) -> GRID_TYPE:
    # grid will expand by one in every direction each turn
    min_x = min(i[0] for i in grid)
    max_x = max(i[0] for i in grid)
    min_y = min(i[1] for i in grid)
    max_y = max(i[1] for i in grid)

    new_grid = set()
    for y in range(min_y - 1, max_y + 2):
        for x in range(min_x - 1, max_x + 2):
            image_value = 0
            for dx, dy in [
                (-1, -1),
                (0, -1),
                (1, -1),
                (-1, 0),
                (0, 0),
                (1, 0),
                (-1, 1),
                (0, 1),
                (1, 1),
            ]:
                neighbor = (x + dx, y + dy)
                in_grid = neighbor in grid

                if step % 2 and 0 in algorithm:
                    # THIS IS THE BIG TRICK
                    # if it's an odd-numbered iteration,
                    # all the stuff outside what you've already
                    # tracked will be ON if your puzzle starts with a #
                    # (I think everyone's does)
                    nx, ny = neighbor
                    if nx > max_x or nx < min_x or ny > max_y or ny < min_y:
                        in_grid = True
                image_value = (image_value * 2) + int(in_grid)
            if image_value in algorithm:
                new_grid.add((x, y))
    return new_grid


def part_one(algorithm: str, start_image: Iterable[str], iterations: int = 2) -> int:
    grid = parse_source_image(start_image)
    algo = parse_algorithm(algorithm)
    for step in range(iterations):
        grid = generate_image(
            grid,
            algo,
            step=step,
        )
        # display_grid(grid)
    return len(grid)


def display_grid(grid: GRID_TYPE):
    x_values = sorted(i[0] for i in grid)
    y_values = sorted(i[1] for i in grid)
    # grid will expand by one in every direction each turn
    min_x = x_values[0] - 1
    # +2 because of range inequality
    max_x = x_values[-1] + 2
    min_y = y_values[0] - 1
    max_y = y_values[-1] + 2
    for y in range(min_y, max_y):
        for x in range(min_x, max_x):
            print("#" if (x, y) in grid else ".", end="")
        print("")


def main():
    test_puzzle_output = part_one(TEST_ALGO, TEST_START_IMAGE)
    assert test_puzzle_output == 35, test_puzzle_output
    with open("day20.txt") as infile:
        puzzle = [line.strip() for line in infile]
    algorithm = puzzle[0]
    assert not puzzle[1]
    grid = puzzle[2:]

    print(part_one(algorithm, grid))
    print(part_one(algorithm, grid, 50))


if __name__ == "__main__":
    main()
