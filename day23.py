from queue import Queue
from collections import Counter
from typing import Optional

TEST_INPUT = """#############
#...........#
###B#C#B#D###
  #A#D#C#A#
  #########""".splitlines()


TEST_PART_TWO_INPUT = """#############
#...........#
###B#C#B#D###
  #D#C#B#A#
  #D#B#A#C#
  #A#D#C#A#
  #########""".splitlines()

REAL_INPUT = """#############
#...........#
###B#D#C#A###
  #C#D#B#A#
  #########""".splitlines()

PART_TWO_INPUT = """#############
#...........#
###B#D#C#A###
  #D#C#B#A#
  #D#B#A#C#
  #C#D#B#A#
  #########""".splitlines()


MOVEMENT_COSTS = {
    "A": 1,
    "B": 10,
    "C": 100,
    "D": 1000,
}
DESTINATIONS = {
    "A": 2,
    "B": 4,
    "C": 6,
    "D": 8,
}
ROOMS = {
    "A": 0,
    "B": 1,
    "C": 2,
    "D": 3,
}

HALLWAY_WIDTH = len("...........")

ROOM_STATE = list[tuple[str, str]]
HALL_STATE = list[str]
PUZZLE_STATE = tuple[ROOM_STATE, HALL_STATE, int]


def parse_input(puzzle: list[str]) -> list[tuple[str]]:
    rooms = [[], [], [], []]
    for line in puzzle[2:-1]:
        for index, char in enumerate(c for c in line if c in "ABCD"):
            rooms[index].append(char)

    return [tuple(room) for room in rooms]


def assert_valid_state(hallway: HALL_STATE, side_rooms: ROOM_STATE):
    count = Counter(hallway)
    expected_total = len(side_rooms[0])
    for room in side_rooms:
        count += Counter(room)
    for index, char in enumerate(hallway):
        if index in {2, 4, 6, 8}:
            assert char == ".", (index, char)
    assert all(val == expected_total for key, val in count.items() if key != "."), (
        hallway,
        side_rooms,
        count,
    )


def move_pieces_from_hall(
    hallway_state: HALL_STATE, side_rooms: ROOM_STATE, current_score: int
) -> list[PUZZLE_STATE]:
    result = []
    for index, char in enumerate(hallway_state):
        if char == ".":
            continue
        destination = DESTINATIONS[char]
        # don't need the +1 offset if we're going left
        start, end = (
            (index + 1, destination + 1)
            if destination > index
            else (destination, index)
        )
        sub_hall = hallway_state[start:end]
        if any(sub_char != "." for sub_char in sub_hall):
            continue
        room_index = ord(char) - ord("A")
        target_room = side_rooms[room_index]

        if target_room[0] != ".":
            continue
        step_down = step_down_score(target_room, char)
        if not step_down:
            continue
        step_down_modifier, new_room = step_down
        base_score = abs(index - destination) + step_down_modifier
        new_hallway = hallway_state[:]
        new_hallway[index] = "."
        new_rooms = side_rooms[:]
        new_rooms[room_index] = tuple(new_room)
        score = current_score + (base_score * MOVEMENT_COSTS[char])
        assert len(new_rooms) == 4, new_rooms
        assert_valid_state(new_hallway, new_rooms)
        result.append((new_hallway, new_rooms, score))
    return result


def step_down_score(
    side_room: tuple[str, str], expected_char: str
) -> Optional[tuple[int, tuple[str, str]]]:
    score = 0
    assert side_room
    for index, char in enumerate(side_room):
        if char == ".":
            score += 1
            new_room = list(side_room[:])
            new_room[index] = expected_char
        elif char != expected_char or (
            side_room[index:]
            and not set(side_room[index:]).issubset({".", expected_char})
        ):
            return None
        else:
            assert index != 0
            return score, tuple(new_room)
    return score, tuple(new_room)


def pluck_piece_from_side_room(
    room: tuple[str, str], expected_char: str
) -> Optional[tuple[int, str, tuple[str, str]]]:
    score = 0
    if set(room) == {"."}:
        return None
    new_room = room[:]
    for index, char in enumerate(room):
        if char == ".":
            score += 1
            continue
        if char == expected_char:
            remainder = room[index + 1 :]
            if not remainder or set(remainder) == {expected_char}:
                # nothing to pick
                return None
        # pick this one
        new_room = list(room)
        new_room[index] = "."
        score += 1
        return score, char, tuple(new_room)
    return score, char, tuple(new_room)


def move_pieces_to_hall(
    hallway_state: HALL_STATE, side_rooms: ROOM_STATE, current_score: int
) -> list[PUZZLE_STATE]:
    result = []
    for room_index, room in enumerate(side_rooms):
        if set(room) == {"."}:
            # empty
            continue
        target_char = chr(ord("A") + room_index)
        if set(room) == {target_char}:
            # already full
            continue
        plucked = pluck_piece_from_side_room(room, target_char)
        if plucked is None:
            continue
        move_cost, source_char, new_room = plucked
        assert len(new_room) == len(room)
        new_rooms = side_rooms[:room_index] + [new_room] + side_rooms[room_index + 1 :]
        base_new_rooms = new_rooms[:]
        hallway_start = 2 + (room_index * 2)
        base_cost = move_cost
        # start by moving right
        for index in range(hallway_start + 1, HALLWAY_WIDTH):
            move_cost += 1
            if hallway_state[index] != ".":
                # blocked
                break
            if index in DESTINATIONS.values():
                # can't stop here
                if index == DESTINATIONS[source_char]:
                    storage_cost = move_cost
                    # but can we go down?
                    target_room = side_rooms[ROOMS[source_char]]
                    if target_room[0] != ".":
                        # damn, blocked
                        continue
                    step_down = step_down_score(target_room, source_char)
                    if not step_down:
                        continue
                    step_down_modifier, new_target_room = step_down
                    storage_cost += step_down_modifier
                    new_side_rooms = base_new_rooms[:]
                    new_side_rooms[ROOMS[source_char]] = new_target_room
                    assert_valid_state(hallway_state, new_side_rooms)
                    result.append(
                        (
                            hallway_state[:],
                            new_side_rooms,
                            current_score
                            + (MOVEMENT_COSTS[source_char] * storage_cost),
                        )
                    )
                continue
            # now save the intermediate state
            new_hallway = hallway_state[:]
            assert new_hallway[index] == "."
            new_hallway[index] = source_char
            intermediate_cost = current_score + (
                move_cost * MOVEMENT_COSTS[source_char]
            )
            assert len(base_new_rooms) == 4, base_new_rooms
            assert_valid_state(new_hallway, base_new_rooms)
            result.append((new_hallway, base_new_rooms, intermediate_cost))
        # now go left
        move_cost = base_cost
        for index in range(hallway_start - 1, -1, -1):
            move_cost += 1
            try:
                if hallway_state[index] != ".":
                    # blocked
                    break
            except IndexError:
                print(index, hallway_state, hallway_start, room_index, side_rooms)
                raise
            if index in DESTINATIONS.values():
                # can't stop here
                if index == DESTINATIONS[source_char]:
                    storage_cost = move_cost
                    # but can we go down?
                    target_room = side_rooms[ROOMS[source_char]]
                    if target_room[0] != ".":
                        # damn, blocked
                        continue
                    step_down = step_down_score(target_room, source_char)
                    if not step_down:
                        continue
                    step_down_modifier, new_target_room = step_down
                    storage_cost += step_down_modifier

                    new_side_rooms = base_new_rooms[:]
                    new_side_rooms[ROOMS[source_char]] = new_target_room
                    assert len(new_side_rooms) == 4, new_side_rooms
                    assert_valid_state(hallway_state, new_side_rooms)
                    result.append(
                        (
                            hallway_state[:],
                            new_side_rooms,
                            current_score + MOVEMENT_COSTS[source_char] * storage_cost,
                        )
                    )
                continue
            # now save the intermediate state
            new_hallway = hallway_state[:]
            assert new_hallway[index] == "."
            new_hallway[index] = source_char
            intermediate_cost = current_score + move_cost * MOVEMENT_COSTS[source_char]
            assert len(base_new_rooms) == 4, base_new_rooms
            assert_valid_state(new_hallway, base_new_rooms)
            result.append((new_hallway, base_new_rooms, intermediate_cost))
    return result


def move_pieces(
    hallway_state: HALL_STATE, side_rooms: ROOM_STATE, current_score: int
) -> list[PUZZLE_STATE]:
    """Attempt to move pieces, returning all possible candidates that aren't blocked"""
    candidates = move_pieces_from_hall(
        hallway_state, side_rooms, current_score
    ) + move_pieces_to_hall(hallway_state, side_rooms, current_score)
    return candidates


def parse_interim(interim_grid: str) -> PUZZLE_STATE:
    lines = interim_grid.splitlines()
    hallway_state = [char for char in lines[1][1:-1]]
    return hallway_state, tuple(parse_input(lines))


def part_one(puzzle: list[str]) -> int:
    order = parse_input(puzzle)
    print("puzzle is", order)
    queue = Queue()
    min_score = 75000
    states_seen = {}
    test_states_expected = [
        (
            [char for char in "...B......."],
            (("B", "A"), ("C", "D"), (".", "C"), ("D", "A")),
        ),
        (
            [char for char in "...B......."],
            (("B", "A"), (".", "D"), ("C", "C"), ("D", "A")),
        ),
        (
            [char for char in ".....D....."],
            (("B", "A"), (".", "B"), ("C", "C"), ("D", "A")),
        ),
        (
            [char for char in ".....D....."],
            ((".", "A"), ("A", "B"), ("C", "C"), ("D", "A")),
        ),
        (
            [char for char in ".....D.D.A."],
            ((".", "A"), ("B", "B"), ("C", "C"), (".", ".")),
        ),
        (
            [char for char in ".........A."],
            ((".", "A"), ("A", "B"), ("C", "C"), ("D", "D")),
        ),
        (["."] * HALLWAY_WIDTH, (("A", "A"), ("B", "B"), ("C", "C"), ("D", "D"))),
    ]
    p2_states_expected = [
        parse_interim(state)
        for state in """#############
#..........D#
###B#C#B#.###
  #D#C#B#A#
  #D#B#A#C#
  #A#D#C#A#
  #########

#############
#A.........D#
###B#C#B#.###
  #D#C#B#.#
  #D#B#A#C#
  #A#D#C#A#
  #########

#############
#A........BD#
###B#C#.#.###
  #D#C#B#.#
  #D#B#A#C#
  #A#D#C#A#
  #########

#############
#A......B.BD#
###B#C#.#.###
  #D#C#.#.#
  #D#B#A#C#
  #A#D#C#A#
  #########

#############
#AA.....B.BD#
###B#C#.#.###
  #D#C#.#.#
  #D#B#.#C#
  #A#D#C#A#
  #########

#############
#AA.....B.BD#
###B#.#.#.###
  #D#C#.#.#
  #D#B#C#C#
  #A#D#C#A#
  #########

#############
#AA.....B.BD#
###B#.#.#.###
  #D#.#C#.#
  #D#B#C#C#
  #A#D#C#A#
  #########

#############
#AA...B.B.BD#
###B#.#.#.###
  #D#.#C#.#
  #D#.#C#C#
  #A#D#C#A#
  #########

#############
#AA.D.B.B.BD#
###B#.#.#.###
  #D#.#C#.#
  #D#.#C#C#
  #A#.#C#A#
  #########

#############
#AA.D...B.BD#
###B#.#.#.###
  #D#.#C#.#
  #D#.#C#C#
  #A#B#C#A#
  #########

#############
#AA.D.....BD#
###B#.#.#.###
  #D#.#C#.#
  #D#B#C#C#
  #A#B#C#A#
  #########

#############
#AA.D......D#
###B#.#.#.###
  #D#B#C#.#
  #D#B#C#C#
  #A#B#C#A#
  #########

#############
#AA.D......D#
###B#.#C#.###
  #D#B#C#.#
  #D#B#C#.#
  #A#B#C#A#
  #########

#############
#AA.D.....AD#
###B#.#C#.###
  #D#B#C#.#
  #D#B#C#.#
  #A#B#C#.#
  #########

#############
#AA.......AD#
###B#.#C#.###
  #D#B#C#.#
  #D#B#C#.#
  #A#B#C#D#
  #########

#############
#AA.......AD#
###.#B#C#.###
  #D#B#C#.#
  #D#B#C#.#
  #A#B#C#D#
  #########

#############
#AA.......AD#
###.#B#C#.###
  #.#B#C#.#
  #D#B#C#D#
  #A#B#C#D#
  #########

#############
#AA.D.....AD#
###.#B#C#.###
  #.#B#C#.#
  #.#B#C#D#
  #A#B#C#D#
  #########

#############
#A..D.....AD#
###.#B#C#.###
  #.#B#C#.#
  #A#B#C#D#
  #A#B#C#D#
  #########

#############
#...D.....AD#
###.#B#C#.###
  #A#B#C#.#
  #A#B#C#D#
  #A#B#C#D#
  #########

#############
#.........AD#
###.#B#C#.###
  #A#B#C#D#
  #A#B#C#D#
  #A#B#C#D#
  #########

#############
#..........D#
###A#B#C#.###
  #A#B#C#D#
  #A#B#C#D#
  #A#B#C#D#
  #########

#############
#...........#
###A#B#C#D###
  #A#B#C#D#
  #A#B#C#D#
  #A#B#C#D#
  #########""".split(
            "\n\n"
        )
    ]
    print("p2 candidates", p2_states_expected)
    test_states_hit = []
    target = [tuple(char for _ in range(len(order[0]))) for char in "ABCD"]
    print("target is", target)
    for candidate in move_pieces(["."] * HALLWAY_WIDTH, order, 0):
        print(candidate)
        queue.put(list(candidate) + [[]])
    while not queue.empty():
        hallway, side_rooms, score, previous_states = queue.get(block=False)
        for new_hall, new_rooms, new_score in move_pieces(hallway, side_rooms, score):
            assert new_score > score
            if list(new_rooms) == target:
                if new_score < min_score:
                    min_score = new_score
                    continue
            if (list(hallway), tuple(side_rooms)) in p2_states_expected and (
                list(new_hall),
                tuple(new_rooms),
            ) in p2_states_expected:
                print(
                    "p2 candidate",
                    "".join(new_hall),
                    ["".join(i) for i in new_rooms],
                    new_score,
                    "from",
                    "".join(hallway),
                    ["".join(i) for i in side_rooms],
                    score,
                    "steps so far",
                    previous_states,
                )
            dict_key = (tuple(new_hall), tuple(new_rooms))
            try:
                existing_state_score = states_seen[dict_key]
            except KeyError:
                states_seen[dict_key] = new_score
            else:
                # prune stuff we've already seen
                if existing_state_score <= new_score:
                    if (list(new_hall), tuple(new_rooms)) in p2_states_expected:
                        print(
                            "discarding",
                            "".join(new_hall),
                            ["".join(i) for i in new_rooms],
                            f"because {existing_state_score} is better than {new_score}",
                        )
                    continue
                states_seen[dict_key] = new_score
            if (
                puzzle == TEST_INPUT
                and (list(new_hall), tuple(new_rooms)) in test_states_expected
            ):
                print(
                    "found expected state",
                    "".join(new_hall),
                    ["".join(i) for i in new_rooms],
                    new_score,
                    "from",
                    "".join(hallway),
                    score,
                )
                test_states_hit.append((new_hall, new_rooms))
            if (
                puzzle == TEST_PART_TWO_INPUT
                and (list(new_hall), tuple(new_rooms)) in p2_states_expected
            ):
                print(
                    "found p2 expected state",
                    "".join(new_hall),
                    ["".join(i) for i in new_rooms],
                    new_score,
                    "from",
                    "".join(hallway),
                    ["".join(i) for i in side_rooms],
                    score,
                    "steps so far",
                    previous_states,
                )
            if new_score > min_score:
                continue
            queue.put(
                (
                    new_hall,
                    new_rooms,
                    new_score,
                    previous_states
                    + [("".join(hallway), ["".join(i) for i in side_rooms], score)],
                )
            )
    if puzzle == TEST_INPUT:
        print(test_states_hit)
    return min_score


def main():
    assert step_down_score(("A", "B"), "C") is None
    assert step_down_score((".", "A"), "B") is None
    assert step_down_score((".", "A"), "A") == (1, ("A", "A"))
    assert step_down_score((".", "."), "B") == (2, (".", "B")), step_down_score(
        (".", "."), "B"
    )
    assert step_down_score((".", ".", ".", "A"), "A") == (3, (".", ".", "A", "A"))
    assert pluck_piece_from_side_room((".", ".", "A", "B"), "A") == (
        3,
        "A",
        (".", ".", ".", "B"),
    )
    assert pluck_piece_from_side_room((".", ".", "B", "B"), "A") == (
        3,
        "B",
        (".", ".", ".", "B"),
    )
    assert pluck_piece_from_side_room((".", ".", "B", "B"), "B") is None
    assert pluck_piece_from_side_room(("C", "C", "D", "B"), "C") == (
        1,
        "C",
        (".", "C", "D", "B"),
    )
    assert pluck_piece_from_side_room((".", "."), "A") is None
    p1_result = part_one(TEST_INPUT)
    p2_result = part_one(TEST_PART_TWO_INPUT)
    assert p1_result == 12521, p1_result
    assert p2_result == 44169, p2_result
    print(part_one(REAL_INPUT))
    print(part_one(PART_TWO_INPUT))


if __name__ == "__main__":
    main()
