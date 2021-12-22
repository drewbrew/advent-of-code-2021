from typing import Iterable


TEST_INPUT = """on x=-20..26,y=-36..17,z=-47..7
on x=-20..33,y=-21..23,z=-26..28
on x=-22..28,y=-29..23,z=-38..16
on x=-46..7,y=-6..46,z=-50..-1
on x=-49..1,y=-3..46,z=-24..28
on x=2..47,y=-22..22,z=-23..27
on x=-27..23,y=-28..26,z=-21..29
on x=-39..5,y=-6..47,z=-3..44
on x=-30..21,y=-8..43,z=-13..34
on x=-22..26,y=-27..20,z=-29..19
off x=-48..-32,y=26..41,z=-47..-37
on x=-12..35,y=6..50,z=-50..-2
off x=-48..-32,y=-32..-16,z=-15..-5
on x=-18..26,y=-33..15,z=-7..46
off x=-40..-22,y=-38..-28,z=23..41
on x=-16..35,y=-41..10,z=-47..6
off x=-32..-23,y=11..30,z=-14..3
on x=-49..-5,y=-3..45,z=-29..18
off x=18..30,y=-20..-8,z=-3..13
on x=-41..9,y=-7..43,z=-33..15
on x=-54112..-39298,y=-85059..-49293,z=-27449..7877
on x=967..23432,y=45373..81175,z=27513..53682""".splitlines()

COORDINATE = tuple[int, int]
PUZZLE = list[tuple[bool, COORDINATE, COORDINATE, COORDINATE]]


def parse_input(puzzle: Iterable[str]) -> PUZZLE:
    result = []
    for line in puzzle:
        state, coords = line.split()
        on = state == "on"
        x_str, y_str, z_str = [i[2:] for i in coords.split(",")]
        x_start, x_end = sorted([int(i) for i in x_str.split("..")])
        y_start, y_end = sorted([int(i) for i in y_str.split("..")])
        z_start, z_end = sorted([int(i) for i in z_str.split("..")])
        result.append(
            (on, (x_start, x_end + 1), (y_start, y_end + 1), (z_start, z_end + 1))
        )
    return result


def part_one(puzzle: Iterable[str], max_coord: int = 50) -> int:
    grid = set()
    for state, (x_min, x_max), (y_min, y_max), (z_min, z_max) in parse_input(puzzle):
        x_range = range(max(x_min, -max_coord), min(x_max, max_coord + 1))
        y_range = range(max(y_min, -max_coord), min(y_max, max_coord + 1))
        z_range = range(max(z_min, -max_coord), min(z_max, max_coord + 1))
        if state:
            grid |= set((x, y, z) for x in x_range for y in y_range for z in z_range)
        else:
            grid -= set((x, y, z) for x in x_range for y in y_range for z in z_range)
    return len(grid)


def is_lit(x: int, y: int, z: int, rules: PUZZLE) -> bool:
    current_state = False
    for state, (x_min, x_max), (y_min, y_max), (z_min, z_max) in rules:
        if state == current_state:
            continue
        if x < x_min or x >= x_max:
            continue
        if y < y_min or y >= y_max:
            continue
        if z < z_min or z >= z_max:
            continue
        current_state = state
    return current_state


def part_two(puzzle: Iterable[str]) -> int:
    rules = parse_input(puzzle)
    count = 0
    min_x = min(x_min for _, (x_min, _), (_, _), (_, _) in rules)
    max_x = max(x_max for _, (_, x_max), (_, _), (_, _) in rules)
    min_y = min(y_min for _, (_, _), (y_min, _), (_, _) in rules)
    max_y = max(y_max for _, (_, _), (_, y_max), (_, _) in rules)
    min_z = min(z_min for _, (_, _), (_, _), (z_min, _) in rules)
    max_z = max(z_max for _, (_, _), (_, _), (_, z_max) in rules)
    print(min_x, max_x, min_y, max_y, min_z, max_z)
    for x in range(min_x, max_x):
        print(x, count)
        for y in range(min_y, max_y):
            for z in range(min_z, max_z):
                count += is_lit(x, y, z, rules)
    return count


def main():
    part_one_result = part_one(TEST_INPUT)
    assert part_one_result == 590784, part_one_result
    part_two_result = part_two(TEST_INPUT)
    assert part_two_result == 2758514936282235, part_two_result
    with open("day22.txt") as infile:
        puzzle = [line.strip() for line in infile]
    print(part_one(puzzle=puzzle))
    print(part_two(puzzle))


if __name__ == "__main__":
    main()
