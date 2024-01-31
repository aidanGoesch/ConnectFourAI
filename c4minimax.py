import time
import math
import random
from functools import lru_cache

import connectfour
import c4functions as c4

# 0 1 2 3 4 5 6
MOVE_ORDER = [3, 2, 4, 1, 5, 0, 6]

def call_counter(func):
    count = 0

    def wrapper(*args, **kwargs):
        nonlocal count
        count += 1
        print(count)
        return func(*args, **kwargs)

    return wrapper


def get_move_col(game_state: connectfour.GameState) -> int:
    while True:
        print("Where would you like to drop your piece?")
        move = input('Enter the column number: ')

        try:
            move = int(move)

            # makes sure the value entered is a valid number between 0 and the amount of columns

            if 0 < move <= connectfour.columns(game_state):
                return move
            else:
                c4.clear_board()
                print('Please enter a valid column number')
                c4.print_board(game_state)
        except ValueError:
            # if letter enetered, clear board and print error message
            c4.clear_board()
            print('Please enter a valid column number')
            c4.print_board(game_state)


def run() -> None:
    '''function that runs connect four in the shell'''
    print('Welcome to Connect 4, Shell version.')

    rows = 6
    cols = 7

    # create new game
    game_state = connectfour.new_game(cols, rows)

    while True:
        # check for a winner before every turn
        if connectfour.winner(game_state) == 0:
            # print board from last turn
            c4.clear_board()
            c4.print_board(game_state)

            if game_state.turn == 1:
                move_column = get_move_col(game_state)
                while True:
                    # try to make entered move
                    try:
                        game_state = connectfour.drop(game_state, move_column - 1)
                        break

                    except connectfour.InvalidMoveError:
                        if c4.full_column(game_state, move_column):
                            print('This column is full. Please pick another column')
                        else:
                            # if player tries to pop a piece that isn't theirs
                            print('You can only pop a column if the bottom piece is yours')
            else:
                ai_move = mini_max(game_state, alpha = -math.inf, beta = math.inf, maximizing_player = True, depth = 9)[0]
                print('ai_move ', ai_move + 1)
                game_state = connectfour.drop(game_state, ai_move)


        else:
            # break out of the game loop if there is a winner
            break

    # check for who won and print the corresponding win message
    if connectfour.winner(game_state) == 1:
        c4.clear_board()
        print('RED WINS!')
        c4.print_board(game_state)

    elif connectfour.winner(game_state) == 2:
        c4.clear_board()
        print('YELLOW WINS')
        c4.print_board(game_state)


# def mini_max(game_state: connectfour.GameState, score: int = 0):
#     """function responsible for scoring each state of the board"""
#     for i in range(6):
#         print(i)
#         try:
#             score += mini_max(connectfour.drop(game_state, i))
#             # print(i, score)
#
#         except connectfour.GameOverError:
#             if connectfour.winner(game_state) == 1:
#                 return -100
#             elif connectfour.winner(game_state) == 2:
#                 return 100
#             elif connectfour.winner(game_state) == 0:
#                 return 0
#         except connectfour.InvalidMoveError:
#             pass
#     return score


@lru_cache(maxsize=None)
def mini_max(game_state: connectfour.GameState, alpha:int, beta:int, maximizing_player: bool = True, depth:int = 0):
    """function responsible for scoring each state of the board"""
    winner = connectfour.winner(game_state)
    is_full = connectfour.is_full(game_state)
    if winner != 0 or depth == 0 or is_full:
        if winner == 1:
            return (None, -1000000)
        elif winner == 2:
            return (None, 1000000)
        elif is_full:
            return (None, 0)
        elif depth == 0:
            # c4.print_board(game_state)
            # print('\n\n')
            return (None, connectfour.score_board(game_state))


    if maximizing_player:
        best_score = -math.inf
        best_col = 3
        for i in MOVE_ORDER:
            if connectfour.dropable(game_state, i):
                score = mini_max(connectfour.drop(game_state, i), alpha, beta, maximizing_player=False, depth=depth - 1)[1]
                if score > best_score:
                    best_score = score
                    best_col = i
                # best_score = max(best_score, score)
                alpha = max(alpha, best_score)
                if alpha >= beta:
                    break
        return (best_col, best_score)

    else:
        best_score = math.inf
        best_col = 3
        for i in MOVE_ORDER:
            if connectfour.dropable(game_state, i):
                score = mini_max(connectfour.drop(game_state, i), alpha, beta, maximizing_player=True, depth=depth - 1)[1]
                if score < best_score:
                    best_score = score
                    best_col = i
                # best_score = min(best_score, score)
                beta = min(beta, best_score)
                if alpha >= beta:
                    break
        return (best_col, best_score)





if __name__ == '__main__':
    run()
    # I = 0
    # g = connectfour.GameState(turn=1)
    # g.board = [[0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 1], [0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0]]
    # c4.print_board(g)
    # print(connectfour.score_board(g))
    # print("best move", minimax(g, alpha = math.inf, beta = -math.inf, maximizing_player=False))

