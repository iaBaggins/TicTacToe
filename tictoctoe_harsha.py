from IPython.display import clear_output
import time

# Data Structures
grid_template = {
    "1A" : " ",  "1B" : " ",  "1C" : " ",
    "2A" : " ",  "2B" : " ",  "2C" : " ",
    "3A" : " ",  "3B" : " ",  "3C" : " "
}

winner_sets = [
    ("1A", "1B", "1C"), ("2A", "2B", "2C"), ("3A", "3B", "3C"),
    ("1A", "2A", "3A"), ("1B", "2B", "3B"), ("1C", "2C", "3C"),
    ("1A", "2B", "3C"), ("1C", "2B", "3A")                    
]

def display_board(g, scores, names):
    """Clears the screen and displays board with a scoreboard."""
    clear_output()
    print(f" SCORE: {names[0]} [{scores[names[0]]}] | {names[1]} [{scores[names[1]]}]")
    print("\n      A     B     C")
    print("   ___________________")
    print("   |     |     |     |")
    print(f"1  |  { g['1A'] }  |  { g['1B'] }  |  { g['1C'] }  |")
    print("   |_____|_____|_____|")
    print("   |     |     |     |")
    print(f"2  |  { g['2A'] }  |  { g['2B'] }  |  { g['2C'] }  |")
    print("   |_____|_____|_____|")
    print("   |     |     |     |")
    print(f"3  |  { g['3A'] }  |  { g['3B'] }  |  { g['3C'] }  |")
    print("   |_____|_____|_____|\n")

def check_winner(g, sets):
    for s in sets:
        if g[s[0]] == g[s[1]] == g[s[2]] != " ":
            return True
    return False

def play_game(names, scores):
    """Logic for a single round of Tic-Tac-Toe."""
    grid = grid_template.copy() # Fresh board for every round
    players_symbols = {names[0]: "X", names[1]: "O"}
    turn = 0
    
    while turn < 9:
        display_board(grid, scores, names)
        curr_name = names[0] if turn % 2 == 0 else names[1]
        curr_symbol = players_symbols[curr_name]
        
        # Move logic
        move = ""
        while move not in grid or grid[move] != " ":
            move = input(f" 👉 {curr_name} ({curr_symbol}), enter move: ").upper()
        
        grid[move] = curr_symbol
        
        if check_winner(grid, winner_sets):
            display_board(grid, scores, names)
            print(f" 🏆 CHAMPION: {curr_name}! 🏆")
            scores[curr_name] += 1
            return
        
        turn += 1
    
    display_board(grid, scores, names)
    print(" 🤝 DRAW! No winner this time. 🤝")

if __name__ == "__main__":
    print("--- WELCOME TO TIC-TAC-TOE PRO ---")
    n1 = input("Enter Player 1 Name (X): ") or "Player 1"
    n2 = input("Enter Player 2 Name (O): ") or "Player 2"
    
    player_names = [n1, n2]
    total_scores = {n1: 0, n2: 0}
    
    while True:
        play_game(player_names, total_scores)
        
        choice = input("\nPlay another round? (Y/N): ").lower()
        if choice != 'y':
            print(f"\nFinal Scores: {n1}: {total_scores[n1]} | {n2}: {total_scores[n2]}")
            print("Thanks for playing!")
            break

