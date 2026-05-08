# ==========================================
#  BATTLE FOR THE SPICED KINGDOM
#  Zero Imports Allowed. Pure Python.
# ==========================================

# --- ANSI COLORS & GRAPHICS ---
C_X = '\033[92m'      # Goblin Green
C_O = '\033[96m'      # Elven Cyan
C_BD = '\033[90m'     # Dark Gray
C_TITLE = '\033[1;93m'# Gold
C_ERR = '\033[91m'    # Red
C_TXT = '\033[37m'    # White
C_RST = '\033[0m'     # Reset
CLEAR_SCREEN = '\033[H\033[J'

ASCII_ART = f"""{C_TITLE}
         ,      ,
        /(.-""-.)\\
    |\\  \\/      \\/  /|
    | \\ / =.  (> \\ / |
    \\( \\   o\\/o   / )/
     \\_, '-/  \\-' ,_/
       /   \\__/   \\
       \\ \\__/\\__/ /
     ___\\ \\|--|/ /___
    /`    \\    /    `\\
"PUNY ELVES! THE SPICE IS OURS!"
How to Play (Read Before Running!)
When it is your turn, you will command your troops using terminal text commands:
•	Standard Drop: Just type the coordinate. Example: B2
•	The Snake (Move): Type SNAKE followed by the piece you want to move, and where to. Example: SNAKE B2 C2
•	The Bribe: Type BRIBE and the enemy coordinate. Example: BRIBE D4 (Gives enemy 2 extra turns).
•	The Split: Type SPLIT followed by your piece, and the adjacent spot to push into. Example: SPLIT B2 B3 (Gives enemy 1 extra turn. Cannot target the exact center of the board).
{C_RST}
"""

EAGLE_TAUNTS = [
    "Oh look, a move. How staggeringly mediocre.",
    "Did you read that tactic in 'Warfare for Toddlers'?",
    "We've seen better strategy from a blind badger.",
    "Are you trying to lose, or does it just come naturally?",
    "A brilliant move! ...If it were opposite day.",
    "Even the mud at the bottom of the swamp is embarrassed for you."
]

# --- CORE LOGIC & STATE ---
def pseudo_random(seed_str, max_val):
    # Generates a pseudo-random number based on string hashing
    val = sum(ord(c) * (i + 1) for i, c in enumerate(seed_str))
    return val % max_val

def build_board(size):
    return [[' ' for _ in range(size)] for _ in range(size)]

def draw_board(board, size, player_X, player_O, msg=""):
    print(CLEAR_SCREEN, end='')
    print(ASCII_ART)
    print(f"{C_TXT}=== BATTLE FOR THE SPICED KINGDOM ==={C_RST}\n")
    
    # Headers
    letters = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    header = "    " + "   ".join(letters[:size])
    print(header)
    
    for r in range(size):
        row_str = f"{r}  "
        for c in range(size):
            val = board[r][c]
            if val == 'X': color = C_X
            elif val == 'O': color = C_O
            else: color = C_BD
            
            display_val = val if val != ' ' else '.'
            row_str += f" {color}{display_val}{C_RST} |"
        
        print(row_str[:-1])
        if r < size - 1:
            print("   " + "---+-" * (size-1) + "---")
            
    print("\n" + msg + "\n")

def check_victory(board, size, target):
    # Dynamic win checking for N-in-a-row
    for r in range(size):
        for c in range(size):
            if board[r][c] == ' ': continue
            symbol = board[r][c]
            
            # Check 4 directions: Right, Down, Down-Right, Down-Left
            directions = [(0,1), (1,0), (1,1), (1,-1)]
            for dr, dc in directions:
                win = True
                for i in range(target):
                    nr, nc = r + (dr * i), c + (dc * i)
                    if nr < 0 or nr >= size or nc < 0 or nc >= size or board[nr][nc] != symbol:
                        win = False
                        break
                if win:
                    return symbol
                    
    # Check Draw
    if all(board[r][c] != ' ' for r in range(size) for c in range(size)):
        return "DRAW"
    return None

def parse_coord(coord_str, size):
    # Converts "B2" to (2, 1) -> (row, col)
    if len(coord_str) != 2: return None
    col_str, row_str = coord_str[0].upper(), coord_str[1]
    letters = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    if col_str not in letters[:size] or not row_str.isdigit(): return None
    col, row = letters.index(col_str), int(row_str)
    if row < 0 or row >= size: return None
    return (row, col)

# --- THE HEURISTIC AI ---
def get_ai_move(board, size, target, my_symbol):
    enemy = 'O' if my_symbol == 'X' else 'X'
    
    # 1. Check for immediate win
    for r in range(size):
        for c in range(size):
            if board[r][c] == ' ':
                board[r][c] = my_symbol
                if check_victory(board, size, target) == my_symbol:
                    board[r][c] = ' '
                    return f"PLACE {r} {c}"
                board[r][c] = ' '
                
    # 2. Check for immediate block
    for r in range(size):
        for c in range(size):
            if board[r][c] == ' ':
                board[r][c] = enemy
                if check_victory(board, size, target) == enemy:
                    board[r][c] = ' '
                    return f"PLACE {r} {c}"
                board[r][c] = ' '

    # 3. Find a spot next to own piece to build lines
    adjacents = []
    for r in range(size):
        for c in range(size):
            if board[r][c] == ' ':
                for dr, dc in [(-1,0), (1,0), (0,-1), (0,1), (1,1), (-1,-1)]:
                    if 0 <= r+dr < size and 0 <= c+dc < size and board[r+dr][c+dc] == my_symbol:
                        adjacents.append((r, c))
                        break
    if adjacents:
        # Pseudo-randomly pick one
        seed = str(board)
        idx = pseudo_random(seed, len(adjacents))
        r, c = adjacents[idx]
        return f"PLACE {r} {c}"

    # 4. Fallback: Pseudo-random empty spot
    empty = [(r, c) for r in range(size) for c in range(size) if board[r][c] == ' ']
    idx = pseudo_random(str(board), len(empty))
    r, c = empty[idx]
    return f"PLACE {r} {c}"

# --- GAME ENGINE ---
def play_game():
    print(CLEAR_SCREEN + ASCII_ART)
    print("Choose your Battlefield:")
    print("1. New Fish (3x3) - First to 3")
    print("2. Pentangle Penguin (5x5) - First to 4")
    print("3. Octopus Octagon (8x8) - First to 5")
    
    choice = ""
    while choice not in ['1', '2', '3']:
        choice = input("Select 1, 2, or 3 > ")
        
    if choice == '1': size, target = 3, 3
    elif choice == '2': size, target = 5, 4
    else: size, target = 8, 5

    print("\nChoose your Faction:")
    print("X. Lord Greenylegs (Goblins)")
    print("O. General Goodylegs (Elves)")
    
    faction = ""
    while faction not in ['X', 'O']:
        faction = input("Select X or O > ").upper()
        
    human = faction
    ai = 'O' if human == 'X' else 'X'
    
    board = build_board(size)
    current = 'X' # X always goes first
    
    inventory = {
        'X': {'SNAKE': 1, 'BRIBE': 1, 'SPLIT': 1},
        'O': {'SNAKE': 1, 'BRIBE': 1, 'SPLIT': 1} # AI has them, but lacks the brain to use them!
    }
    extra_turns = {'X': 0, 'O': 0}
    
    msg = "The battle begins! Eagle Gods are watching."
    
    while True:
        draw_board(board, size, human, ai, msg)
        
        # Display Status
        print(f"[{current}'s Turn] Extra Turns left: {extra_turns[current]}")
        inv = inventory[current]
        print(f"Specials Available: SNAKE({inv['SNAKE']}), BRIBE({inv['BRIBE']}), SPLIT({inv['SPLIT']})")
        print("Commands: 'B2', 'SNAKE B2 C2', 'BRIBE B2', 'SPLIT B2 C2'")
        
        turn_success = False
        
        if current == human:
            cmd = input(f"\n{C_TITLE}Commander, your orders? > {C_RST}").upper().split()
            
            if not cmd: continue
            
            # STANDARD PLACE
            if len(cmd) == 1:
                coord = parse_coord(cmd[0], size)
                if coord and board[coord[0]][coord[1]] == ' ':
                    board[coord[0]][coord[1]] = current
                    turn_success = True
                    msg = "Piece deployed."
                else:
                    msg = f"{C_ERR}Invalid coordinate or space occupied!{C_RST}"
                    
            # SNAKE
            elif cmd[0] == "SNAKE" and len(cmd) == 3:
                if inventory[current]['SNAKE'] < 1:
                    msg = f"{C_ERR}You have no Snake brigades left!{C_RST}"
                else:
                    c1, c2 = parse_coord(cmd[1], size), parse_coord(cmd[2], size)
                    if c1 and c2 and board[c1[0]][c1[1]] == current and board[c2[0]][c2[1]] == ' ':
                        board[c1[0]][c1[1]] = ' '
                        board[c2[0]][c2[1]] = current
                        inventory[current]['SNAKE'] -= 1
                        turn_success = True
                        msg = "The Snake strikes! Piece moved."
                    else:
                        msg = f"{C_ERR}Invalid Snake move.{C_RST}"

            # BRIBE
            elif cmd[0] == "BRIBE" and len(cmd) == 2:
                if inventory[current]['BRIBE'] < 1:
                    msg = f"{C_ERR}You have no Bribes left!{C_RST}"
                else:
                    c1 = parse_coord(cmd[1], size)
                    enemy = 'O' if current == 'X' else 'X'
                    if c1 and board[c1[0]][c1[1]] == enemy:
                        board[c1[0]][c1[1]] = current
                        inventory[current]['BRIBE'] -= 1
                        extra_turns[enemy] += 2
                        turn_success = True
                        msg = "Bribe successful! Enemy unit flipped. They gain 2 extra turns!"
                    else:
                        msg = f"{C_ERR}Invalid Bribe target.{C_RST}"

            # SPLIT
            elif cmd[0] == "SPLIT" and len(cmd) == 3:
                if inventory[current]['SPLIT'] < 1:
                    msg = f"{C_ERR}You have no Splits left!{C_RST}"
                else:
                    c1, c2 = parse_coord(cmd[1], size), parse_coord(cmd[2], size)
                    center = (size // 2, size // 2)
                    enemy = 'O' if current == 'X' else 'X'
                    if c1 and c2 and c2 != center:
                        if board[c1[0]][c1[1]] == current:
                            # Check adjacency
                            if abs(c1[0]-c2[0]) <= 1 and abs(c1[1]-c2[1]) <= 1:
                                if board[c2[0]][c2[1]] in [' ', enemy]:
                                    board[c2[0]][c2[1]] = current
                                    inventory[current]['SPLIT'] -= 1
                                    extra_turns[enemy] += 1
                                    turn_success = True
                                    msg = "Split executed! You pushed into the space. Enemy gains 1 extra turn."
                                else: msg = f"{C_ERR}Cannot split into your own piece!{C_RST}"
                            else: msg = f"{C_ERR}Split target must be adjacent!{C_RST}"
                        else: msg = f"{C_ERR}Must select your own piece to split!{C_RST}"
                    else: msg = f"{C_ERR}Invalid Split. Cannot push into the center!{C_RST}"
                    
            else:
                msg = f"{C_ERR}Eagle Gods squawk: 'Learn to speak clearly, mortal!'{C_RST}"
                
        else: # AI Turn
            msg = f"{current} is thinking..."
            draw_board(board, size, human, ai, msg)
            
            # To pause slightly without import time, we do useless math
            for _ in range(5000000): pass 
            
            ai_cmd = get_ai_move(board, size, target, current).split()
            r, c = int(ai_cmd[1]), int(ai_cmd[2])
            board[r][c] = current
            turn_success = True
            
            letters = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
            msg = f"Enemy deployed troops to {letters[c]}{r}."
            
        # Turn Resolution
        if turn_success:
            # Random Eagle Taunt
            if pseudo_random(str(board), 100) > 60:
                taunt = EAGLE_TAUNTS[pseudo_random(str(board), len(EAGLE_TAUNTS))]
                msg += f"\n{C_TITLE}[Eagle God]: \"{taunt}\"{C_RST}"

            # Win Check
            winner = check_victory(board, size, target)
            if winner:
                draw_board(board, size, human, ai, f"{C_TITLE}THE DUST SETTLES...{C_RST}")
                if winner == 'X':
                    print(f"{C_X}Lord Greenylegs cackles! The Spiced Kingdom falls to the goblin horde!{C_RST}")
                elif winner == 'O':
                    print(f"{C_O}General Goodylegs stands victorious! The Spiced Kingdom is safe!{C_RST}")
                else:
                    print(f"{C_BD}Total annihilation. Both armies collapse. The Eagle Gods sigh.{C_RST}")
                break

            # Turn passing logic
            if extra_turns[current] > 0:
                extra_turns[current] -= 1
                msg += f"\n>>> {current} takes an EXTRA TURN! <<<"
            else:
                current = 'O' if current == 'X' else 'X'

if __name__ == "__main__":
    play_game()
