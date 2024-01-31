import connectfour

def print_board(game_state: connectfour.GameState) -> None:
    '''function that a GameState and prints the board associated with it'''
    
    # board is sideways (x and y axis are flipped)
    board = game_state.board 
    converted_board = [[None for x in range(len(board))] for y in range(len(board[0]))]

    # print player header and column numbers
    print_player_banner(game_state)
    _print_col_banner(connectfour.columns(game_state))

    # flips the x and y axis so they are correctly oriented
    for y in range(len(board[0])):
        for x in range(len(board)):
            converted_board[y][x] = board[x][y]

    # iterates through the list and converts (0,1,2) into (.,red,yellow)
    for x in converted_board:
        line = ''
        for y in x:
            if y == 0:
                line += ' . '
            elif y == 1:
                line += ' R '
            elif y == 2:
                line += ' Y '
        print(line[1:])

def init_rows() -> int:
    '''function that takes no parameters and prompts the user for a numbers of rows
    and returns a user entered value between 4 and 40'''
    while True:
        try:
            rows = int(input('How many rows would you like? '))
            
            if 4 <= rows <= 20:
                return rows
            else:
                print('Please enter a number of rows between 4 and 20')
        except ValueError:
            # catch error in case the user enters something that can't be converted to int
            print('Please enter a number of rows betweeen 4 and 20')

def init_cols() -> int:
    '''function that takes no parameters and prompts the user for a numbers of columns
    and returns a user entered value between 4 and 40'''
    while True:
        try:
            cols = int(input('How many columns would you like? '))
            
            if 4 <= cols <= 20:
                return cols
            else:
                print('Please enter a number of cols between 4 and 20')
        except ValueError:
            # catch error in case the user enters something that can't be converted to int
            print('Please enter a number of cols betweeen 4 and 20')

def get_move(game_state: connectfour.GameState) -> str:
    '''function that takes a game_state as a parameter which prompts the user for a move and
    only returns a valid move (either pop or drop)'''
    while True:
        move = input('Would you like to POP or DROP: ').upper()
        # cast user input to all caps
        if move == 'DROP' or move == 'POP':
            return move
        else:
            clear_board()
            print('Please enter a valid move')
            print_board(game_state)

def get_move_col(game_state: connectfour.GameState) -> int:
    '''function that takes a GameState as a parameter which prompts the user for a column 
    for a move to be done in and only returns if the number entered is between 0 and the amount of columns
    in the current game board'''
    while True:
        move = input('Enter a column number: ')

        try:
            move = int(move)
            
            # makes sure the value entered is a valid number between 0 and the amount of columns
            
            if 0 < move <= connectfour.columns(game_state):
                return move
            else:
                clear_board()
                print('Please enter a valid collumn number')
                print_board(game_state)

        except ValueError:
            # if letter enetered, clear board and print error message
            clear_board()
            print('Please enter a valid collumn number')
            print_board(game_state)        

def print_player_banner(game_state: connectfour.GameState) -> None:
    '''function that takes a GameState as a parameter and prints who's turn it is'''
    if game_state.turn == 1:
        print('RED TURN')
    else:
        print('YELLOW TURN')

def clear_board() -> None:
    '''function that clears the previous move's board out of view'''
    clear = '\n' * 40
    print(clear)

def _print_col_banner(cols: int):
    '''function that prints the column numbers above each column'''
    banner = ''
    for x in range(1, cols+1):
        # if there are 2 numbers in the colum header then there should only be one 
        # one space between numbers
        if x < 10:
            banner += f' {x} '
        else:
            banner += f' {x}'
    
    print(banner[1:])

def full_column(game_state: connectfour.GameState, col: int) -> bool:
    '''function that takes a GameState and an int as a parameter and checks if that specific 
    column is full'''
    board = game_state.board
    if 0 not in board[col-1]:
        return True
    return False

def make_hashable(game_state: connectfour.GameState):
    temp_board = game_state.board[::]
    for i in range(6):
        temp_board[i] = tuple(temp_board[i])

    return tuple(temp_board)

