from typing import Iterable
from collections import defaultdict
from queue import Queue
from string import ascii_lowercase
from collections import Counter


TEST_INPUTS = (
    (
        """start-A
start-b
A-c
A-b
b-d
A-end
b-end""".splitlines(),
        10,
        36,
    ),
    (
        """dc-end
HN-start
start-kj
dc-start
dc-HN
LN-dc
HN-end
kj-sa
kj-HN
kj-dc""".splitlines(),
        19,
        103,
    ),
    (
        """fs-end
he-DX
fs-he
start-DX
pj-DX
end-zg
zg-sl
zg-pj
pj-he
RW-he
fs-DX
pj-RW
zg-RW
start-pj
he-WI
zg-he
pj-fs
start-RW""".splitlines(),
        226,
        3509,
    ),
)


def parse_input(puzzle: Iterable[str]) -> dict[str, set[str]]:
    graph = defaultdict(set)
    for line in puzzle:
        start, end = line.split("-")
        graph[start].add(end)
        graph[end].add(start)
    return graph


def part_one(puzzle: Iterable[str]) -> int:
    graph = parse_input(puzzle)
    paths = set()
    intermediate_paths = set()
    queue = Queue()
    queue.put(("start", ["start"]))
    while not queue.empty():
        current_node, path_so_far = queue.get(block=False)
        neighbors = graph[current_node]
        for neighbor in neighbors:
            if neighbor == "start":
                continue
            if neighbor == "end":
                paths.add(tuple(path_so_far + ["end"]))
                continue
            if all(char in ascii_lowercase for char in neighbor):
                if neighbor in path_so_far:
                    # can only visit lowercase points once
                    continue
            new_path = path_so_far + [neighbor]
            if tuple(new_path) in intermediate_paths:
                continue
            queue.put((neighbor, new_path))
    return len(paths)


def part_two(puzzle: Iterable[str]):
    graph = parse_input(puzzle)
    paths = set()
    intermediate_paths = set()
    queue = Queue()
    queue.put(("start", ["start"]))
    while not queue.empty():
        current_node: str
        path_so_far: list[str]
        current_node, path_so_far = queue.get(block=False)
        neighbors = graph[current_node]
        for neighbor in neighbors:
            if neighbor == "start":
                continue
            if neighbor == "end":
                paths.add(tuple(path_so_far + ["end"]))
                continue
            if neighbor == neighbor.lower():
                if neighbor in path_so_far:
                    # have we visited any lowercase caves twice so far?
                    visited = Counter(path_so_far)
                    multi_visited = False
                    for node, count in visited.items():
                        if node == node.lower():
                            if count == 2:
                                multi_visited = True
                                break
                    if multi_visited:
                        continue

            new_path = path_so_far + [neighbor]
            if tuple(new_path) in intermediate_paths:
                continue
            queue.put((neighbor, new_path))

    return len(paths)


def main():
    for puzzle, score, score_p2 in TEST_INPUTS:
        p1_score = part_one(puzzle)
        assert p1_score == score, (puzzle, p1_score)
        p2_score = part_two(puzzle)
        assert p2_score == score_p2, (puzzle, p2_score, score_p2)
    with open("day12.txt") as infile:
        puzzle = [line.strip() for line in infile]
    print(part_one(puzzle))
    print(part_two(puzzle))


if __name__ == "__main__":
    main()
