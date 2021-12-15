from typing import Iterable
from networkx import DiGraph, shortest_path

TEST_INPUT = """1163751742
1381373672
2136511328
3694931569
7463417111
1319128137
1359912421
3125421639
1293138521
2311944581""".splitlines()


def parse_input(puzzle: Iterable[str]) -> DiGraph:
    graph = DiGraph()
    seen = {}
    for y, row in enumerate(puzzle):
        for x, char in enumerate(row):
            neighbors = [(x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)]
            value = int(char)
            seen[x, y] = value
            for dx, dy in neighbors:
                try:
                    neighbor = seen[dx, dy]
                except KeyError:
                    try:
                        neighbor = int(puzzle[dy][dx])
                    except IndexError:
                        continue
                graph.add_edge((x, y), (dx, dy), weight=neighbor)
    return graph


def display_grid(grid: dict[tuple[int, int], int]):
    max_x, max_y = max(grid)
    for y in range(max_y + 1):
        for x in range(max_x + 1):
            print(grid.get((x, y), " "), end="")
        print("")


def scale_puzzle(puzzle: Iterable[str]) -> tuple[DiGraph, dict[tuple[int, int], int]]:
    graph = parse_input(puzzle)
    grid = {}
    for y, row in enumerate(puzzle):
        for x, char in enumerate(row):
            grid[x, y] = int(char)
    width = len(puzzle)
    assert width == len(puzzle[0])
    for (x, y), risk in list(grid.items()):
        risk_scales = [
            risk + i if risk + i < 10 else (risk + i) % 10 + 1 for i in range(1, 9)
        ]
        if risk == 8:
            assert risk_scales == [9, 1, 2, 3, 4, 5, 6, 7]
        # 1 step each way (9 on the example)
        grid[x + width, y] = risk_scales[0]
        grid[x, y + width] = risk_scales[0]
        # 2 steps each way (1)
        grid[x + width * 2, y] = risk_scales[1]
        grid[x + width, y + width] = risk_scales[1]
        grid[x, y + width * 2] = risk_scales[1]
        # 3 (2)
        grid[x + width * 3, y] = risk_scales[2]
        grid[x + width * 2, y + width] = risk_scales[2]
        grid[x + width, y + width * 2] = risk_scales[2]
        grid[x, y + width * 3] = risk_scales[2]
        # 4 (3)
        grid[x + width * 4, y] = risk_scales[3]
        grid[x + width * 3, y + width] = risk_scales[3]
        grid[x + width * 2, y + width * 2] = risk_scales[3]
        grid[x + width, y + width * 3] = risk_scales[3]
        grid[x, y + width * 4] = risk_scales[3]
        # 5 (4)
        grid[x + width * 4, y + width] = risk_scales[4]
        grid[x + width * 3, y + width * 2] = risk_scales[4]
        grid[x + width * 2, y + width * 3] = risk_scales[4]
        grid[x + width, y + width * 4] = risk_scales[4]
        # 6 (5)
        grid[x + width * 4, y + width * 2] = risk_scales[5]
        grid[x + width * 3, y + width * 3] = risk_scales[5]
        grid[x + width * 2, y + width * 4] = risk_scales[5]
        # 7 (6)
        grid[x + width * 4, y + width * 3] = risk_scales[6]
        grid[x + width * 3, y + width * 4] = risk_scales[6]
        # 8 (7)
        grid[x + width * 4, y + width * 4] = risk_scales[7]

    for (
        x,
        y,
    ) in grid:
        neighbors = [
            (pos, grid[pos])
            for pos in ((x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1))
            if pos in grid
        ]
        for (dx, dy), risk in neighbors:
            if (dx, dy) == (0, 0):
                continue

            graph.add_edge((x, y), (dx, dy), weight=risk)
    return graph, grid


def part_two(puzzle: Iterable[str]) -> int:
    graph, grid = scale_puzzle(puzzle)
    path = shortest_path(graph, (0, 0), max(grid), weight="weight")
    return sum(grid[x, y] for x, y in path[1:])


def part_one(puzzle: Iterable[str]) -> int:
    graph = parse_input(puzzle)
    path = shortest_path(
        graph, (0, 0), max(graph.nodes), weight="weight"
    )
    return sum(int(puzzle[y][x]) for x, y in path[1:])


def main():
    part_one_result = part_one(TEST_INPUT)
    assert part_one_result == 40, part_one_result
    part_two_result = part_two(TEST_INPUT)
    assert part_two_result == 315, part_two_result
    with open("day15.txt") as infile:
        puzzle = [line.strip() for line in infile]
    print(part_one(puzzle))
    print(part_two(puzzle))


if __name__ == "__main__":
    main()
