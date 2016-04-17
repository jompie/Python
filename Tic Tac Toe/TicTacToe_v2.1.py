# Global variables
board = [" "]*10
game_state = True
announce = ""

# This function resets the board to the original state
def reset_board():
    global board, game_state
    board = [" "]*10
    game_state = True

# this funtion will print the board to the screen
def display_board():
    print (" {0} | {1} | {2} ".format(board[7],board[8],board[9]))
    print ("---+---+---")
    print (" {0} | {1} | {2} ".format(board[4],board[5],board[6]))
    print ("---+---+---")
    print (" {0} | {1} | {2} ".format(board[1],board[2],board[3]))

# This function checks if there's a winner
def win_check(board, mark):
    # Check horizontal
    # Loops throug combinations of board positions 123, 456, 567
    i = 1
    l = []
    while i < 10:
        l.append(board[i])
        if len(l) == 3:
            if set(mark) == set(l):
                return True
            l = []
        i += 1
    #Check vertical
     #loops through combinations of board positions 147, 258, 369
    i = 1
    j = 0
    l = []
    while j < 3:
        l.append(board[i])
        if len(l)==3:
            if set(mark) == set(l):
                return True
            l = []
            i -= 8
            j += 1
        i += 3
    #chek diagonal
    # loops through combinations of board positions 159, 357
    i = 1
    j = 0
    l = []
    while j < 2:
        l.append(board[i])
        if len(l) ==3:
            if set(mark) == set(l):
                return True
            l = []
            j += 1
            i -= 8
        if j < 1:
            i += 4
        else:
            i += 2
    return False

# This function checks if every position on the board has been marked by a player
def full_board_check(board):
    if " " in board[1:]:
        return False
    else:
        return True
    
# This function asks the player where he wants to put his mark
# It also checks if it's a valid move
def ask_player(mark):
    global board
    getting_input = True
    while getting_input:
        try:
            choice = int(input('Choose where to place your: ' + mark+"\t"))
        except ValueError:
            print("Sorry, please input a number between 1-9.")
            continue

        if board[choice] == " ":
            board[choice] = mark
            getting_input = False
        else:
            print ("That space isn't empty!")

# Handles a players turn
def player_choice(mark):
    global board, game_state, announce
    announce= ""
    mark = str(mark)
    ask_player(mark) # Gets player input
    if win_check(board,mark): # check if game is won
        display_board()
        announce = mark+" wins! Congratulations"
        game_state = False

    display_board()
    if full_board_check(board): # check if board is full. A full board with no winner means a tie
        announce = "Tie!"
        game_state = False

    return game_state, announce

def play_game():
    reset_board()           
    global announce
    X="X"
    O="O"
    turn = 1
    game_on = True
    while game_on:
        display_board()        
        if turn % 2 == 1:
            game_state,announce = player_choice(X)
            print (announce)
            if game_state == False:
                game_on = False
        else:
            game_state,announce = player_choice(O)
            print (announce)
            if game_state == False:
                game_on = False
        turn += 1 
    # Ask player for a rematch
    rematch = input('Would you like to play again? y/n')
    if rematch.lower().startswith("y"):
        play_game()
    else:
        print ("Thanks for playing!")

play_game()
            
    

