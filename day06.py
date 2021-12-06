from collections import Counter


TEST_INPUT = "3,4,3,1,2"


def part_one(puzzle_input: str, days: int = 80):
    school = [int(i.strip()) for i in puzzle_input.split(",")]
    for _ in range(days):
        new_school = []
        new_fish = []
        for timer in school:
            if not timer:
                new_fish.append(8)
                new_school.append(6)
            else:
                new_school.append(timer - 1)
        school = new_school + new_fish

    return len(school)


def part_two(puzzle_input: str, days: int = 256):
    school = Counter([int(i.strip()) for i in puzzle_input.split(",")])
    for _ in range(days):
        school = {
            0: school.get(1, 0),
            1: school.get(2, 0),
            2: school.get(3, 0),
            3: school.get(4, 0),
            4: school.get(5, 0),
            5: school.get(6, 0),
            6: school.get(7, 0) + school.get(0, 0),
            7: school.get(8, 0),
            8: school.get(0, 0),
        }
    return sum(school.values())


def main():
    very_short_test = part_one(TEST_INPUT, 3)
    assert very_short_test == 7, very_short_test
    assert part_two(TEST_INPUT, 3) == 7, part_two(TEST_INPUT, 3)
    shorter_test = part_one(TEST_INPUT, 10)
    assert shorter_test == len("0,1,0,5,6,0,1,2,2,3,7,8".split(",")), shorter_test
    assert part_two(TEST_INPUT, 10) == part_one(TEST_INPUT, 10)
    short_test = part_one(TEST_INPUT, 18)
    assert short_test == 26, short_test
    long_test = part_one(TEST_INPUT)
    assert long_test == 5934
    assert part_two(TEST_INPUT, 80) == long_test, part_two(TEST_INPUT, 80)
    very_long_test = part_two(TEST_INPUT, 256)
    assert very_long_test == 26984457539, very_long_test
    with open("day06.txt") as infile:
        puzzle = infile.read()
    print(part_one(puzzle))
    print(part_two(puzzle, 256))


if __name__ == "__main__":
    main()
