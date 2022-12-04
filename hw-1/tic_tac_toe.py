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


# предложение: мне кажется, хорошо в питоне использовать аннотации переменных
def calculate_cell_type(field, cell_type: Cell) -> int:
    final_amount = 0
    for i in range(len(field)):
        final_amount += field[i].count(cell_type)
    return final_amount


def is_field_correct(field, size):
    if field is not None:
        if size is None:
            size = len(field)
        assert len(field) == size
        for i in range(len(field)):
            assert len(field[i]) == size
        crosses_count = calculate_cell_type(field, Cell.CROSS)
        noughts_count = calculate_cell_type(field, Cell.NOUGHT)
        assert crosses_count - noughts_count in [0, 1]
        return True
    assert size >= MIN_GAME_SIZE
    assert size <= MAX_GAME_SIZE
    return True


# предложение: можно классы вынести в отдельный файлик для читабельности, а потом их импортить
class Game:
    def __init__(self, size=None, is_cross_turn=True, field=None):
        if is_field_correct(field, size):
            self.size = size
            self.field = field
            crosses_count = calculate_cell_type(field, Cell.CROSS)
            noughts_count = calculate_cell_type(field, Cell.NOUGHT)
            self.is_cross_turn = crosses_count - noughts_count == 0
        else:
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

    def is_over(self):
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
        def duplicate_char(length, char=" "):  # очень хочется другое имя переменной
            return char * length

        def val_to_sign(val):  # тут тоже
            if val == 0:
                return "-"
            elif val == 1:
                return "O"
            else:
                return "X"

        lines = []
        cell_width = 5
        cell_height = 3
        header = duplicate_char(cell_width // 2 + 1) + duplicate_char(cell_width).join(
            list(map(str, range(1, self.size + 1)))) + duplicate_char(
            cell_width // 2)
        lines.append(header)
        for i in range(self.size):
            for j in range(cell_height):
                if j == cell_height // 2:
                    prefix = str(i + 1)
                    space_char = " "
                    content = list(map(lambda x: val_to_sign(x.value), self.field[i]))
                elif j == cell_height - 1:
                    prefix = " "
                    if i == self.size - 1 and j == cell_height - 1:
                        space_char = " "
                        content = [" "] * self.size
                    else:
                        space_char = "_"
                        content = ["_"] * self.size
                else:
                    prefix = " "
                    space_char = " "
                    content = [" "] * self.size
                spacer = duplicate_char(cell_width // 2, char=space_char)
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
        for key, value in self.__best_turn.items():
            try:
                print(self.get_cache(key, True))
            except:
                raise Exception
            print(key)
            print(value)
            print("\n" * 3)


def flatten(target_list):
    return [item for sublist in target_list for item in sublist]


def incorrect_input(message):
    ans = "Incorrect input"
    if message:
        ans += ": " + str(message)
    print(ans)


if __name__ == '__main__':
    input_size = 0
    # предложение: выделить этот условие while в отдельную функцию типа is_input_fieldsize_correct но вообще,
    # наверное, даже весь этот кусок кода хочется закинуть в одну функцию: start_game/request_initial_input + тяжело
    # читать постоянные приведения к int, мб закинуть полученный input в отдельную переменную и один раз её привести
    # к инту?
    while (not (input_size := input("Enter game size: ")).isdigit()) or (
            not MIN_GAME_SIZE <= int(input_size) <= MAX_GAME_SIZE):
        incorrect_input(f"please enter the number in range [{MIN_GAME_SIZE}-{MAX_GAME_SIZE}]")
    inp_parity = 0  # ???, мне кажется, стоит придумать другое имя, input_first_player (?)
    # предложение: выделить этот условие while в отдельную функцию типа is_input_whoisturn_correct, хз
    while (not (inp_parity := input("First move (0 - you, 1 - robot): ")).isdigit()) or (not int(inp_parity) in [0, 1]):
        incorrect_input("please enter the number 0 or 1")
    game = Game(size=int(input_size))
    minimax = Minimax(size=int(input_size), is_bot_turn_first=bool(int(inp_parity)))

    if bool(int(inp_parity)):
        game = minimax.best_turn(game)

    while not game.is_over():
        print(game)
        move_regexp = rf"^[1-{game.size}]\s[1-{game.size}]$"
        input_turn = ""
        coords = [0, 0]
        # всё ещё хочется всё условие while закинуть в отдельную функцию
        while (not (input_turn := input("Select cell (two numbers x and y): "))) or (
                not re.match(move_regexp, input_turn.strip())) or (
                not (coords := list(map(lambda x: int(x) - 1, input_turn.strip().split())))) or (
                not game.is_empty_cell(coords[0], coords[1])):
            incorrect_input(f"please enter the numbers x and y in range [1-{game.size}], cell should be empty")
        game = game.turn(coords[0], coords[1])
        if not game.is_over():
            game = minimax.best_turn(game)

    print(game)
    winner = game.winner()
    if winner is minimax.bot_cell_type:
        print("Destiny of losers is to lose. You lost.")
    elif winner is None:
        print("This time draw...")
    else:
        print("What? You are lucky bastard! You won.")
