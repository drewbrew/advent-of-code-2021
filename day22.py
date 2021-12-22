from typing import Generator, Iterable
import datetime


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

COORDINATE_PAIR = tuple[int, int]
REGION = tuple[COORDINATE_PAIR, COORDINATE_PAIR, COORDINATE_PAIR]
PUZZLE = list[tuple[bool, COORDINATE_PAIR, COORDINATE_PAIR, COORDINATE_PAIR]]


def parse_input(puzzle: Iterable[str], is_part_one: bool = True) -> PUZZLE:
    result = []
    for line in puzzle:
        state, coords = line.split()
        on = state == "on"
        x_str, y_str, z_str = [i[2:] for i in coords.split(",")]
        x_start, x_end = sorted([int(i) for i in x_str.split("..")])
        y_start, y_end = sorted([int(i) for i in y_str.split("..")])
        z_start, z_end = sorted([int(i) for i in z_str.split("..")])
        result.append(
            # the fudge factor here makes the naive solution easy in part 1
            # as I can easily do a range() call
            (
                on,
                (x_start, x_end + is_part_one),
                (y_start, y_end + is_part_one),
                (z_start, z_end + is_part_one),
            )
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


def cuboid_reboot(instructions: PUZZLE) -> list[REGION]:
    regions: list[REGION] = []
    active_regions: list[REGION] = []
    for state, x_values, y_values, z_values in instructions:
        active_regions.clear()
        for x2_values, y2_values, z2_values in regions:
            # for all existing regions (read: last instruction's active regions),
            # subtract the regions in the instruction from them
            active_regions.extend(
                region_subtract(
                    (x2_values, y2_values, z2_values),
                    (x_values, y_values, z_values),
                )
            )
        if state:
            # save them to the active regions
            active_regions.append((x_values, y_values, z_values))
        # then swap active regions with target regions
        # because the active regions are all we care about
        regions, active_regions = active_regions, regions
    # this is the final list of active regions
    return regions


def region_subtract(
    region_1: REGION,
    region_2: REGION,
) -> Generator[REGION, None, None]:
    """Generate all possible regions formed by subtracting region 2 from region 1"""
    if region_1 != region_2:
        if not regions_overlap(region_1, region_2):
            yield region_1

        else:
            (x_1_min, x_1_max), (y_1_min, y_1_max), (z_1_min, z_1_max) = region_1
            (x_2_min, x_2_max), (y_2_min, y_2_max), (z_2_min, z_2_max) = region_2
            # we have 3 boundaries in each dimension to consider:
            # 1. the lower end of both regions (offset by 1 in the removal region)
            # 2. the middle point where r1 ends and r2 begins or vice versa
            # 3. the higher end of both regions (same offset in the reverse direction)
            for x_index, (x_min, x_max) in enumerate(
                zip(
                    (x_1_min, max(x_1_min, x_2_min), x_2_max + 1),
                    (x_2_min - 1, min(x_1_max, x_2_max), x_1_max),
                )
            ):
                if x_min > x_max:
                    continue
                for y_index, (y_min, y_max) in enumerate(
                    zip(
                        (y_1_min, max(y_1_min, y_2_min), y_2_max + 1),
                        (y_2_min - 1, min(y_1_max, y_2_max), y_1_max),
                    )
                ):
                    if y_min > y_max:
                        continue
                    for z_index, (z_min, z_max) in enumerate(
                        zip(
                            (z_1_min, max(z_1_min, z_2_min), z_2_max + 1),
                            (z_2_min - 1, min(z_1_max, z_2_max), z_1_max),
                        )
                    ):
                        if z_min > z_max:
                            continue
                        if x_index == 1 and y_index == 1 and z_index == 1:
                            # catch factor: don't include the max/min pair to avoid
                            # the dead center of the cuboid
                            continue
                        yield (x_min, x_max), (y_min, y_max), (z_min, z_max)


def regions_overlap(region_1: REGION, region_2: REGION) -> bool:
    (x_1_min, x_1_max), (y_1_min, y_1_max), (z_1_min, z_1_max) = region_1
    (x_2_min, x_2_max), (y_2_min, y_2_max), (z_2_min, z_2_max) = region_2
    return (
        x_2_min <= x_1_max
        and x_2_max >= x_1_min
        and y_2_min <= y_1_max
        and y_2_max >= y_1_min
        and z_2_min <= z_1_max
        and z_2_max >= z_1_min
    )


def region_size(region: REGION) -> int:
    (x_min, x_max), (y_min, y_max), (x_min, z_max) = region
    return (x_max - x_min + 1) * (y_max - y_min + 1) * (z_max - x_min + 1)


def part_two(puzzle: Iterable[str]) -> int:
    rules = parse_input(puzzle, is_part_one=False)
    regions = cuboid_reboot(rules)
    return sum(region_size(region) for region in regions)


def main():
    part_one_result = part_one(TEST_INPUT)
    assert part_one_result == 590784, part_one_result
    with open("day22.txt") as infile:
        puzzle = [line.strip() for line in infile]
    print(part_one(puzzle=puzzle))
    print(part_two(puzzle))


if __name__ == "__main__":
    main()
