from exceptions.exceptions import InputError


class Ui:
    def __init__(self, game, ai):
        self._game = game
        self._ai = ai
        self._board = self._game.get_board
        self._valid = self._game.get_validator
        self._player = 0
        self._computer = 1
        self._player_piece = 1
        self._computer_piece = 2

    def read_move(self):
        while True:
            try:
                column = input("Input column on which you wish to make a move (0-6): ")
                self._valid.validate_move(column)
                return int(column)
            except InputError as ie:
                print(str(ie))

    def start(self):
        print("Welcome to Connect Four!")
        print("Let's play! Human starts!")
        turn = self._player
        game_over = False
        while not game_over:
            print(self._board.__str__())
            if turn == self._player:
                move = self.read_move()
                make_move = self._game.move_human(move)
                if make_move is not False:  # if the human player made a move, switch turns
                    turn += 1
                    turn = turn % 2
                if self._board.is_winning_move(self._player_piece):
                    print(self._board.__str__())
                    print("Congrats! You win!")
                    game_over = True
            else:
                self._game.move_computer(self._ai)
                if self._board.is_winning_move(self._computer_piece):
                    print(self._board.__str__())
                    print("Computer wins!")
                    game_over = True
                turn += 1                  # switch turns
                turn = turn % 2
            if self._board.is_board_full is True:
                print(self._board.__str__())
                print("It's draw!")
                game_over = True
