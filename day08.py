from typing import Iterable
from itertools import permutations
import sys


TEST_INPUT = """be cfbegad cbdgef fgaecd cgeb fdcge agebfd fecdb fabcd edb | fdgacbe cefdb cefbgd gcbe
edbfga begcd cbg gc gcadebf fbgde acbgfd abcde gfcbed gfec | fcgedb cgb dgebacf gc
fgaebd cg bdaec gdafb agbcfd gdcbef bgcad gfac gcb cdgabef | cg cg fdcagb cbg
fbegcd cbd adcefb dageb afcb bc aefdc ecdab fgdeca fcdbega | efabcd cedba gadfec cb
aecbfdg fbg gf bafeg dbefa fcge gcbea fcaegb dgceab fcbdga | gecf egdcabf bgf bfgea
fgeab ca afcebg bdacfeg cfaedg gcfdb baec bfadeg bafgc acf | gebdcfa ecba ca fadegcb
dbcfg fgd bdegcaf fgec aegbdf ecdfab fbedc dacgb gdcebf gf | cefg dcbef fcge gbcadfe
bdfegc cbegaf gecbf dfcage bdacg ed bedf ced adcbefg gebcd | ed bcgafe cdgba cbgef
egadfb cdbfeg cegd fecab cgb gbdefca cg fgcdab egfdb bfceg | gbdfcae bgc cg cgb
gcafb gcf dcaebfg ecagb gf abcdeg gaef cafbge fdbac fegbdc | fgae cfgab fg bagce""".splitlines()


# move up 5 lines
MOVE_UP = "\x1B[5F"


def display_digits(digits: list[str]) -> None:
    # top line
    line_1 = " ".join(" - " if "a" in digit else "   " for digit in digits)
    # top vertical lines
    line_2 = " ".join(
        f'{"|" if "b" in digit else " "} {"|" if "c" in digit else " "}'
        for digit in digits
    )
    # middle line
    line_3 = " ".join(" - " if "d" in digit else "   " for digit in digits)
    # bottom vertical lines
    line_4 = " ".join(
        f'{"|" if "e" in digit else " "} {"|" if "f" in digit else " "}'
        for digit in digits
    )
    # bottom line
    line_5 = " ".join(" - " if "g" in digit else "   " for digit in digits)
    print(MOVE_UP + line_1)
    print(line_2)
    print(line_3)
    print(line_4)
    print(line_5)


def part_one(puzzle: Iterable[str]) -> int:
    count = 0
    for line in puzzle:
        _, output = line.split("|")
        words = list(output.split())
        count += sum(len(word) in {2, 3, 4, 7} for word in words)
    return count


def sub_out_words(words: Iterable[str], cipher: tuple[str]) -> list[str]:
    output = []
    for word in words:
        new_word = ""
        for char in word:
            new_word += cipher[ord(char) - ord("a")]
        output.append("".join(sorted(i for i in new_word)))
    return output


def decode_line(line: str, display: bool = False) -> int:
    expected_outputs = {
        "abcefg": 0,
        "cf": 1,
        "acdeg": 2,
        "acdfg": 3,
        "bcdf": 4,
        "abdfg": 5,
        "abdefg": 6,
        "acf": 7,
        "abcdefg": 8,
        "abcdfg": 9,
    }
    targeted_words = set(expected_outputs)
    # oh, hey, this is a substitution cipher
    # and we only have 10 inputs and outputs
    # so we might be able to brute force it
    perms = list(permutations("abcdefg"))
    in_words, out_words = [i.strip().split() for i in line.split("|")]
    if display:
        # print 6 lines so we don't wreck the console (and have a space between digits for readability)
        print("\n\n\n\n\n")
    for candidate in perms:
        # 'abcdefg' should become 'deafgbc'

        decoded_inputs = sub_out_words(in_words, candidate)
        if display:
            display_digits(decoded_inputs)
        if set(decoded_inputs) == targeted_words:
            decoded_output = sub_out_words(out_words, candidate)
            return int("".join(str(expected_outputs[word]) for word in decoded_output))

    raise ValueError(f"Did not get a winner from {line}")


def part_two(puzzle: Iterable[str], display: bool = False) -> int:
    return sum(decode_line(line, display) for line in puzzle)


def main():
    part_one_result = part_one(TEST_INPUT)
    assert part_one_result == 26, part_one_result
    part_two_test = [
        "acedgfb cdfbe gcdfa fbcad dab cefabd cdfgeb eafb cagedb ab | cdfeb fcadb cdfeb cdbaf"
    ]
    part_two_result = part_two(part_two_test)
    assert part_two_result == 5353, part_two_result
    with open("day08.txt") as infile:
        puzzle = [line.strip() for line in infile]
    print(part_one(puzzle))
    print(part_two(puzzle, "display" in sys.argv))


if __name__ == "__main__":
    main()
