# :video_game: Connect Four Game

-	human vs computer implementation of the two-player connection board game using python 3 & pygame, object oriented programming and layered architecture 
-	graphical user interface & console-based user interface
-	customizable board size, initially set to standard: seven-column, six-row
-	all modules with the exception of the UI are covered with specifications and PyUnit test cases
-	the program protects itself against the user’s invalid input, displaying error messages
-	the computer player has different difficulty levels: 
    1.	 **no AI**: computer player tries to find a winning move by checking empty spaces. If winning is not possible, it prevents the human player from winning. If previous         strategies did not work, it moves randomly.
    2.	 **simple AI** (without minimax): computer chooses next move by computing the score of all possible next moves and picking the highest one
    3.   **AI**: minimax algorithm using alpha–beta pruning

The user should input in **settings.properties** file board size, user interface (ui/gui) and AI (yes/no) for the computer player. 

## How to Play:
The two players take turns dropping colored tokens (red-human, yellow-computer) into a seven-column, six-row vertically suspended grid. The pieces fall straight down, occupying the lowest available space within the selected column. The objective of the game is to be the first to form a horizontal, vertical, or diagonal line of four of one's own tokens.
