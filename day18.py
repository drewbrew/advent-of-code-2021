"""Day 18: snailfish math"""
import json
from typing import Iterable, Literal
from itertools import permutations


class Snailfish:
    def __init__(self, raw_data: list | str, depth: int = 0) -> None:
        if isinstance(raw_data, str):
            raw_data = json.loads(raw_data)

        assert len(raw_data) == 2, raw_data
        self.depth = depth
        if isinstance(raw_data[0], list):
            self.left = Snailfish(raw_data[0], depth=self.depth + 1)
        else:
            assert isinstance(raw_data[0], int)
            self.left = raw_data[0]
        if isinstance(raw_data[1], list):
            self.right = Snailfish(raw_data[1], depth=self.depth + 1)
        else:
            assert isinstance(raw_data[1], int)
            self.right = raw_data[1]

    def __repr__(self) -> str:
        return "[" + repr(self.left) + "," + repr(self.right) + "]"

    def add_to_left(self, value: int):
        if isinstance(self.left, int):
            self.left += value
        elif isinstance(self.left, Snailfish):
            self.left.add_to_left(value)
        else:
            raise TypeError(str(type(self.left)))

    def add_to_right(self, value: int):
        if isinstance(self.right, int):
            self.right += value
        elif isinstance(self.right, Snailfish):
            self.right.add_to_right(value)
        else:
            raise TypeError(str(type(self.right)))

    def needs_exploding(self) -> bool:
        if self.depth >= 4:
            return True
        needs_exploding = False
        if isinstance(self.left, Snailfish):
            needs_exploding = needs_exploding or self.left.needs_exploding()
        if isinstance(self.right, Snailfish):
            needs_exploding = needs_exploding or self.right.needs_exploding()
        return needs_exploding

    def explode(self) -> Literal[False] | tuple[int, int]:
        currently_exploding = False
        if not self.needs_exploding():
            return False
        if self.depth == 4:
            assert all(isinstance(x, int) for x in (self.left, self.right))
            # yay we must explode
            return self.left, self.right

        if isinstance(self.left, Snailfish):
            currently_exploding = self.left.explode()
        if currently_exploding:
            left, right = currently_exploding
            if self.depth == 3:
                self.left = 0
            if isinstance(self.right, int):
                self.right += right
            else:
                self.right.add_to_left(right)
            return left, 0
        if isinstance(self.right, Snailfish):
            currently_exploding = self.right.explode()
        if currently_exploding:
            left, right = currently_exploding
            if self.depth == 3:
                self.right = 0
            if isinstance(self.left, int):
                self.left += left
            else:
                self.left.add_to_right(left)
            return 0, right
        return currently_exploding

    def split(self) -> bool:
        is_split = False
        if isinstance(self.left, int):
            if self.left >= 10:
                self.left = Snailfish(
                    [self.left // 2, self.left // 2 + self.left % 2], self.depth + 1
                )
                return True
        else:
            is_split = self.left.split()
        if not is_split:
            if isinstance(self.right, int):
                if self.right >= 10:
                    self.right = Snailfish(
                        [self.right // 2, self.right // 2 + self.right % 2],
                        self.depth + 1,
                    )
                    return True
            else:
                is_split = self.right.split()
        return is_split

    def reduce(self) -> None:
        while self.explode() or self.split():
            # keep doing nothing until both rules are satisfied
            pass

    def __add__(self, other: "Snailfish") -> "Snailfish":
        # override the addition operator since this is a literal math assignment
        summed = Snailfish(f"[{repr(self)},{repr(other)}]")
        summed.reduce()
        return summed

    @property
    def magnitude(self) -> int:
        score = 0
        if isinstance(self.left, int):
            score += 3 * self.left
        else:
            score += 3 * self.left.magnitude
        if isinstance(self.right, int):
            score += 2 * self.right
        else:
            score += 2 * self.right.magnitude
        return score


def part_one(puzzle: Iterable[str]) -> int:
    total_fish = None
    for line in puzzle:
        if not total_fish:
            total_fish = Snailfish(json.loads(line))
        else:
            total_fish = total_fish + Snailfish(json.loads(line))
    return total_fish.magnitude


def part_two(puzzle: Iterable[str]) -> int:
    best_score = 0
    perms = permutations([Snailfish(line) for line in puzzle], 2)
    for a, b in perms:
        fish = a + b
        if fish.magnitude > best_score:
            best_score = fish.magnitude
    return best_score


def main():
    fish = Snailfish(json.loads("[[[[[4,3],4],4],[7,[[8,4],9]]],[1,1]]"))
    fish.reduce()
    assert repr(fish) == "[[[[0,7],4],[[7,8],[6,0]]],[8,1]]", repr(fish)
    assert Snailfish([[9, 1], [1, 9]]).magnitude == 129
    assert (
        Snailfish(
            [[[[8, 7], [7, 7]], [[8, 6], [7, 7]]], [[[0, 7], [6, 6]], [8, 7]]]
        ).magnitude
        == 3488
    )
    assert (
        Snailfish(
            [[[[6, 6], [7, 6]], [[7, 7], [7, 0]]], [[[7, 7], [7, 7]], [[7, 8], [9, 9]]]]
        ).magnitude
        == 4140
    )
    test_input = """[[[0,[5,8]],[[1,7],[9,6]]],[[4,[1,2]],[[1,4],2]]]
[[[5,[2,8]],4],[5,[[9,9],0]]]
[6,[[[6,2],[5,6]],[[7,6],[4,7]]]]
[[[6,[0,7]],[0,9]],[4,[9,[9,0]]]]
[[[7,[6,4]],[3,[1,3]]],[[[5,5],1],9]]
[[6,[[7,3],[3,2]]],[[[3,8],[5,7]],4]]
[[[[5,4],[7,7]],8],[[8,3],8]]
[[9,3],[[9,9],[6,[4,9]]]]
[[2,[[7,7],7]],[[5,8],[[9,3],[0,2]]]]
[[[[5,2],5],[8,[3,7]]],[[5,[7,5]],[4,4]]]
""".splitlines()
    part_one_result = part_one(test_input)
    assert part_one_result == 4140, part_one_result
    part_two_result = part_two(test_input)
    assert part_two_result == 3993, part_two_result
    with open("day18.txt") as infile:
        puzzle = [line.strip() for line in infile]
    print(part_one(puzzle))
    print(part_two(puzzle))


if __name__ == "__main__":
    main()
