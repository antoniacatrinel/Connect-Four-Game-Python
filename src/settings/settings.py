from configparser import ConfigParser
from board.board import Board
from exceptions.exceptions import SettingsError
from game.game import Game
from gui.gui import Gui
from ui.ui import Ui
from validators.validators import ValidateBoard
import os


class Settings:
    """
    Class that reads and parses file 'settings.properties' and configures settings of game
    """
    def __init__(self):
        thisfolder = os.path.dirname(os.path.abspath(__file__))
        initfile = os.path.join(thisfolder, 'settings.properties')
        parser = ConfigParser()
        parser.read(initfile)
        no_of_rows = parser.get("settings", "board_height")
        no_of_columns = parser.get("settings", "board_width")
        try:
            no_of_rows = int(no_of_rows)
            no_of_columns = int(no_of_columns)
        except ValueError:
            raise SettingsError("Invalid board dimensions! They must be positive integers!")
        ui_style = parser.get("settings", "UI")
        ui_style.lower()

        ai = parser.get("settings", "AI")
        ai.lower()
        """
        Initialize board
        """
        board = Board(int(no_of_rows), int(no_of_columns))
        board_valid = ValidateBoard()
        """
        Initialize game
        """
        game = Game(board, board_valid)
        if ai == "yes":
            if ui_style == "ui":
                self._ui = Ui(game, ai=True)
            elif ui_style == "gui":
                self._ui = Gui(game, ai=True)
            else:
                raise SettingsError("Invalid UI settings!")
        elif ai == "no":
            if ui_style == "ui":
                self._ui = Ui(game, ai=False)
            elif ui_style == "gui":
                self._ui = Gui(game, ai=False)
            else:
                raise SettingsError("Invalid UI settings!")
        else:
            raise SettingsError("Invalid AI settings!")

    @property
    def ui(self):
        return self._ui
