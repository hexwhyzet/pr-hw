import copy
from dataclasses import dataclass
from enum import Enum


@dataclass
class Cell(Enum):
    EMPTY = 0
    NOUGHT = 1
    CROSS = 2


class Minimax:
    __best_turn = dict()

    def __init__(self, size, is_bot_turn_first=False):
        self.bot_cell_type = Cell.CROSS if is_bot_turn_first else Cell.NOUGHT
        init_game = Game(size=size)
        self.__recursive_init(init_game, is_bot_turn_first)

    def __recursive_init(self, game, is_bot_turn):
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
            if min_weight > weight:
                min_outcome = outcome
            if max_weight < weight:
                max_outcome = outcome

        if min_outcome is None or max_outcome is None:
            return 0
        if is_bot_turn:
            self.__best_turn[game] = max_outcome
            return max_weight
        else:
            return min_weight

    def best_turn(self, game):
        if game not in self.__best_turn:
            raise Exception
        return self.__best_turn[game]


class Game:
    def __init__(self, size=None, is_cross_turn=True, field=None):
        if field is not None:
            if size is None:
                size = len(field)
            assert len(field) == size
            for i in range(len(field)):
                assert len(field[i]) == size
            self.size = size
            self.field = field
            self.is_cross_turn = is_cross_turn
        assert size > 2
        self.size = size
        self.field = [[Cell.EMPTY for _ in range(size)] for _ in range(size)]
        self.is_cross_turn = is_cross_turn

    def __hash__(self):
        return hash(''.join(map(lambda x: ''.join(x), self.field)) + str(self.is_cross_turn))

    def turn(self, x, y, inplace=False):
        if self.field[y][x].value != Cell.EMPTY:
            raise Exception
        if inplace:
            self.field[y][x].value = Cell.CROSS if self.is_cross_turn else Cell.NOUGHT
            self.is_cross_turn = not self.is_cross_turn
            return self
        new_field = copy.deepcopy(self.field)
        new_field[y][x] = Cell.CROSS if self.is_cross_turn else Cell.NOUGHT
        return Game(field=new_field, is_cross_turn=not self.is_cross_turn)

    def possible_turns(self):
        for x in range(self.size):
            for y in range(self.size):
                if self.field[y][x].value != Cell.EMPTY:
                    yield self.turn(x, y)

    def winner(self):
        for y in range(self.size):
            for cell_type in [Cell.CROSS, Cell.NOUGHT]:
                if all(map(lambda cell: cell.value == cell_type, self.field[y])):
                    return cell_type
        for x in range(self.size):
            for cell_type in [Cell.CROSS, Cell.NOUGHT]:
                if all(map(lambda cell: cell.value == cell_type, [self.field[y][x] for y in range(self.size)])):
                    return cell_type


if __name__ == '__main__':
    minimax = Minimax(3, True)
    test = 5
