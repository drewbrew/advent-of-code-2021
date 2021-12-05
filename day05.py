from typing import Iterable
from collections import defaultdict

TEST_INPUT = """0,9 -> 5,9
8,0 -> 0,8
9,4 -> 3,4
2,2 -> 2,1
7,0 -> 7,4
6,4 -> 2,0
0,9 -> 2,9
3,4 -> 1,4
0,0 -> 8,8
5,5 -> 8,2""".splitlines()


def parse_input(puzzle: Iterable[str], skip_diagonal: bool = True) -> defaultdict[tuple[int, int], int]:
    grid = defaultdict(lambda: 0)
    for line in puzzle:
        coord1, coord2 = line.split(' -> ')
        x1, y1 = (int(i) for i in coord1.split(','))
        x2, y2 = (int(i) for i in coord2.split(','))
        if x1 == x2:
            start, end = sorted([y1, y2])
            for y in range(start, end + 1):
                grid[x1, y] += 1
        elif y1 == y2:
            start, end = sorted([x1, x2])
            for x in range(start, end + 1):
                grid[x, y1] += 1
        elif not skip_diagonal:
            # figure out our slope
            dx = 1
            dy = 1
            if x1 > x2:
                dx = -1
            if y1 > y2:
                dy = -1
            # put the starting point in
            grid[x1, y1] += 1
            # then increment both coordinates with each step
            while (x1, y1) != (x2, y2):
                x1 += dx
                y1 += dy
                grid[x1, y1] += 1
    return grid


def part_one(puzzle: Iterable[str], part_two: bool = False) -> int:
    grid = parse_input(puzzle, skip_diagonal=not part_two)
    return len([coord for coord, count in grid.items() if count > 1])


def main():
    part_one_result = part_one(TEST_INPUT)
    part_two_result = part_one(TEST_INPUT, part_two=True)
    assert part_one_result == 5, part_one_result
    assert part_two_result == 12, part_two_result
    with open('day05.txt') as infile:
        puzzle = [line.strip() for line in infile]
    print(part_one(puzzle))
    print(part_one(puzzle, True))
        

if __name__ == '__main__':
    main()