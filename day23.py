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
    amphis = [char for line in puzzle[2:4] for char in line if char in set("ABCD")]
    return list(zip(amphis[:4], amphis[4:]))


def assert_valid_state(hallway, side_rooms):
    count = Counter(hallway)
    for room in side_rooms:
        count += Counter(room)
    for index, char in enumerate(hallway):
        if index in {2, 4, 6, 8}:
            assert char == ".", (index, char)
    assert all(val == 2 for key, val in count.items() if key != "."), (
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
        elif char != expected_char:
            return None
        else:
            assert index != 0
            return score, tuple(new_room)
    return score, tuple(new_room)


def move_pieces_to_hall(
    hallway_state: HALL_STATE, side_rooms: ROOM_STATE, current_score: int
) -> list[PUZZLE_STATE]:
    result = []
    for room_index, room in enumerate(side_rooms):
        if room == (".", "."):
            # empty
            continue
        target_char = chr(ord("A") + room_index)
        if room == (target_char, target_char):
            # already full
            continue
        move_cost = 0
        if room[0] != ".":
            source_char = room[0]
            move_cost += 1
            new_room = (".", room[1])
        else:
            source_char = room[1]
            new_room = (".", ".")
            move_cost += 2
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


def part_one(puzzle: list[str]) -> int:
    order = parse_input(puzzle)
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
    test_states_hit = []
    target = [("A", "A"), ("B", "B"), ("C", "C"), ("D", "D")]
    for candidate in move_pieces(["."] * HALLWAY_WIDTH, order, 0):
        print(candidate)
        queue.put(candidate)
    while not queue.empty():
        hallway, side_rooms, score = queue.get(block=False)
        for new_hall, new_rooms, new_score in move_pieces(hallway, side_rooms, score):
            assert new_score > score
            if list(new_rooms) == target:
                print("win", new_score)
                if new_score < min_score:
                    min_score = new_score
                    continue
            dict_key = (tuple(new_hall), tuple(new_rooms))
            try:
                existing_state_score = states_seen[dict_key]
            except KeyError:
                states_seen[dict_key] = new_score
            else:
                # prune stuff we've already seen
                if existing_state_score <= new_score:
                    continue
                states_seen[dict_key] = new_score
            if (
                puzzle == TEST_INPUT
                and (list(new_hall), tuple(new_rooms)) in test_states_expected
            ):
                print("found expected state", new_hall, new_rooms, score)
                test_states_hit.append((new_hall, new_rooms))
            if new_score > min_score:
                continue
            queue.put((new_hall, new_rooms, new_score))
    if puzzle == TEST_INPUT:
        print(test_states_hit)
    return min_score
    # 15324 is too high
    # 11326 is too low
    # visually solving this even though I know it's a trap for part 2
    # 1. Move upper A to the second left
    # #.A.........#
    # ###B#D#C#.###
    #   #C#D#B#A#
    #   #########
    cost = 9
    # 2. move lower A to second right
    # #.A.......A.#
    # ###B#D#C#.###
    #   #C#D#B#.#
    #   #########
    cost += 3
    # 3. move each D into its hallway
    # #.A.......A.#
    # ###B#.#C#D###
    #   #C#.#B#D#
    #   #########
    cost += 7000
    cost += 7000
    # 4; move the B that's in hallway A into its hallway
    # #.A.......A.#
    # ###.#.#C#D###
    #   #C#B#B#D#
    #   #########
    cost += 50
    # 5. Move the C that's on top of the B up and to the right
    # #.A.....C..#
    # ###.#.#.#D###
    #   #C#B#B#D#
    #   #########
    cost += 200
    # 6. Move the B that was underneath it into its hallway
    # #.A.....C.A.#
    # ###.#B#.#D###
    #   #C#B#.#D#
    #   #########
    cost += 50
    # 7. move that C back into its hallway
    # #.A.......A.#
    # ###.#B#.#D###
    #   #C#B#C#D#
    #   #########
    cost += 300
    # 8. move the last C from the A column into its hallway
    # #.A.......A.#
    # ###.#B#C#D###
    #   #.#B#C#D#
    #   #########
    cost += 700
    # 9. move the first A into its hallway
    # #.........A.#
    # ###.#B#C#D###
    #   #A#B#C#D#
    #   #########
    cost += 3
    # 10. Move the second A into its hallway
    # #...........#
    # ###A#B#C#D###
    #   #A#B#C#D#
    #   #########
    cost += 9
    return cost


def main():
    assert step_down_score(("A", "B"), "C") is None
    assert step_down_score((".", "A"), "B") is None
    assert step_down_score((".", "A"), "A") == (1, ("A", "A"))
    assert step_down_score((".", "."), "B") == (2, (".", "B")), step_down_score(
        (".", "."), "B"
    )
    assert step_down_score((".", ".", ".", "A"), "A") == (3, (".", ".", "A", "A"))
    p1_result = part_one(TEST_INPUT)
    # p2_result = part_one(TEST_PART_TWO_INPUT)
    assert p1_result == 12521, p1_result
    # assert p2_result == 44169, p2_result
    print(part_one(REAL_INPUT))
    # print(part_one(PART_TWO_INPUT))


if __name__ == "__main__":
    main()
