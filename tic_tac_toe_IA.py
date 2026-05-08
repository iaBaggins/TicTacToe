# In this script you can write your code.
# Start by writing all the functions.
# In the last part after if __name__ == "__main__": you can call the functions to play your game.
# If you run `python tic_tac_toe.py` in the command line the game will start. Try it out! ;)


# ome Tests:
# Choose X/O:
# - enter nothing
# - enter A
# - enter 1
# - enter char1234
# - enter code
# Play piece:
# - Enter nothing
# - Enter out of bounds C4
# - Enter wrong order 4C
# - Enter string "horse" 
# - Enter code
# Win/Lose/Draw:
# - Check win condition with both players
# - Check Draw condition


# defining winner sets
winner_sets = list[
    ("1A", "1B", "1C"),
    ("2A", "2B", "2C"),
    ("3A", "3B", "3C"),

    ("1A", "2A", "3A"),
    ("1B", "2B", "3B"),
    ("1C", "2C", "3C"),

    ("1A", "2B", "3C"),
    ("1C", "2B", "3A"),
    ]


def board(grid):

    print("      A     B     C")
    print("   ___________________")
    print("   |     |     |     |")
    print(f"1  |  { grid['1A'] }  |  { grid['1B'] }  |  { grid['1C'] }  |")
    print("   |_____|_____|_____|")
    print("   |     |     |     |")
    print(f"2  |  { grid['2A'] }  |  { grid['2B'] }  |  { grid['2C'] }  |")
    print("   |_____|_____|_____|")
    print("   |     |     |     |")
    print(f"3  |  { grid['3A'] }  |  { grid['3B'] }  |  { grid['3C'] }  |")
    print("   |_____|_____|_____|")


grid = {
    "1A" : " ",  "1B" : " ",  "1C" : " ",
    "2A" : " ",  "2B" : " ",  "2C" : " ",
    "3A" : " ",  "3B" : " ",  "3C" : " "
}

# Initial player is player X
# Will change into O when grid is successfully updated

player_x_o = "X"


# Function for changing player
def change_player(x_o):
    global player_x_o
    if x_o == "X":
        player_x_o = "O"
    elif x_o == "O":
         player_x_o = "X"
    else:
        return False


# validates input and
def validate_input(move):

    for slot in grid:
        
        # validate input on slot key
        if move != slot :
            return "Please choose a valid slot"
        
        # validate input on slot availability
        elif grid[move] != ' ' :
            return "Please choose an empty slot"
        else:
            return True 
        
    return False
        

# update grid 
def update_grid(move):
    # checks for input validity 
    if validate_input(move):
        # updates grid if passes
        grid[move] = player_x_o

        # switches player
        if change_player(player_x_o):
            return True
        else:
            print("Could not change player")
            
    else :
        # returns message from validate_input function
        # was it invalid slot key or the slot was not empty
        return "Could not validate"
    
    return(board(grid))
    


def next_move():
    print("Input format example: 3B, 1A, 2C....")
    move = input("Choose your move from the grid: ")
    return update_grid(move)


def check_winner(grid, winner_sets):
    for a, b, c in winner_sets:
        if grid[a] == grid[b] == grid[c] and grid[a] != " ":
            return grid[a]  # "X" or "O"
    return None      

# Tic-tac-toe game
if __name__ == "__main__":


    while True :

        # display board
        print(board(grid))

        # check for win/draw
        check_winner(grid, winner_sets)

        # ask for next move
        print(next_move())

