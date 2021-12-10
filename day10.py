"""Day 10: syntax errors, all of them"""


from typing import Iterable, Optional


SCORES = {
    ")": 3,
    "]": 57,
    "}": 1197,
    ">": 25137,
}

CHAR_MATCHES = {
    "<": ">",
    "{": "}",
    "[": "]",
    "(": ")",
}


TEST_INPUT = """[({(<(())[]>[[{[]{<()<>>
[(()[<>])]({[<{<<[]>>(
{([(<{}[<>[]}>{[]{[(<()>
(((({<>}<{<{<>}{[]{[]{}
[[<[([]))<([[{}[[()]]]
[{[{({}]{}}([{[{{{}}([]
{<[[]]>}<{[{[{[]{()[[[]
[<(<(<(<{}))><([]([]()
<{([([[(<>()){}]>(<<{{
<{([{{}}[<[[[<>{}]]]>[]]""".splitlines()


def first_incorrect_char(line: str) -> Optional[str]:
    tokens = []
    for char in line:
        if char in CHAR_MATCHES:
            tokens.append(char)
            continue
        if char != CHAR_MATCHES[tokens[-1]]:
            return char
        # we matched that token. Drop it
        tokens.pop()
    return None


def complete_the_line(line: str) -> Optional[str]:
    tokens = []
    for char in line:
        if char in CHAR_MATCHES:
            tokens.append(char)
            continue
        if char != CHAR_MATCHES[tokens[-1]]:
            return None
        # we matched that token. Drop it
        tokens.pop()
    return "".join(CHAR_MATCHES[char] for char in reversed(tokens))


def score_completion(completion_chars: str) -> int:
    score = 0
    points = {
        ")": 1,
        "]": 2,
        "}": 3,
        ">": 4,
    }
    for char in completion_chars:
        score *= 5
        score += points[char]
    return score


def part_one(puzzle: Iterable[str]) -> int:
    chars = [first_incorrect_char(line) for line in puzzle]
    return sum(SCORES[i] for i in chars if i is not None)


def part_two(puzzle: Iterable[str]) -> int:
    completions = [complete_the_line(line) for line in puzzle]
    scores = sorted(
        score_completion(completion)
        for completion in completions
        if completion is not None
    )
    return scores[len(scores) // 2]


def main():
    assert first_incorrect_char(TEST_INPUT[0]) is None, first_incorrect_char(
        TEST_INPUT[0]
    )
    assert first_incorrect_char(TEST_INPUT[2]) == "}", first_incorrect_char(
        TEST_INPUT[2]
    )
    assert first_incorrect_char(TEST_INPUT[4]) == ")", first_incorrect_char(
        TEST_INPUT[4]
    )
    assert first_incorrect_char(TEST_INPUT[5]) == "]", first_incorrect_char(
        TEST_INPUT[5]
    )
    assert first_incorrect_char(TEST_INPUT[-3]) == ")", first_incorrect_char(
        TEST_INPUT[-3]
    )
    assert first_incorrect_char(TEST_INPUT[-2]) == ">", first_incorrect_char(
        TEST_INPUT[-2]
    )
    assert complete_the_line(TEST_INPUT[1]) == ")}>]})", complete_the_line(
        TEST_INPUT[1]
    )
    assert (
        complete_the_line("[({(<(())[]>[[{[]{<()<>>") == "}}]])})]"
    ), complete_the_line("[({(<(())[]>[[{[]{<()<>>")
    part_one_result = part_one(TEST_INPUT)
    assert part_one_result == 6 + 57 + 1197 + 25137, part_one_result
    part_two_result = part_two(TEST_INPUT)
    assert part_two_result == 288957, part_two_result
    with open("day10.txt") as infile:
        puzzle = [line.strip() for line in infile]
    print(part_one(puzzle))
    print(part_two(puzzle))


if __name__ == "__main__":
    main()
