from board.board import Board
import unittest
from exceptions.exceptions import InputError
from game.game import Game
from validators.validators import ValidateBoard


class TestBoard(unittest.TestCase):
    def setUp(self) -> None:
        self._board = Board(6, 7)

    def tearDown(self) -> None:
        pass

    def test_getters(self):
        self.assertEqual(self._board.get_number_of_rows, 6)
        self.assertEqual(self._board.get_number_of_columns, 7)

    def test_get_board_position(self):
        self._board._board[2][0] = 2
        self._board._board[4][2] = 1
        self.assertEqual(self._board.get_board_value(2, 0), 2)
        self.assertEqual(self._board.get_board_value(4, 2), 1)
        self.assertEqual(self._board.get_board_value(0, 0), 0)

    def test_create_board(self):
        rows = self._board.get_number_of_rows
        columns = self._board.get_number_of_columns
        for row in range(rows):
            for column in range(columns):
                self.assertEqual(self._board.get_board_value(row, column), 0)

    def test_drop_piece(self):
        self.assertEqual(self._board.get_board_value(1, 0), 0)
        self._board.drop_piece_on_board(1, 0, 2)
        self.assertEqual(self._board.get_board_value(1, 0), 2)
        self.assertEqual(self._board.get_board_value(2, 4), 0)
        self._board.drop_piece_on_board(2, 4, 1)
        self.assertEqual(self._board.get_board_value(2, 4), 1)

    def test_is_valid_location(self):
        column = 0
        self.assertTrue(self._board.is_valid_column(column))
        rows = self._board.get_number_of_rows
        for row in range(rows-1):
            self._board.drop_piece_on_board(row, column, 2)
        self.assertTrue(self._board.is_valid_column(column))
        self._board.drop_piece_on_board(int(rows) - 1, column, 2)
        self.assertFalse(self._board.is_valid_column(column))

    def test_get_next_open_row(self):
        column = 5
        self.assertEqual(self._board.get_next_available_row(column), 0)
        self._board.drop_piece_on_board(0, column, 1)
        self._board.drop_piece_on_board(1, column, 1)
        self._board.drop_piece_on_board(2, column, 1)
        self.assertEqual(self._board.get_next_available_row(column), 3)
        self._board.drop_piece_on_board(3, column, 1)
        self.assertEqual(self._board.get_next_available_row(column), 4)

    def test_get_board_copy(self):
        self._board.drop_piece_on_board(0, 0, 1)
        self._board.drop_piece_on_board(0, 1, 2)
        self._board.drop_piece_on_board(4, 0, 1)
        self._board.drop_piece_on_board(1, 0, 2)
        self._board.drop_piece_on_board(5, 0, 1)
        self._board.drop_piece_on_board(5, 1, 2)
        self._board.drop_piece_on_board(5, 2, 1)
        board_copy = self._board.get_board_copy()
        rows = self._board.get_number_of_rows
        columns = self._board.get_number_of_columns
        for row in range(rows):
            for column in range(columns):
                self.assertEqual(board_copy.get_board_value(row, column), self._board.get_board_value(row, column))

    def test_winning_move(self):
        # test horizontal
        self._board.drop_piece_on_board(1, 0, 2)
        self._board.drop_piece_on_board(2, 0, 2)
        self._board.drop_piece_on_board(3, 0, 2)
        self._board.drop_piece_on_board(4, 0, 2)
        self.assertTrue(self._board.is_winning_move(2))

        # test vertical
        self._board.drop_piece_on_board(5, 0, 1)
        self._board.drop_piece_on_board(5, 1, 1)
        self._board.drop_piece_on_board(5, 2, 1)
        self._board.drop_piece_on_board(5, 3, 1)
        self.assertTrue(self._board.is_winning_move(1))

        # test diagonals positively sloped
        self._board.drop_piece_on_board(1, 0, 3)
        self._board.drop_piece_on_board(2, 1, 3)
        self._board.drop_piece_on_board(3, 2, 3)
        self._board.drop_piece_on_board(4, 3, 3)
        self.assertTrue(self._board.is_winning_move(3))

        # test diagonals positively sloped
        self._board.drop_piece_on_board(5, 2, 4)
        self._board.drop_piece_on_board(4, 3, 4)
        self._board.drop_piece_on_board(3, 4, 4)
        self._board.drop_piece_on_board(2, 5, 4)
        self.assertTrue(self._board.is_winning_move(4))

    def test_is_board_full(self):
        self.assertFalse(self._board.is_board_full())
        rows = self._board.get_number_of_rows
        columns = self._board.get_number_of_columns
        for row in range(rows):
            for column in range(columns):
                self._board.drop_piece_on_board(row, column, 2)
        self.assertTrue(self._board.is_board_full())

    def test_get_valid_locations(self):
        rows = self._board.get_number_of_rows
        columns = self._board.get_number_of_columns
        valid_locations = self._board.get_available_locations()
        self.assertEqual(len(valid_locations), columns)
        for row in range(rows):
            self._board.drop_piece_on_board(row, 5, 1)
        valid_locations = self._board.get_available_locations()
        self.assertEqual(len(valid_locations), columns-1)
        for row in range(rows):
            self._board.drop_piece_on_board(row, 4, 2)
        valid_locations = self._board.get_available_locations()
        self.assertEqual(len(valid_locations), columns-2)
        for row in range(rows):
            for column in range(columns):
                self._board.drop_piece_on_board(row, column, 3)
        valid_locations = self._board.get_available_locations()
        self.assertEqual(len(valid_locations), 0)


class TestValidators(unittest.TestCase):
    def setUp(self) -> None:
        self._board = Board(6, 7)
        self._validator = ValidateBoard()

    def tearDown(self) -> None:
        pass

    def test_validate_move(self):
        with self.assertRaises(InputError) as ie:
            self._validator.validate_move('a')
        self.assertEqual(str(ie.exception), "Invalid move! Must be an integer between 0 and 6!\n")
        with self.assertRaises(InputError) as ie:
            self._validator.validate_move(-1)
        self.assertEqual(str(ie.exception), "Invalid move! Must be an integer between 0 and 6!\n")
        with self.assertRaises(InputError) as ie:
            self._validator.validate_move(8)
        self.assertEqual(str(ie.exception), "Invalid move! Must be an integer between 0 and 6!\n")


class TestGame(unittest.TestCase):
    def setUp(self) -> None:
        self._game = Game(Board(6, 7), ValidateBoard)

    def tearDown(self) -> None:
        pass

    def test_getters(self):
        board = self._game.get_board
        self.assertEqual(board.get_board_value(0, 0), 0)
        self.assertEqual(board.get_board_value(5, 0), 0)
        validator = self._game.get_validator
        with self.assertRaises(InputError) as ie:
            validator.validate_move('a')
        self.assertEqual(str(ie.exception), "Invalid move! Must be an integer between 0 and 6!\n")

    def test_move_human(self):
        self._game.move_human(1)
        board = self._game.get_board
        self.assertEqual(board.get_board_value(0, 1), 1)
        self._game.move_human(5)
        board = self._game.get_board
        self.assertEqual(board.get_board_value(0, 5), 1)
        self._game.move_human(5)
        board = self._game.get_board
        self.assertEqual(board.get_board_value(1, 5), 1)
        self._game.move_human(5)
        board = self._game.get_board
        self.assertEqual(board.get_board_value(2, 5), 1)
        self._game.move_human(5)
        board = self._game.get_board
        self.assertEqual(board.get_board_value(3, 5), 1)
        self._game.move_human(5)
        board = self._game.get_board
        self.assertEqual(board.get_board_value(4, 5), 1)
        self._game.move_human(5)
        board = self._game.get_board
        self.assertEqual(board.get_board_value(5, 5), 1)
        self.assertFalse(self._game.move_human(5))

    def test_move_computer(self):
        self._game.move_computer(ai=True)
        self._game.move_computer(ai=False)
