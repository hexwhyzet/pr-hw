import copy
import re
from dataclasses import dataclass
from enum import Enum

MIN_GAME_SIZE = 2
MAX_GAME_SIZE = 9


@dataclass
class Cell(Enum):
    EMPTY = 0
    NOUGHT = 1
    CROSS = 2


class Game:
    def __init__(self, size=None, is_cross_turn=True, field=None):
        if field is not None:
            if size is None:
                size = len(field)
            assert len(field) == size
            for i in range(len(field)):
                assert len(field[i]) == size
            crosses = 0
            noughts = 0
            for i in range(size):
                for j in range(size):
                    if field[i][j] is Cell.CROSS:
                        crosses += 1
                    if field[i][j] is Cell.NOUGHT:
                        noughts += 1
            assert crosses - noughts in [0, 1]
            self.size = size
            self.field = field
            self.is_cross_turn = crosses - noughts == 0
            return
        assert size >= MIN_GAME_SIZE
        assert size <= MAX_GAME_SIZE
        self.size = size
        self.field = [[Cell.EMPTY for _ in range(size)] for _ in range(size)]
        self.is_cross_turn = is_cross_turn

    def __hash__(self):
        flat_list = list(map(lambda x: str(x.value), flatten(self.field)))
        flat_list.append(str(self.is_cross_turn))
        return hash(''.join(flat_list))

    def __eq__(self, other):
        return self.__hash__() == other.__hash__()

    def is_empty_cell(self, x, y):
        return self.field[y][x] is Cell.EMPTY

    def turn(self, x, y, inplace=False):
        if self.field[y][x] is not Cell.EMPTY:
            raise Exception
        if inplace:
            self.field[y][x] = Cell.CROSS if self.is_cross_turn else Cell.NOUGHT
            self.is_cross_turn = not self.is_cross_turn
            return self
        new_field = copy.deepcopy(self.field)
        new_field[y][x] = Cell.CROSS if self.is_cross_turn else Cell.NOUGHT
        return Game(field=new_field, is_cross_turn=not self.is_cross_turn)

    def possible_turns(self):
        for x in range(self.size):
            for y in range(self.size):
                if self.field[y][x] is Cell.EMPTY:
                    yield self.turn(x, y)

    def ended(self):
        if self.winner() is not None:
            return True
        any_empty = False
        for i in range(self.size):
            for j in range(self.size):
                if self.field[i][j] is Cell.EMPTY:
                    any_empty = True
        return not any_empty

    def winner(self):
        for y in range(self.size):
            for cell_type in [Cell.CROSS, Cell.NOUGHT]:
                if all(map(lambda cell: cell is cell_type, self.field[y])):
                    return cell_type
        for x in range(self.size):
            for cell_type in [Cell.CROSS, Cell.NOUGHT]:
                if all(map(lambda cell: cell is cell_type, [self.field[y][x] for y in range(self.size)])):
                    return cell_type
        for cell_type in [Cell.CROSS, Cell.NOUGHT]:
            if all(map(lambda cell: cell is cell_type, [self.field[y][y] for y in range(self.size)])):
                return cell_type
            if all(map(lambda cell: cell is cell_type, [self.field[y][self.size - y - 1] for y in range(self.size)])):
                return cell_type

    def __repr__(self):
        def s(length, ch=" "):
            return ch * length

        def val_to_sign(val):
            if val == 0:
                return "-"
            elif val == 1:
                return "O"
            else:
                return "X"

        lines = []
        cell_width = 5
        cell_height = 3
        header = s(cell_width // 2 + 1) + s(cell_width).join(list(map(str, range(1, self.size + 1)))) + s(
            cell_width // 2)
        lines.append(header)
        for i in range(self.size):
            for j in range(cell_height):
                if j == cell_height // 2:
                    prefix = str(i + 1)
                    space_ch = " "
                    content = list(map(lambda x: val_to_sign(x.value), self.field[i]))
                elif j == cell_height - 1:
                    prefix = " "
                    if i == self.size - 1 and j == cell_height - 1:
                        space_ch = " "
                        content = [" "] * self.size
                    else:
                        space_ch = "_"
                        content = ["_"] * self.size
                else:
                    prefix = " "
                    space_ch = " "
                    content = [" "] * self.size
                spacer = s(cell_width // 2, ch=space_ch)
                lines.append(prefix + spacer + (spacer + "|" + spacer).join(content) + spacer)
        return "\n".join(lines)


class Minimax:
    __best_turn = dict()
    __cache = [dict(), dict()]

    def get_cache(self, game: Game, is_bot_turn: bool) -> int:
        if game in self.__cache[is_bot_turn].keys():
            return self.__cache[is_bot_turn][game]
        if game in self.__cache[not is_bot_turn].keys():
            return -self.__cache[not is_bot_turn][game]

    def add_cache(self, game, is_bot_turn, weight):
        self.__cache[is_bot_turn][game] = weight

    def does_cache_exist(self, game, is_bot_turn):
        return game in self.__cache[is_bot_turn].keys() or game in self.__cache[not is_bot_turn].keys()

    def __init__(self, size, is_bot_turn_first=False):
        self.bot_cell_type = Cell.CROSS if is_bot_turn_first else Cell.NOUGHT
        init_game = Game(size=size)
        self.__recursive_init(init_game, is_bot_turn_first)

    def __recursive_init(self, game, is_bot_turn):
        if self.does_cache_exist(game, is_bot_turn):
            return self.get_cache(game, is_bot_turn)

        winner = game.winner()
        if winner is not None:
            if is_bot_turn:
                return -1
            else:
                return 1

        min_weight = float('+inf')
        min_outcome = None
        max_weight = float('-inf')
        max_outcome = None
        for outcome in game.possible_turns():
            weight = self.__recursive_init(outcome, not is_bot_turn)
            self.add_cache(outcome, not is_bot_turn, weight)
            if min_weight > weight:
                min_weight = weight
                min_outcome = outcome
            if max_weight < weight:
                max_weight = weight
                max_outcome = outcome

        if min_outcome is None or max_outcome is None:
            return 0
        if is_bot_turn:
            self.__best_turn[game] = max_outcome
            return max_weight
        else:
            return min_weight

    def best_turn(self, game):
        if game not in self.__best_turn.keys():
            raise Exception
        return self.__best_turn[game]

    def debug(self):
        for key, val in self.__best_turn.items():
            try:
                print(self.get_cache(key, True))
            except:
                raise Exception
            print(key)
            print(val)
            print("\n" * 3)


def flatten(target_list):
    return [item for sublist in target_list for item in sublist]


def incorrect_input(message):
    ans = "Incorrect input"
    if message:
        ans += ": " + str(message)
    print(ans)


if __name__ == '__main__':
    inp_size = 0
    while (not (inp_size := input("Enter game size: ")).isdigit()) or (
            not MIN_GAME_SIZE <= int(inp_size) <= MAX_GAME_SIZE):
        incorrect_input(f"please enter the number in range [{MIN_GAME_SIZE}-{MAX_GAME_SIZE}]")
    inp_parity = 0
    while (not (inp_parity := input("First move (0 - you, 1 - robot): ")).isdigit()) or (not int(inp_parity) in [0, 1]):
        incorrect_input("please enter the number 0 or 1")
    game = Game(size=int(inp_size))
    minimax = Minimax(size=int(inp_size), is_bot_turn_first=bool(int(inp_parity)))

    if bool(int(inp_parity)):
        game = minimax.best_turn(game)

    while not game.ended():
        print(game)
        move_regexp = rf"^[1-{game.size}]\s[1-{game.size}]$"
        inp_turn = ""
        coords = [0, 0]
        while (not (inp_turn := input("Select cell (two numbers x and y): "))) or (
                not re.match(move_regexp, inp_turn.strip())) or (
                not (coords := list(map(lambda x: int(x) - 1, inp_turn.strip().split())))) or (
                not game.is_empty_cell(coords[0], coords[1])):
            incorrect_input(f"please enter the numbers x and y in range [1-{game.size}], cell should be empty")
        game = game.turn(coords[0], coords[1])
        if not game.ended():
            game = minimax.best_turn(game)

    print(game)
    winner = game.winner()
    if winner is minimax.bot_cell_type:
        print("Destiny of losers is to lose. You lost.")
    elif winner is None:
        print("This time draw...")
    else:
        print("What? You are lucky bastard! You won.")
