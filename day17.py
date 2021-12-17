TEST_INPUT = "target area: x=20..30, y=-10..-5"

PUZZLE_INPUT = "target area: x=128..160, y=-142..-88"


def advance(
    position: tuple[int, int], velocity: tuple[int, int]
) -> tuple[tuple[int, int], tuple[int, int]]:
    x, y = position
    vx, vy = velocity
    x += vx
    y += vy
    if vx > 0:
        vx -= 1
    elif vx < 0:
        vx += 1
    vy -= 1
    return (x, y), (vx, vy)


def parse_input(puzzle: str) -> set[tuple[int, int]]:
    words = puzzle.split()
    min_x, max_x = [int(i) for i in words[2][2:-1].split("..")]
    min_y, max_y = [int(i) for i in words[-1][2:].split("..")]
    return set((x, y) for x in range(min_x, max_x + 1) for y in range(min_y, max_y + 1))


def x_values(grid: set[tuple[int, int]]) -> list[int, int]:
    candidates = []
    max_x = max(i[0] for i in grid)
    min_x = min(i[0] for i in grid)
    for x in range(max_x + 1):
        score = 0
        dx = x
        while dx > 0 and score <= max_x:
            score += dx
            if score >= min_x and score <= max_x:
                candidates.append(x)
                break
    return candidates


def part_two(puzzle: str) -> int:
    """find the number of velocity combos possible that hit the target"""
    grid = parse_input(puzzle)
    min_x = 1
    max_x = max(i[0] for i in grid)
    y_candidates = sorted(set(i[1] for i in grid))
    min_y = y_candidates[0]
    candidates = 0
    hits = set()
    for vx0 in range(min_x, max_x + 1):
        for vy in range(min_y, abs(min_y) + 1):
            x, y = (0, 0)
            vx = vx0
            vy0 = vy
            while y >= min_y and x <= max_x:
                if (x, y) in grid:
                    candidates += 1
                    hits.add((vx0, vy0))
                    break
                (x, y), (vx, vy) = advance((x, y), (vx, vy))

    return candidates


def part_one(puzzle: str) -> int:
    """find the max y velocity possible while still hitting the target"""
    grid = parse_input(puzzle)
    # start with finding the range of x values such that the sum of x + (x - 1) + (x - 2) ...
    # has an integer value within our grid
    x_candidates = x_values(grid)
    y_candidates = sorted(set(i[1] for i in grid))
    min_y = y_candidates[0]
    # overshoot just for fun
    max_y = abs(y_candidates[-1] * 3)
    candidates = []
    for vx in x_candidates:
        vx0 = vx
        for vy in range(min_y, max_y + 1):
            x, y = (0, 0)
            vy0 = vy
            vx = vx0
            max_y_found = -1000
            while y >= min_y:

                (x, y), (vx, vy) = advance((x, y), (vx, vy))
                if y > max_y_found:
                    max_y_found = y
                if (x, y) in grid:
                    candidates.append(max_y_found)
                    break

    return max(candidates)


def main():

    assert part_one(TEST_INPUT) == 45
    assert part_two(TEST_INPUT) == 112, part_two(TEST_INPUT)
    print(part_one(PUZZLE_INPUT))
    print(part_two(PUZZLE_INPUT))


if __name__ == "__main__":
    main()
