import pygame
import sys
import math

# define size of 1 square
square_size = 100  # pixels

# define colors in RGB color model: color(red, green, blue); r,g,b int (0, 255)
black = (0, 0, 0)
blue = (115, 215, 255)
red = (205, 92, 92)
light_red = (240, 128, 128)
green = (127, 255, 0)
yellow = (255, 255, 130)

# define radius of each circle
circle_radius = int(square_size / 2 - 5)  # diameter/2 - something so circle < square


class Gui:
    """
    Class that represents the board as a matrix with (number_of_rows+1) * number_of_columns of 100 pixels and then draws
    in each blue square a black circle in which the pieces will be put. Then using the mouse motion detection, I drew
    a piece (red for human and yellow for computer). At each user click, we get the position of the click using (x,y)
    coordinates in pixels and depending on the interval in which they are in, we calculate the column chosen by the user
    and drop the piece there.
    """
    def __init__(self, game, ai):
        self._game = game
        self._ai = ai
        self._board = self._game.get_board
        self._valid = self._game.get_validator
        self._number_of_rows = self._board.get_number_of_rows
        self._number_of_columns = self._board.get_number_of_columns
        self._player = 0
        self._computer = 1
        self._player_piece = 1
        self._computer_piece = 2
        # initialize pygame
        pygame.init()

        # define height and width of board
        self.screen_width = self._number_of_columns * square_size
        self.screen_height = (self._number_of_rows + 1) * square_size

        size = (self.screen_width, self.screen_height)

        self.screen = pygame.display.set_mode(size)
        pygame.display.set_caption("Connect Four")        # set title of game window

        # define a font for winning message
        self.myfont = pygame.font.SysFont("verdana", 70)  # pygame.font.SysFont(name, size, bold=False, italic=False) -> Font

    def draw_board(self):
        for column in range(self._number_of_columns):
            for row in range(self._number_of_rows):
                # pygame.draw.rect(surface, color, rect(left, top, width, height))
                pygame.draw.rect(self.screen, blue, (column * square_size, row * square_size + square_size, square_size, square_size))
                # pygame.draw.circle(surface, color, center, radius)
                pygame.draw.circle(self.screen, black, (int(column * square_size + square_size / 2), int(row * square_size + square_size + square_size / 2)), circle_radius)

        for column in range(self._number_of_columns):
            for row in range(self._number_of_rows):
                if int(self._board.get_board_value(row, column)) == int(self._player_piece):  # player
                    # pygame.draw.circle(surface, color, center, radius)
                    pygame.draw.circle(self.screen, red, (int(column * square_size + square_size / 2), self.screen_height - int(row * square_size + square_size / 2)), circle_radius)
                elif int(self._board.get_board_value(row, column)) == int(self._computer_piece):  # computer
                    # pygame.draw.circle(surface, color, center, radius)
                    pygame.draw.circle(self.screen, yellow, (int(column * square_size + square_size / 2), self.screen_height - int(row * square_size + square_size / 2)), circle_radius)
        pygame.display.update()  # save changes to game board

    def start(self):
        self.draw_board()
        pygame.display.update()
        turn = self._player
        game_over = False
        is_running = True
        while not game_over and is_running:
            for event in pygame.event.get():   # get each event
                if event.type == pygame.QUIT:  # quit
                    is_running = False

                if event.type == pygame.MOUSEMOTION:  # display the piece at the top row in order to see where user clicks
                    if turn == self._player:
                        pygame.draw.rect(self.screen, black, (0, 0, self.screen_width, square_size))
                        pos_x = event.pos[0]
                        pygame.draw.circle(self.screen, light_red, (pos_x, int(square_size / 2)), circle_radius)

                pygame.display.update()

                # user chose a column by clicking
                if event.type == pygame.MOUSEBUTTONDOWN:  # pygame.MOUSEBUTTONDOWN -> (pos, button, touch)
                    if turn == self._player:              # human's turn
                        pos_x = event.pos[0]
                        move = int(math.floor(pos_x / square_size))   # calculate column based on pixels value of click
                        self._game.move_human(move)
                        if self._board.is_winning_move(1):                        # draw text on a new Surface
                            # render(text, antialias(pixels at edges appear smoother), color, background=None)
                            label = self.myfont.render("You win!", True, red)
                            self.screen.blit(label, (205, 20))   # blit = "assigning" pixels; only update screen at position (x,y)
                            game_over = True
                        self.draw_board()
                        turn += 1
                        turn = turn % 2

            if turn == self._computer and not game_over:  # computer's turn
                if self._ai is False:
                    pygame.time.wait(500)
                self._game.move_computer(self._ai)
                if self._board.is_winning_move(2):
                    # render(text, antialias(pixels at edges appear smoother), color, background=None)
                    label = self.myfont.render("Computer wins!", True, yellow)
                    self.screen.blit(label, (70, 20))  # blit = "assigning" pixels; only update screen at position (x,y)
                    game_over = True
                self.draw_board()
                turn += 1
                turn = turn % 2

            if self._board.is_board_full is True:
                # render(text, antialias(pixels at edges appear smoother), color, background=None)
                label = self.myfont.render("It's draw!", True, green)
                self.screen.blit(label, (205, 20))  # blit = "assigning" pixels; only update screen at position (x,y)
                game_over = True

            if game_over:  # keep game window open for another 5 secs after end of game
                pygame.time.wait(5000)  # 5000ms = 5s

        # qui gui
        pygame.quit()
        sys.exit(0)
