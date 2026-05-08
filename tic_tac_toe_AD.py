def create_board():
    """Create and return a new Tic-Tac-Toe board."""
    return ["1", "2", "3", "4", "5", "6", "7", "8", "9"]


def display_board(board):
    """Print the current Tic-Tac-Toe board."""
    print()
    print(f"{board[0]} | {board[1]} | {board[2]}")
    print("--+---+--")
    print(f"{board[3]} | {board[4]} | {board[5]}")
    print("--+---+--")
    print(f"{board[6]} | {board[7]} | {board[8]}")
    print()


def choose_symbol():
    """Let Player 1 choose X or O and return both player symbols."""
    player_1 = input("Player 1, choose X or O: ").upper()

    if player_1 == "O":
        player_2 = "X"
    else:
        player_1 = "X"
        player_2 = "O"

    return player_1, player_2


def get_player_move(player):
    """Ask the current player to choose a position from 1 to 9."""
    move = input(f"Player {player}, choose a position from 1 to 9: ")
    return int(move)


def is_valid_move(board, move):
    """Check if the chosen position is free and inside the board."""
    if move < 1 or move > 9:
        return False

    if board[move - 1] == "X" or board[move - 1] == "O":
        return False

    return True


def make_move(board, move, player):
    """Place the player's symbol on the board."""
    board[move - 1] = player


def check_winner(board, player):
    """Check if the current player has won the game."""
    winning_lines = [
        [0, 1, 2],
        [3, 4, 5],
        [6, 7, 8],
        [0, 3, 6],
        [1, 4, 7],
        [2, 5, 8],
        [0, 4, 8],
        [2, 4, 6],
    ]

    for line in winning_lines:
        if all(board[index] == player for index in line):
            return True

    return False


def check_draw(board):
    """Check if the board is full and no more moves are possible."""
    return all(field == "X" or field == "O" for field in board)


def switch_player(current_player, player_1, player_2):
    """Switch from the current player to the other player."""
    if current_player == player_1:
        return player_2

    return player_1


def play_game():
    """Run the full Tic-Tac-Toe game."""
    print("Welcome to a new round of Tic-Tac-Toe!")
    board = create_board()
    player_1, player_2 = choose_symbol()
    current_player = player_1

    while True:
        display_board(board)

        move = get_player_move(current_player)

        if not is_valid_move(board, move):
            print("Invalid move. Please try again.")
            continue

        make_move(board, move, current_player)

        if check_winner(board, current_player):
            display_board(board)
            print(f"Player {current_player} wins!")
            break

        if check_draw(board):
            display_board(board)
            print("It's a draw!")
            break

        current_player = switch_player(current_player, player_1, player_2)

if __name__ == "__main__":
    play_game()