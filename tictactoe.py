"""
Tic Tac Toe Player
"""
"""
Rather than a simple text interface, this version of 
minmax ia tic-tac-toe is written to take advantage 
of the pygame driver provided by project at
https://cs50.harvard.edu/ai/2020/projects/0/tictactoe/

The Harvard course also include a tight summary of 
some search algorithms including minmax at
https://cs50.harvard.edu/ai/2020/notes/0/
Use the minmax psuedo code to understand the requirements 
on the project's methods in this file.

There are other lectures by click on the included index.

Method interaction requirements clarification and a few lines from 
the Dors Coding School.

Rich Rein
"""

"""
Build
Download the Harvard code from https://cdn.cs50.net/ai/2020/x/projects/0/tictactoe.zip and unzip it.
If using an IDE such as pycharm, create the project on the folder.
Download this file and replace the tictactoe.py with this file.
"""

import math
import copy

X = "X"
O = "O"
EMPTY = None
new_board = [[EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]]
rows = len(new_board)
cols = len(new_board[0])
if rows != cols: raise NotImplementedError # Grid can be larger, but must be square for the logic to work.
maxrow = rows - 1
maxcol = cols - 1


def initial_state():
    """
    Returns starting state of the board.
    """
    return new_board


def player(board):
    """
    Returns player who has the next turn on a board.
    """
    empty = 0
    for row in range(rows):
        for col in range(cols):
            if board[row][col] == EMPTY:
                 empty += 1
    return X if empty % 2 == 1 else O  # first and odd players is X, even are O


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    moves = set()
    for row in range(rows):
        for col in range(cols):
            if board[row][col] == EMPTY:
                moves.add((row, col))
    return moves

def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    Returns a board + new move/action.
    Implements board state stacking.
    """

    # get x, y from new action
    (x, y) = action

    # copy board and add action/move
    board_and_new_move = copy.deepcopy(board)
    board_and_new_move[x][y] = player(board)

    return(board_and_new_move)


def winner(board):
    """
    Returns the winner of the game, if there is one.
    Else returns EMPTY/None.
    Note: Quick exit patterns used for pattern matching.
    """

    for p in [X, O]:

        # Search Rows
        for row in range(rows):
            for col in range(cols):
                if board[row][col] != p: break
                if col == maxcol: return p

        # Search Columns
        for col in range(cols):
            for row in range(rows):
                if board[row][col] != p: break
                if row == maxrow: return p

        # Search top left diag
        for col in range(cols):
            if board[col][col] != p: break
            if col == maxcol: return p

        # Search top right diag
        for col in range(cols):
            if board[maxcol - col][col] != p: break
            if col == maxcol: return p

    return EMPTY


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    True if winner or tie (full board).
    Thought: Could stop game if there was no hope. But requires different impl
    """
    if winner(board) != EMPTY:
        return True

    # Look for tie
    remainingCells = rows * cols;
    for row in range(rows):
        for col in range(cols):
            if board[row][col] != EMPTY: remainingCells -= 1
    if remainingCells == 0:
        return True

    # No winner or tie
    return False


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    Returns the value of the moves.
    Determines the winner is positive value or negative.
    Use winner(board) to check winner.
    X is the maximizing player
    """

    if winner(board) == X:
        return 1
    elif winner(board) == O:
        return -1
    else:
        return 0


def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    Min/Max dives down into alternating min and max layers at each available move/action for each imagined board.
    If X's turn: Return the action with the greatest value.
    If O's turn: Return the action with the least value.
    """

    if terminal(board):
        return None

    elif player(board) == X:
        sortedActionsByValue = []
        for action in actions(board):
            sortedActionsByValue.append([min_value(result(board, action)), action])
        return sorted(sortedActionsByValue, key=lambda x: x[0], reverse=True)[0][1]

    elif player(board) == O:
        sortedActionsByValue = []
        for action in actions(board):
            sortedActionsByValue.append([max_value(result(board, action)), action])
        return sorted(sortedActionsByValue, key=lambda x: x[0])[0][1]


def max_value(board):
    if terminal(board):
        return utility(board)

    value = float("-inf")

    for action in actions(board):
        value = max(value, min_value(result(board, action)))

    return value


def min_value(board):
    if terminal(board):
        return utility(board)

    value = float("inf")

    for action in actions(board):
        value = min(value, max_value(result(board, action)))

    return value






















