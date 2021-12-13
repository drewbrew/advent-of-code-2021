from collections import defaultdict
from typing import Iterable, Optional


TEST_INPUT = """6,10
0,14
9,10
0,3
10,4
4,11
6,0
6,12
4,1
0,13
10,12
3,4
3,0
8,4
1,10
2,14
8,10
9,0

fold along y=7
fold along x=5
""".splitlines()


def parse_input(
    puzzle: Iterable[str],
) -> tuple[dict[tuple[int, int], bool], list[tuple[Optional[int], Optional[int]]]]:
    grid = defaultdict(lambda: False)
    folds = []
    for line in puzzle:
        if not line:
            continue
        if "," in line:
            x, y = [int(i.strip()) for i in line.split(",")]
            grid[x, y] = True
        elif line.startswith("fold along"):
            words = line.split()
            coord, amount = words[-1].split("=")
            amount = int(amount)
            if coord == "x":
                folds.append((amount, None))
            else:
                folds.append((None, amount))
        else:
            raise ValueError("Unknown line " + line)
    return grid, folds


def fold_grid(
    grid: dict[tuple[int, int], bool], amount: tuple[Optional[int], Optional[int]]
) -> None:
    x, y = amount
    if x:
        coordinates = [pos for pos, value in grid.items() if value and pos[0] > x]
        for coordinate in coordinates:
            grid[coordinate] = False
            dx, y = coordinate
            delta = dx - x
            # yes I could simplify this but I'm not awake enough for that
            grid[dx - delta - delta, y] = True
    elif y:
        coordinates = [pos for pos, value in grid.items() if pos[1] > y and value]
        for coordinate in coordinates:
            grid[coordinate] = False
            x, dy = coordinate
            delta = dy - y
            grid[x, dy - delta - delta] = True
    else:
        raise ValueError("both are false?")


def display_grid(grid: dict[tuple[int, int], bool]) -> None:
    max_x = max(pos[0] for pos, value in grid.items() if value)
    max_y = max(pos[1] for pos, value in grid.items() if value)
    for y in range(max_y + 1):
        for x in range(max_x + 1):
            print("#" if grid[x, y] else ".", end="")
        print("")


def part_one(puzzle: Iterable[str]) -> int:
    grid, folds = parse_input(puzzle)
    fold_grid(grid, folds[0])
    return sum(grid.values())


def part_two(puzzle: Iterable[str]) -> dict[tuple[int, int], bool]:
    grid, folds = parse_input(puzzle)
    for fold in folds:
        fold_grid(grid, fold)
    return grid


def main():
    part_one_result = part_one(TEST_INPUT)
    assert part_one_result == 17, part_one_result
    with open("day13.txt") as infile:
        puzzle = [line.strip() for line in infile]
    print(part_one(puzzle))
    display_grid(part_two(puzzle))


if __name__ == "__main__":
    main()
