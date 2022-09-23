import unittest

from tic_tac_toe import Cell, Game


class TestStringMethods(unittest.TestCase):
    def test_turn(self):
        game1 = Game(size=3).turn(0, 0)
        game2 = Game(field=[[Cell.CROSS, Cell.EMPTY, Cell.EMPTY],
                            [Cell.EMPTY, Cell.EMPTY, Cell.EMPTY],
                            [Cell.EMPTY, Cell.EMPTY, Cell.EMPTY]])
        self.assertEqual(game1, game2)

    def test_inplace_turn(self):
        game1 = Game(size=3)
        game2 = game1.turn(0, 0, inplace=True)
        self.assertEqual(game1, game2)

    def test_winner(self):
        game1 = Game(field=[[Cell.CROSS, Cell.EMPTY, Cell.EMPTY],
                            [Cell.NOUGHT, Cell.CROSS, Cell.EMPTY],
                            [Cell.NOUGHT, Cell.EMPTY, Cell.CROSS]])
        game2 = Game(field=[[Cell.NOUGHT, Cell.NOUGHT, Cell.NOUGHT],
                            [Cell.CROSS, Cell.CROSS, Cell.EMPTY],
                            [Cell.EMPTY, Cell.EMPTY, Cell.CROSS]])
        game3 = Game(field=[[Cell.CROSS, Cell.NOUGHT, Cell.EMPTY],
                            [Cell.CROSS, Cell.NOUGHT, Cell.CROSS],
                            [Cell.EMPTY, Cell.NOUGHT, Cell.CROSS]])
        game4 = Game(field=[[Cell.CROSS, Cell.NOUGHT, Cell.EMPTY],
                            [Cell.CROSS, Cell.EMPTY, Cell.EMPTY],
                            [Cell.EMPTY, Cell.NOUGHT, Cell.CROSS]])
        self.assertEqual(game1.winner().value, Cell.CROSS.value)
        self.assertEqual(game2.winner().value, Cell.NOUGHT.value)
        self.assertEqual(game3.winner().value, Cell.NOUGHT.value)
        self.assertEqual(game4.winner(), None)

    def test_possible_turns(self):
        game = Game(field=[[Cell.CROSS, Cell.CROSS, Cell.EMPTY],
                           [Cell.NOUGHT, Cell.CROSS, Cell.NOUGHT],
                           [Cell.NOUGHT, Cell.NOUGHT, Cell.CROSS]])
        game_correct = Game(field=[[Cell.CROSS, Cell.CROSS, Cell.CROSS],
                                   [Cell.NOUGHT, Cell.CROSS, Cell.NOUGHT],
                                   [Cell.NOUGHT, Cell.NOUGHT, Cell.CROSS]])
        possible_turns = list(game.possible_turns())
        self.assertEqual(len(possible_turns), 1)
        self.assertEqual(game.turn(2, 0), possible_turns[0])
        self.assertEqual(game_correct, possible_turns[0])

    def test_is_empty(self):
        game = Game(field=[[Cell.CROSS, Cell.CROSS, Cell.EMPTY],
                           [Cell.NOUGHT, Cell.CROSS, Cell.NOUGHT],
                           [Cell.NOUGHT, Cell.NOUGHT, Cell.CROSS]])
        self.assertEqual(game.is_empty_cell(1, 1), False)
        self.assertEqual(game.is_empty_cell(2, 0), True)


if __name__ == '__main__':
    unittest.main()
