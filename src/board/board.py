import copy
from texttable import Texttable


class Board:
    def __init__(self, rows, columns):
        self._number_of_rows = rows
        self._number_of_columns = columns
        self._board = []
        self._player_piece = 1
        self._computer_piece = 2
        self.create_new_board()

    @property
    def get_number_of_rows(self):
        return self._number_of_rows

    @property
    def get_number_of_columns(self):
        return self._number_of_columns

    def get_board_value(self, row, column):
        return int(self._board[row][column])

    def create_new_board(self):
        """
        Function that creates a new board as a matrix with all elements 0
        :return: new board
        """
        for row in range(self._number_of_rows):
            row = []
            for column in range(self._number_of_columns):
                row.append(0)
            self._board.append(row)

    def drop_piece_on_board(self, row, column, piece):
        self._board[row][column] = int(piece)

    def is_valid_column(self, column):
        """
        Check if column is available for move: it isn't filled to the top
        :param column:
        :return:
        """
        return self._board[self._number_of_rows-1][column] == 0

    def get_next_available_row(self, column):
        """
        Check on which row of the selected column the piece will fall on
        :param column:
        :return:
        """
        for row in range(self._number_of_rows):
            if self._board[row][column] == 0:
                return row

    def get_board_copy(self):
        """
        Method that returns a copy of the current board
        :return: a Board() type object representing the current state of the board
        """
        board = Board(self._number_of_rows, self._number_of_columns)
        board._board = copy.deepcopy(self._board)
        return board

    def to_str(self):  # ended up not using this
        """
        Method that converts the board to string for printing
        :return:
        """
        current_board = ""
        for row in range(self._number_of_rows-1, -1, -1):
            for column in range(self._number_of_columns):
                if int(self.get_board_value(row, column)) == 0:
                    current_board += "-"
                else:
                    current_board += str(self.get_board_value(row, column))
            current_board += "\n"
        return current_board

    def __str__(self):
        """
        Method that converts the board to a text table format for printing
        :return:
        """
        table = Texttable()
        header = [' ']
        for index in range(self.get_number_of_columns):
            header.append(str(index))
        table.header(header)
        for row_index in range(self._number_of_rows-1, -1, -1):
            row = [row_index]
            for column_index in range(self._number_of_columns):
                row.append(self.get_board_value(row_index, column_index))
            table.add_row(row)
        return table.draw()

    def is_winning_move(self, piece):
        # Check horizontal locations for win
        for column in range(self._number_of_columns-3):  # winning move cannot begin on last 3 columns
            for row in range(self._number_of_rows):
                if int(self._board[row][column]) == int(piece) and int(self._board[row][column+1]) == int(piece) \
                   and int(self._board[row][column+2]) == int(piece) and int(self._board[row][column+3]) == int(piece):
                    return True

        # Check vertical locations for win
        for column in range(self._number_of_columns):
            for row in range(self._number_of_rows-3):  # winning move cannot begin on last 3 rows
                if int(self._board[row][column]) == int(piece) and int(self._board[row+1][column]) == int(piece) \
                   and int(self._board[row+2][column]) == int(piece) and int(self._board[row+3][column]) == int(piece):
                    return True

        # Check diagonals upwards for win (positively sloped diagonals)
        for column in range(self._number_of_columns-3):  # winning move cannot begin on last 3 columns
            for row in range(self._number_of_rows-3):  # winning move cannot begin on last 3 rows
                if int(self._board[row][column]) == int(piece) and int(self._board[row+1][column+1]) == int(piece) \
                   and int(self._board[row+2][column+2]) == int(piece) and int(self._board[row+3][column+3]) == int(piece):
                    return True

        # Check diagonals downwards for win (negatively sloped diagonals)
        for column in range(self._number_of_columns-3):  # winning move cannot begin on last 3 columns
            for row in range(3, self._number_of_rows):  # winning move cannot begin on first 3 rows
                if int(self._board[row][column]) == int(piece) and int(self._board[row-1][column+1]) == int(piece) \
                   and int(self._board[row-2][column+2]) == int(piece) and int(self._board[row-3][column+3]) == int(piece):
                    return True

    def is_board_full(self):
        """
        Method that checks is board is full = no more available moves -> draw
        :return:
        """
        for row in range(self._number_of_rows):
            for column in range(self._number_of_columns):
                if int(self.get_board_value(row, column)) == 0:
                    return False  # found first empty position, so board is not full
        return True

    """
    Functions for Minimax Algorithm 
    """
    def get_available_locations(self):
        """
        Method that creates and returns a list of all possible locations of a move = all columns that are not completely
        filled
        :return:
        """
        valid_locations = []
        for column in range(self._number_of_columns):
            if self.is_valid_column(column):
                valid_locations.append(column)
        return valid_locations

    def compute_score(self, group, piece):
        """
        Evaluate each group of 4 pieces and compute score
        """
        if int(piece) == int(self._player_piece):   # figure out which is the opponent
            opponent_piece = int(self._computer_piece)
        else:
            opponent_piece = int(self._player_piece)

        score = 0
        if int(group.count(piece)) == 4:        # if we have a group of 4 in a row, that's great so we increase score by 100
            score += 100
        elif int(group.count(piece)) == 3 and int(group.count(0)) == 1:  # if we have a group of 3 in a row, increase score by 5
            score += 5
        elif int(group.count(piece)) == 2 and int(group.count(0)) == 2:  # if we have a group of 2 in a row, increase score by 2
            score += 2

        # check 3 in a row for opponent because it's more important to make a winning move than to block opponent
        if int(group.count(opponent_piece)) == 3 and int(group.count(0)) == 1:
            score -= 4
        return score

    def get_score(self, piece):
        """
        Look at current board and count how many 4, 3 and 2 s in a row we have + central column
        In each group of 4 consecutive squares count how many empty and filled in squares there are
        :param piece: piece that we are searching for (1 for player, 2 for computer)
        :return:
        """
        score = 0

        # Score Center column because you have way more move possibilities if you're in the centre
        center_list = []
        for row in range(self._number_of_rows):
            middle_column = self._number_of_columns//2
            center_list.append(self.get_board_value(row, middle_column))
        center_count = center_list.count(piece)
        score += center_count * 3

        # Score Horizontally
        for row in range(self._number_of_rows):
            row_list = []
            for column in range(self._number_of_columns):
                row_list.append(self.get_board_value(row, column))

            # look at each group of 4 squares
            for column in range(self.get_number_of_columns-3):
                group = row_list[column:column+4]
                score += self.compute_score(group, piece)

        # Score Vertically
        for column in range(self._number_of_columns):
            column_list = []
            for row in range(self._number_of_rows):
                column_list.append(self.get_board_value(row, column))

            # look at each group of 4 squares
            for row in range(self._number_of_rows - 3):
                group = column_list[row:row + 4]
                score += self.compute_score(group, piece)

        # Score Diagonally positively sloped
        for row in range(self._number_of_rows - 3):
            for column in range(self._number_of_columns - 3):
                # look at each group of 4 squares
                group = []
                for i in range(4):
                    group.append(self.get_board_value(row + i, column + i))
                score += self.compute_score(group, piece)

        # Score Diagonally negatively sloped
        for row in range(self._number_of_rows - 3):
            for column in range(self._number_of_columns - 3):
                # look at each group of 4 squares
                group = []
                for i in range(4):
                    group.append(self.get_board_value(row + 3 - i, column + i))
                if int(group.count(piece)) == 4:  # if we find 4 pieces in a row -> score increases by 100
                    score += 100
                elif int(group.count(piece)) == 3 and int(group.count(0)) == 1:  # 0 means empty
                    score += 10

        return score
