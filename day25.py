from typing import Literal


TEST_INPUT = """v...>>.vv>
.vv>>.vv..
>>.>v>...v
>>v>>.>.v.
v>v.vv.v..
>.>>..v...
.vv..>.>v.
v.v..>>v.v
....v..v.>""".splitlines()


GRID = dict[tuple[int, int], Literal[">"] | Literal["v"]]


def parse_input(puzzle: list[str]) -> dict[tuple[int, int], GRID]:
    grid = {}
    for y, row in enumerate(puzzle):
        for x, char in enumerate(row):
            if char == ".":
                continue
            grid[x, y] = char
    return grid


def move_east(grid: GRID, x_size: int) -> GRID:
    new_grid = {(x, y): value for (x, y), value in grid.items() if value == "v"}
    for (x, y), value in grid.items():
        if value == ">":
            new_pos = (x + 1) % x_size, y
            if new_pos in grid:
                new_grid[x, y] = value
            else:
                new_grid[new_pos] = value
    return new_grid


def move_south(grid: GRID, y_size: int) -> GRID:
    new_grid = {(x, y): value for (x, y), value in grid.items() if value == ">"}
    for (x, y), value in grid.items():
        if value == "v":
            new_pos = x, (y + 1) % y_size
            if new_pos in grid:
                new_grid[x, y] = value
            else:
                new_grid[new_pos] = value
    return new_grid


def display_grid(grid: GRID, x_size: int, y_size: int):
    for y in range(y_size):
        for x in range(x_size):
            print(grid.get((x, y), "."), end="")
        print("")


def part_one(puzzle: list[str]) -> int:
    grid = parse_input(puzzle)
    x_size = max(i[0] for i in grid) + 1
    y_size = max(i[1] for i in grid) + 1

    iterations = 0
    while True:
        new_grid = move_east(grid, x_size)
        new_grid = move_south(new_grid, y_size)
        iterations += 1
        if new_grid == grid:
            return iterations
        grid = new_grid
        if puzzle == TEST_INPUT and iterations > 60:
            raise ValueError("oh noes")


def main():
    part_one_result = part_one(TEST_INPUT)
    assert part_one_result == 58, part_one_result
    with open("day25.txt") as infile:
        puzzle = [line.strip() for line in infile]
    print(part_one(puzzle))


if __name__ == "__main__":
    main()
