from random import shuffle
import random
import math


class Game:
    def __init__(self, board, board_valid):
        self._board = board
        self._board_validator = board_valid
        self._player_piece = 1
        self._computer_piece = 2

    @property
    def get_board(self):
        return self._board

    @property
    def get_validator(self):
        return self._board_validator

    def move_human(self, move):
        """
        Method that handles human moves
        :param move:
        :return:
        """
        if self._board.is_valid_column(move):
            row = self._board.get_next_available_row(move)
            self._board.drop_piece_on_board(row, move, self._player_piece)
        else:
            return False   # chosen column is not a valid location = column is full

    def move_computer_random(self):
        """
        Method that handles computer moves: random
        :return:
        """
        choices = []
        for column in range(int(self._board.get_number_of_columns)):
            if self._board.is_valid_column(column):
                row = self._board.get_next_available_row(column)
                choices.append((row, column))
        shuffle(choices)
        move = choices[0]
        self._board.drop_piece_on_board(move[0], move[1], self._computer_piece)
        print("Computer moves on column " + str(move[1]) + " and row " + str(move[0]) + "!\n")

    def move_computer_no_ai(self):
        """
        Method that handles computer moves: try to win
        :return:
        """
        # First try to win
        for column in range(int(self._board.get_number_of_columns)):  # try to find a winning move
            if self._board.is_valid_column(column):
                row = self._board.get_next_available_row(column)
                # simulate move
                board = self._board.get_board_copy()
                board.drop_piece_on_board(row, column, self._computer_piece)  # board[row][column] = 2
                if board.is_winning_move(self._computer_piece) is True:
                    self._board.drop_piece_on_board(row, column, self._computer_piece)
                    print("Computer moves on column " + str(column) + " and row " + str(row) + "!\n")
                    return

        # If winning is not possible, prevent human from winning
        for column in range(int(self._board.get_number_of_columns)):
            if self._board.is_valid_column(column):
                row = self._board.get_next_available_row(column)
                # simulate move
                board = self._board.get_board_copy()
                board.drop_piece_on_board(row, column, self._player_piece)  # try each move for human player
                if board.is_winning_move(self._player_piece) is True:
                    self._board.drop_piece_on_board(row, column, self._computer_piece)
                    print("Computer moves on column " + str(column) + " and row " + str(row) + "!\n")
                    return

        # If previous strategies did not work, move randomly
        self.move_computer_random()

    """
    Minimax Algorithm - look down at every branch possible and pick the one with the best score
    """
    def is_terminal_node(self):
        """
        terminal_node = human winning or computer winning or board is full
        :return:
        """
        return self._board.is_winning_move(self._player_piece) or self._board.is_winning_move(self._computer_piece) \
               or len(self._board.get_available_locations()) == 0

    def minimax_alpha_beta_pruning(self, depth, alpha, beta, maximizingPlayer):     # fail soft version
        """
        Alpha–beta pruning applied to a standard minimax tree -> decreases the number of nodes that are evaluated by the minimax algorithm
                                                              -> search time can be limited to the 'more promising' subtree
        node = board
        maximizingPlayer = player who tries to get the highest score -> computer
        minimizingPlayer = human
        leaf node = terminal nodes and nodes at the maximum search depth
        terminal_node = human winning / computer winning / board is full = draw

        (* Initial call *)
        minimax(origin, depth, −∞, +∞, TRUE)
        :param alpha: For a max node: the current best value is at least alpha
        :param beta: For a min node: the current best value is at most beta
        :param depth: how far we're searching
        :param maximizingPlayer: True for AI, False for human
        :return: tuple of (best_column, best_score)
        """                                                     # MINIMAX ALGORITHM PSEUDOCODE
        valid_locations = self._board.get_available_locations()
        is_terminal = self.is_terminal_node()                   # function alphabeta(node, depth, α, β, maximizingPlayer) is

        # static evaluation
        if depth == 0 or is_terminal:                             # if depth = 0 or node is a terminal node then
            if is_terminal:                                         # return the heuristic value of node
                if self._board.is_winning_move(self._computer_piece):  # return a VERY high score to FORCE this move
                    return None, 100000000000
                elif self._board.is_winning_move(self._player_piece):  # return a VERY low score to AVOID this happening
                    return None, -100000000000
                else:
                    return None, 0    # game over -> board is full -> draw
            else:               # depth == 0
                return None, self._board.get_score(self._computer_piece)

        if maximizingPlayer:  # computer                          # if maximizingPlayer then
            best_score = -math.inf                                # value := −∞
            best_column = random.choice(valid_locations)
            for column in valid_locations:                           # for each child of node do
                row = self._board.get_next_available_row(column)            # value := max(value, alphabeta(child, depth − 1, α, β, FALSE))
                board = self._board.get_board_copy()
                board.drop_piece_on_board(row, column, self._computer_piece)    # simulate move
                game = Game(board, self._board_validator)
                new_score = game.minimax_alpha_beta_pruning(depth - 1, alpha, beta, False)[1]
                if new_score > best_score:    # maximum
                    best_score = new_score
                    best_column = column
                alpha = max(alpha, best_score)                         # α := max(α, value)
                if alpha >= beta:                                      # if α ≥ β then
                    break                                                 # break (* β cutoff *)
            return best_column, best_score                             # return value

        else:   # minimizingPlayer = human                             # else (* minimizing player *)
            best_score = math.inf                                 # value := +∞
            best_column = random.choice(valid_locations)
            for column in valid_locations:                           # for each child of node do
                row = self._board.get_next_available_row(column)            # value := min(value, alphabeta(child, depth − 1, α, β, TRUE))
                board = self._board.get_board_copy()
                board.drop_piece_on_board(row, column, self._player_piece)      # simulate move
                game = Game(board, self._board_validator)
                new_score = game.minimax_alpha_beta_pruning(depth - 1, alpha, beta, True)[1]
                if new_score < best_score:     # minimum
                    best_score = new_score
                    best_column = column
                beta = min(beta, best_score)                          # β := min(β, value)
                if alpha >= beta:                                     # if β ≤ α then
                    break                                                # break (* α cutoff *)
            return best_column, best_score                            # return value

    def pick_best_move(self, piece):
        """
        For each possible column run get_score() and pick highest score returned
        :param piece:
        :return:
        """
        best_score = 0
        valid_locations = self._board.get_available_locations()
        best_move = random.choice(valid_locations)
        for column in valid_locations:
            row = self._board.get_next_available_row(column)
            # simulate move
            board = self._board.get_board_copy()
            board.drop_piece_on_board(row, column, piece)
            score = board.get_score(piece)
            if int(score) >= int(best_score):
                best_score = score
                best_move = column
        return best_move

    def move_computer_ai_simple(self):
        """
        Method that handles computer moves: chooses next move by computing the score of all possible next moves
        and picking the highest one
        :return:
        """
        move = int(self.pick_best_move(self._computer_piece))
        row = int(self._board.get_next_available_row(move))
        self._board.drop_piece_on_board(row, move, self._computer_piece)
        print("Computer moves on column " + str(move) + " and row " + str(row) + "!\n")

    def move_computer_ai_better(self):
        """
        Method that handles computer moves: creates a strategy using minimax algorithm
        :return:
        """
        alpha = -math.inf
        beta = math.inf
        depth = 5
        move, minimax_score = self.minimax_alpha_beta_pruning(depth, alpha, beta, True)
        row = int(self._board.get_next_available_row(move))
        self._board.drop_piece_on_board(row, move, self._computer_piece)
        print("Computer moves on column " + str(move) + " and row " + str(row) + "!\n")

    def move_computer(self, ai):
        """
        Method that handles computer moves - either with or without AI
        :return:
        """
        if ai is True:
            # self.move_computer_ai_simple()
            self.move_computer_ai_better()
        else:
            self.move_computer_no_ai()
