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
                ai_move = minimax(game_state, depth = 9)[0]
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


def hash_state(game_state : connectfour.GameState, maximizing : bool):
    tmp = [game_state.__hash__()]
    tmp += [int(maximizing)]
    # print(tmp)
    return tuple(tmp)


@lru_cache(maxsize=None)
def minimax(game_state : connectfour.GameState, depth = 6):
    transposition_table = dict()
    def alphabeta(alpha:int, beta:int, maximizing_player: bool = True, depth:int = 0):
        """function responsible for scoring each state of the board"""

        hash_value = hash_state(game_state, maximizing_player)
        if hash_value in transposition_table:
            # c, s, a, b,
            #
            #
            # if connectfour.dropable(game_state, transposition_table[hash_value][0]):
                return transposition_table[hash_value]


        if depth == 0:
            transposition_table[hash_value] = (None, connectfour.score_board(game_state))
            return transposition_table[hash_value]


        if maximizing_player:   # player 1
            best_score = -math.inf
            best_col = 3
            for i in MOVE_ORDER:
                if connectfour.dropable(game_state, i):
                    # print(game_state.board, 1, "turn =", game_state.turn)
                    game_state.drop(i)

                    # print(game_state.board, 2, "turn =", game_state.turn)
                    if connectfour.is_winning_move(game_state, i, connectfour._opposite_turn(game_state.turn)):
                        # print(game_state.board)

                        game_state.undo(i)
                        score = math.inf
                    elif game_state.is_full():
                        game_state.undo(i)
                        return (3, 0)
                    else:
                        score = alphabeta(alpha, beta, maximizing_player=False, depth=depth - 1)[1]
                        game_state.undo(i)

                    if score > best_score:
                        best_score = score
                        best_col = i
                    alpha = max(alpha, best_score)

                    # if depth == 6:
                    #     print(i, score, best_col, alpha, beta)

                    if alpha >= beta:
                        break
            transposition_table[hash_value] = (best_col, best_score, alpha, beta)
            return transposition_table[hash_value]

        else:    # player 2
            best_score = 10000000
            best_col = 3
            for i in MOVE_ORDER:
                if connectfour.dropable(game_state, i):
                    game_state.drop(i)
                    if connectfour.is_winning_move(game_state, i, connectfour._opposite_turn(game_state.turn)):
                        score = -math.inf
                        game_state.undo(i)
                    elif game_state.is_full():
                        game_state.undo(i)
                        return (3, 0)
                    else:
                        score = alphabeta(alpha, beta, maximizing_player=True, depth=depth - 1)[1]
                        game_state.undo(i)

                    if score < best_score:
                        best_score = score
                        best_col = i
                    beta = min(beta, best_score)
                    if alpha >= beta:
                        break
            transposition_table[hash_value] = (best_col, best_score, alpha, beta)
            return transposition_table[hash_value]


    start_time = time.time()

    optimal_move = (0, 0)
    d = 4
    while d <= 16 and time.time() - start_time < 1.0:
        optimal_move = alphabeta(alpha = -math.inf, beta = math.inf, maximizing_player = True, depth = d)

        print(d, time.time(), start_time, time.time() - start_time, optimal_move, game_state.board)
        print(transposition_table)

        d += 2

    return optimal_move
    # return alphabeta(alpha = -math.inf, beta = math.inf, maximizing_player = True, depth = depth)





if __name__ == '__main__':
    run()
    # I = 0
    # g = connectfour.GameState(turn=1)
    # g.board = [[0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 1], [0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0]]
    # c4.print_board(g)
    # print(connectfour.score_board(g))
    # print("best move", minimax(g, alpha = math.inf, beta = -math.inf, maximizing_player=False))

