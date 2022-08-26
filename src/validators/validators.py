from exceptions.exceptions import InputError


class ValidateBoard:
    """
    Class that validates a new move from human
    """
    @staticmethod
    def validate_move(move):
        try:
            move = int(move)
        except ValueError:
            raise InputError("Invalid move! Must be an integer between 0 and 6!\n")
        if int(move) < 0 or int(move) > 6:
            raise InputError("Invalid move! Must be an integer between 0 and 6!\n")
