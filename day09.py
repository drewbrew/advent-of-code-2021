from typing import Iterable
from queue import Queue


TEST_INPUT = """2199943210
3987894921
9856789892
8767896789
9899965678""".splitlines()


def parse_input(puzzle: Iterable[str]) -> dict[tuple[int, int]]:
    grid = {}
    for y, row in enumerate(puzzle):
        for x, char in enumerate(row):
            grid[x, y] = int(char)
    return grid


def part_one(puzzle: Iterable[str]) -> int:
    grid = parse_input(puzzle)
    score = 0
    for (x, y), value in grid.items():
        neighbors = [
            grid[neighbor]
            for neighbor in [(x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)]
            if neighbor in grid
        ]
        if all(neighbor > value for neighbor in neighbors):
            score += value + 1
    return score


def basin_size(low_point: tuple[int, int], grid: dict[tuple[int, int]]) -> int:
    queue = Queue()
    queue.put(low_point)
    places_seen = set()
    while not queue.empty():
        next_neighbor = queue.get(block=False)
        if next_neighbor in places_seen:
            continue
        places_seen.add(next_neighbor)
        x, y = next_neighbor
        neighbors = [
            neighbor
            for neighbor in [(x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)]
            if neighbor in grid and grid[neighbor] != 9
        ]
        for neighbor in neighbors:
            queue.put(neighbor)
    return len(places_seen)


def part_two(puzzle: Iterable[str]) -> int:
    grid = parse_input(puzzle)
    low_points = []
    for (x, y), value in grid.items():
        neighbors = [
            grid[neighbor]
            for neighbor in [(x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)]
            if neighbor in grid
        ]
        if all(neighbor > value for neighbor in neighbors):
            low_points.append((x, y))
    basin_sizes = sorted((basin_size(pos, grid) for pos in low_points), reverse=True)
    return basin_sizes[0] * basin_sizes[1] * basin_sizes[2]


def main():
    part_one_test = part_one(TEST_INPUT)
    assert part_one_test == 15, part_one_test
    part_two_test = part_two(TEST_INPUT)
    assert part_two_test == 1134, part_two_test
    with open("day09.txt") as infile:
        puzzle = [line.strip() for line in infile]
    print(part_one(puzzle))
    print(part_two(puzzle))


if __name__ == "__main__":
    main()
