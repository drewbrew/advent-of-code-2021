from typing import Iterable, Literal, Optional
from itertools import permutations

TEST_INPUT = """--- scanner 0 ---
404,-588,-901
528,-643,409
-838,591,734
390,-675,-793
-537,-823,-458
-485,-357,347
-345,-311,381
-661,-816,-575
-876,649,763
-618,-824,-621
553,345,-567
474,580,667
-447,-329,318
-584,868,-557
544,-627,-890
564,392,-477
455,729,728
-892,524,684
-689,845,-530
423,-701,434
7,-33,-71
630,319,-379
443,580,662
-789,900,-551
459,-707,401

--- scanner 1 ---
686,422,578
605,423,415
515,917,-361
-336,658,858
95,138,22
-476,619,847
-340,-569,-846
567,-361,727
-460,603,-452
669,-402,600
729,430,532
-500,-761,534
-322,571,750
-466,-666,-811
-429,-592,574
-355,545,-477
703,-491,-529
-328,-685,520
413,935,-424
-391,539,-444
586,-435,557
-364,-763,-893
807,-499,-711
755,-354,-619
553,889,-390

--- scanner 2 ---
649,640,665
682,-795,504
-784,533,-524
-644,584,-595
-588,-843,648
-30,6,44
-674,560,763
500,723,-460
609,671,-379
-555,-800,653
-675,-892,-343
697,-426,-610
578,704,681
493,664,-388
-671,-858,530
-667,343,800
571,-461,-707
-138,-166,112
-889,563,-600
646,-828,498
640,759,510
-630,509,768
-681,-892,-333
673,-379,-804
-742,-814,-386
577,-820,562

--- scanner 3 ---
-589,542,597
605,-692,669
-500,565,-823
-660,373,557
-458,-679,-417
-488,449,543
-626,468,-788
338,-750,-386
528,-832,-391
562,-778,733
-938,-730,414
543,643,-506
-524,371,-870
407,773,750
-104,29,83
378,-903,-323
-778,-728,485
426,699,580
-438,-605,-362
-469,-447,-387
509,732,623
647,635,-688
-868,-804,481
614,-800,639
595,780,-596

--- scanner 4 ---
727,592,562
-293,-554,779
441,611,-461
-714,465,-776
-743,427,-804
-660,-479,-426
832,-632,460
927,-485,-438
408,393,-506
466,436,-512
110,16,151
-258,-428,682
-393,719,612
-211,-452,876
808,-476,-593
-575,615,604
-485,667,467
-680,325,-822
-627,-443,-432
872,-547,-609
833,512,582
807,604,487
839,-516,451
891,-625,532
-652,-548,-490
30,-46,-14""".splitlines()

COORDINATE = tuple[int, int, int]


def parse_input(puzzle: Iterable[str]) -> list[COORDINATE]:
    scanners = []
    current_scanner = []
    for line in puzzle:
        if not line:
            continue
        if line.startswith("---"):
            if current_scanner:
                scanners.append(current_scanner)
            current_scanner = []
        else:
            current_scanner.append(tuple(int(i) for i in line.split(",")))
    if current_scanner:
        scanners.append(current_scanner)
    return scanners


def reorient(
    coordinate: COORDINATE,
    axis1: int,
    sign1: Literal[-1] | Literal[1],
    axis2: int,
    sign2: Literal[1] | Literal[-1],
) -> COORDINATE:
    axis3 = 3 - (axis1 + axis2)
    sign3 = 1 if (((axis2 - axis1) % 3 == 1) ^ (sign1 != sign2)) else -1
    return (
        coordinate[axis1] * sign1,
        coordinate[axis2] * sign2,
        coordinate[axis3] * sign3,
    )


def position_deltas(positions: list[COORDINATE]) -> list[COORDINATE]:
    """get a list of all delta values between adjacent coordinates"""
    return [
        (x1 - x0, y1 - y0, z1 - z0)
        for (x0, y0, z0), (x1, y1, z1) in zip(positions, positions[1:])
    ]


def try_alignment(
    known_beacons: list[COORDINATE], unaligned_beacons: list[COORDINATE]
) -> tuple[Optional[set[COORDINATE]], COORDINATE]:
    for axis in range(3):
        known_sorted = sorted(known_beacons, key=lambda coordinate: coordinate[axis])
        unaligned_beacons.sort(key=lambda coordinate: coordinate[axis])
        known_deltas = position_deltas(known_sorted)
        unaligned_deltas = position_deltas(unaligned_beacons)
        intersection = set(known_deltas).intersection(unaligned_deltas)
        if intersection:
            diff = intersection.pop()
            known_x, known_y, known_z = known_sorted[known_deltas.index(diff)]
            unaligned_x, unaligned_y, unaligned_z = unaligned_beacons[
                unaligned_deltas.index(diff)
            ]
            origin_x, origin_y, origin_z = (
                unaligned_x - known_x,
                unaligned_y - known_y,
                unaligned_z - known_z,
            )
            moved = {
                (x - origin_x, y - origin_y, z - origin_z)
                for (x, y, z) in unaligned_beacons
            }
            matches = known_beacons & moved
            if len(matches) >= 12:
                return moved, (origin_x, origin_y, origin_z)
    return None, None


def try_orient_and_align(
    known_beacons: list[COORDINATE], readings: list[COORDINATE]
) -> tuple[Optional[list[COORDINATE]], COORDINATE]:
    # work through each rotation + sign inversion
    for axis1 in range(3):
        for sign1 in [1, -1]:
            for axis2 in {0, 1, 2} - {axis1}:
                for sign2 in [1, -1]:
                    unaligned_beacons = [
                        reorient(reading, axis1, sign1, axis2, sign2)
                        for reading in readings
                    ]
                    aligned_beacons, scanner_pos = try_alignment(
                        known_beacons, unaligned_beacons
                    )
                    if aligned_beacons:
                        return aligned_beacons, scanner_pos
    return None, None


def orient_all(
    known_beacons: set[COORDINATE],
    known_scanners: list[COORDINATE],
    unaligned_readings: list[COORDINATE],
) -> None:
    # work through everything we don't know until we successfully align the scanners
    while unaligned_readings:
        progress = False
        for readings in list(unaligned_readings):
            beacons, scanner_pos = try_orient_and_align(known_beacons, readings)
            if beacons:
                unaligned_readings.remove(readings)
                known_beacons |= beacons
                known_scanners.append(scanner_pos)
                progress = True
        assert progress


def run_puzzle(puzzle: Iterable[str]) -> tuple[int, int]:
    scanner_readings = parse_input(puzzle)
    known_scanners = [(0, 0, 0)]
    known_beacons = set(scanner_readings[0])
    unaligned = scanner_readings[1:]
    orient_all(
        known_beacons=known_beacons,
        known_scanners=known_scanners,
        unaligned_readings=unaligned,
    )
    part_one_result = len(known_beacons)
    pairs = permutations(known_scanners, 2)
    distances = [(x1 - x0, y1 - y0, z1 - z0) for (x0, y0, z0), (x1, y1, z1) in pairs]
    part_two_result = max(abs(x) + abs(y) + abs(z) for (x, y, z) in distances)
    return part_one_result, part_two_result


def main():
    part_one_result, part_two_result = run_puzzle(TEST_INPUT)
    assert part_one_result == 79, part_one_result
    assert part_two_result == 3621, part_two_result
    with open("day19.txt") as infile:
        puzzle = [line.strip() for line in infile]
    print("\n".join(str(i) for i in run_puzzle(puzzle)))


if __name__ == "__main__":
    main()
