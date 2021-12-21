from collections import Counter
from itertools import product
from dataclasses import dataclass
from typing import Iterable, Literal
from functools import lru_cache

PLAYER_1_TEST_START = 4
PLAYER_2_TEST_START = 8
# your puzzle input
PLAYER_1_START = 7
PLAYER_2_START = 2

PART_2_WIN = 21

PAIR_TYPE = tuple[int, int]

# out of the 27 possible combinations for 3d3, count up their frequencies
# the repeat=3 is because each turn is 3 rolls of the die
FREQUENCIES = Counter(sum(rolls) for rolls in product([1, 2, 3], repeat=3))


@dataclass(frozen=True)
class State:
    positions: PAIR_TYPE
    scores: PAIR_TYPE

    def __init__(self, positions: Iterable[int], scores: Iterable[int]):
        object.__setattr__(self, "positions", tuple(positions))
        object.__setattr__(self, "scores", tuple(scores))


def count(start: int = 1, step: int = 3, loop: int = 100):
        rolls = list(range(start, loop + 1))
        index = 0
        while True:
            next_3_indexes = index, index + 1, index + 2
            try:
                next_3_values = [rolls[i] for i in next_3_indexes]
            except IndexError:
                next_3_values = []
                # approaching the boundary
                for i in (index, index + 1, index + 2):
                    try:
                        next_3_values.append(rolls[i])
                    except IndexError:
                        next_3_values.append(rolls[i % loop])
            yield tuple(next_3_values)
            index += step


def add_pair(pair_one: PAIR_TYPE, pair_two: PAIR_TYPE) -> PAIR_TYPE:
    return pair_one[0] + pair_two[0], pair_one[1] + pair_two[1]


def multiply_by_pair(number: int, pair: PAIR_TYPE) -> PAIR_TYPE:
    return number * pair[0], number * pair[1]


def move(value: int, player: int, state: State) -> State:
    positions = list(state.positions)
    scores = list(state.scores)
    positions[player] = (positions[player] + value) % 10
    if not positions[player]:
        positions[player] = 10
    scores[player] += positions[player]
    return State(positions, scores)


@lru_cache(maxsize=None)
def play(player: Literal[0] | Literal[1], state: State) -> PAIR_TYPE:
    if state.scores[0] >= PART_2_WIN:
        return (1, 0)
    if state.scores[1] >= PART_2_WIN:
        return (0, 1)
    # cheeky way to swap players
    next_player = int(not player)
    p1_wins, p2_wins = (0, 0)
    for total_roll, frequency in FREQUENCIES.items():
        # recursively play through each possible game, using the LRU cache for speed
        played = play(next_player, move(total_roll, player, state))
        # and add the result of the game (multiplied by the frequency of the 3-die outcome)
        # to the game score
        p1_wins, p2_wins = add_pair((p1_wins, p2_wins), multiply_by_pair(frequency, played))
    return p1_wins, p2_wins


def part_two(p1_start: int, p2_start: int) -> int:
    player_1_score, player_2_score = play(0, State([p1_start, p2_start], (0, 0)))
    return max(player_1_score, player_2_score)


def part_one(p1_start: int, p2_start: int, winning_score: int = 1000, die_size: int = 100):
    # this was the horribly naive solution I came up with before discovering LRU cache
    # and the trick
    counter = count(loop=die_size)
    p1_score = 0
    p2_score = 0
    p1_pos = p1_start
    p2_pos = p2_start
    total_rolls = 0
    while p1_score < winning_score and p2_score < winning_score:
        p1_rolls = next(counter)
        p1_pos += sum(p1_rolls)
        total_rolls += 3
        score = p1_pos % 10
        if not score:
            score = 10
        p1_score += score
        if p1_score >= winning_score:
            break
        p2_rolls = next(counter)
        p2_pos += sum(p2_rolls)
        score = p2_pos % 10
        if not score:
            score = 10
        p2_score += score
        total_rolls += 3

    print(f'Game over: p1 score {p1_score}, p2 {p2_score} after {total_rolls} rolls')
    return total_rolls * min(p1_score, p2_score)


def main():
    test_game = part_one(PLAYER_1_TEST_START, PLAYER_2_TEST_START)
    assert test_game == 739785, test_game
    test_long_game = part_two(PLAYER_1_TEST_START, PLAYER_2_TEST_START)
    assert test_long_game == 444356092776315, test_long_game
    real_game = part_one(PLAYER_1_START, PLAYER_2_START)
    print(real_game)
    print(part_two(PLAYER_1_START, PLAYER_2_START))


if __name__ == '__main__':
    main()
