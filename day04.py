from typing import Iterable


TEST_INPUT = """7,4,9,5,11,17,23,2,0,14,21,24,10,16,13,6,15,25,12,22,18,20,8,19,3,26,1

22 13 17 11  0
 8  2 23  4 24
21  9 14 16  7
 6 10  3 18  5
 1 12 20 15 19

 3 15  0  2 22
 9 18 13 17  5
19  8  7 25 23
20 11 10 24  4
14 21 16 12  6

14 21 17 24  4
10 16 15  9 19
18  8 23 26 20
22 11 13  6  5
 2  0 12  3  7""".splitlines()

BOARD_WIDTH = 5


class Board:
    def __init__(self, board: Iterable[str]) -> None:

        raw_board = [[int(i) for i in line.split() if i] for line in board if line]
        self.state = {}
        self.board = {}
        for y, row in enumerate(raw_board):
            for x, number in enumerate(row):
                self.board[x, y] = number
                self.state[x, y] = False
        self.reverse_board = {
            position: number for number, position in self.board.items()
        }
        assert all(
            (x, y) in self.state for x in range(BOARD_WIDTH) for y in range(BOARD_WIDTH)
        ), (board, self.state, raw_board)

    def score(self) -> int:
        score = 0
        for pos, state in self.state.items():
            if not state:
                score += self.board[pos]
        return score

    def draw(self, number) -> bool:
        try:
            x, y = self.reverse_board[number]
        except KeyError:
            return False
        self.state[x, y] = True
        return True

    def is_winner(self) -> bool:
        if any(
            # h & v
            (
                all(self.state[0, y] for y in range(BOARD_WIDTH)),
                all(self.state[1, y] for y in range(BOARD_WIDTH)),
                all(self.state[2, y] for y in range(BOARD_WIDTH)),
                all(self.state[3, y] for y in range(BOARD_WIDTH)),
                all(self.state[4, y] for y in range(BOARD_WIDTH)),
                all(self.state[x, 0] for x in range(BOARD_WIDTH)),
                all(self.state[x, 1] for x in range(BOARD_WIDTH)),
                all(self.state[x, 2] for x in range(BOARD_WIDTH)),
                all(self.state[x, 3] for x in range(BOARD_WIDTH)),
                all(self.state[x, 4] for x in range(BOARD_WIDTH)),
            )
        ):
            return True
        return False

    def __str__(self):
        result = []
        for y in range(BOARD_WIDTH):
            row = []
            for x in range(BOARD_WIDTH):
                number = self.board[x, y]
                state = self.board[x, y]
                row.append(f'{number}{"*" if state else ""}')
            result.append(row)
        result.append([f"score: {self.score()}"])
        return "\n".join(" ".join(line) for line in result)


class Bingo:
    def __init__(self, puzzle: Iterable[str], part_two: bool = False):
        puzzle = list(puzzle)
        self.draws = [int(i) for i in puzzle[0].split(",")]
        assert not puzzle[1]
        # each group of 6 (blank + 5) is a board
        assert not len(puzzle[1:]) % 6
        self.boards: list[Board] = []
        for puzzle_start in range(1, len(puzzle), 6):
            next_board = puzzle[puzzle_start : puzzle_start + 6]
            self.boards.append(Board(next_board))
        self.part_two = part_two

    def go(self) -> int:
        most_recent_winner = None
        most_recent_draw = None
        for draw in self.draws:
            hits = [
                board
                for board in self.boards
                if not board.is_winner() and board.draw(draw)
            ]
            winners = [board for board in hits if board.is_winner()]
            if len(winners) == 1:
                most_recent_winner = winners[0]
                most_recent_draw = draw
            if winners:
                if not self.part_two:
                    assert len(winners) == 1
                    return winners[0].score() * draw
                else:
                    if len(winners) == len(self.boards):
                        assert most_recent_draw is not None
                        assert most_recent_winner is not None
                        return most_recent_winner.score() * most_recent_draw
        if self.part_two:
            assert most_recent_draw is not None
            assert most_recent_winner is not None
            return most_recent_winner.score() * most_recent_draw
        raise ValueError("no winner found?")


def part_one(puzzle_input: Iterable[str], part_two: bool = False) -> int:
    game = Bingo(puzzle=puzzle_input, part_two=part_two)
    return game.go()


def main():
    part_one_result = part_one(TEST_INPUT)
    assert part_one_result == 188 * 24, part_one_result
    part_two_result = part_one(TEST_INPUT, True)
    assert part_two_result == 148 * 13, part_two_result
    with open("day04.txt") as infile:
        game = [line.strip() for line in infile]
    print(part_one(game))
    print(part_one(game, True))


if __name__ == "__main__":
    main()
