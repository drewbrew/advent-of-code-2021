from collections import Counter, defaultdict
from typing import Iterable


TEST_INPUT = """NNCB

CH -> B
HH -> N
CB -> H
NH -> C
HB -> C
HC -> B
HN -> C
NN -> C
BH -> H
NC -> B
NB -> B
BN -> B
BB -> N
BC -> B
CC -> N
CN -> C""".splitlines()


def parse_input(puzzle: Iterable[str]) -> tuple[str, dict[str, tuple[str, str]]]:
    molecule = puzzle[0]
    assert not puzzle[1]
    output = {}
    for line in puzzle[2:]:
        input_pair, insertion = line.split(" -> ")
        elem1, elem2 = input_pair
        output[input_pair] = (elem1 + insertion, insertion + elem2)
    return molecule, output


def count_elements(state: dict[str, int]) -> dict[str, int]:
    """Count all the first elements in state

    NOTE: This will be off-by-one for the very last element in the source
    molecule, which this function doesn't have access to.
    """
    output = defaultdict(int)
    for pair, count in state.items():
        output[pair[0]] += count
    return output


def make_reactions(
    reactions: dict[str, tuple[str, str]], current_state: dict[str, int]
) -> dict[str, int]:
    output = defaultdict(int)
    for pair, count in current_state.items():
        for reaction_output in reactions[pair]:
            output[reaction_output] += count
    return output


def part_one(puzzle: Iterable[str], iterations: int = 10) -> int:
    molecule, reactions = parse_input(puzzle)
    interim = Counter("".join(i) for i in zip(molecule[:-1], molecule[1:]))
    for _ in range(iterations):
        interim = make_reactions(reactions, interim)
    output = count_elements(interim)
    # fix the off-by-one from count_elements()
    output[molecule[-1]] += 1
    return max(output.values()) - min(output.values())


def main():
    part_one_result = part_one(TEST_INPUT)
    assert part_one_result == 1588
    part_two_result = part_one(TEST_INPUT, 40)
    assert part_two_result == 2188189693529, part_two_result
    with open("day14.txt") as infile:
        puzzle = [line.strip() for line in infile]
    print(part_one(puzzle))
    print(part_one(puzzle, 40))


if __name__ == "__main__":
    main()
