import tkinter as tk
from tkinter import messagebox
import random
import time

# ---------- Common Dice ----------
def roll_dice():
    return random.randint(1, 6)

# ---------- Main Menu ----------
def show_main_menu():
    main = tk.Tk()
    main.title("GameHum3.0")
    main.geometry("400x400")

    tk.Label(main, text="Select a Game", font=("Arial", 20)).pack(pady=20)

    tk.Button(main, text="Cluedo", command=lambda: play_cluedo_gui(main)).pack(pady=10)
    tk.Button(main, text="Snakes and Ladders", command=lambda: play_snakes_gui(main)).pack(pady=10)
    tk.Button(main, text="Chess", command=lambda: play_chess_gui(main)).pack(pady=10)
    tk.Button(main, text="Football", command=lambda: play_football_gui(main)).pack(pady=10)
    tk.Button(main, text="Uno", command=lambda: play_uno_gui(main)).pack(pady=10)

    main.mainloop()

# ---------- Cluedo ----------
def play_cluedo_gui(parent):
    CHARACTERS = ["Miss Scarlett", "Colonel Mustard", "Mr. Green", "Mrs. Peacock", "Professor Plum"]
    WEAPONS = ["Candlestick", "Dagger", "Lead Pipe", "Revolver", "Rope"]
    ROOMS = ["Kitchen", "Ballroom", "Conservatory", "Dining Room", "Billiard Room", "Library", "Lounge", "Hall", "Study"]
    CROSS_OUT = {"characters": [], "weapons": [], "rooms": []}

    hidden_character = random.choice(CHARACTERS)
    hidden_weapon = random.choice(WEAPONS)
    hidden_room = random.choice(ROOMS)

    window = tk.Toplevel(parent)
    window.title("Cluedo")
    window.geometry("500x400")

    current_room = tk.StringVar(value=random.choice(ROOMS))

    def update_game():
        roll = roll_dice()
        idx = ROOMS.index(current_room.get())
        current_room.set(ROOMS[(idx + roll) % len(ROOMS)])
        room = current_room.get()
        clue = f"Clue in {room}: ???"
        clue_label.config(text=clue)
        status_label.config(text=f"Moved to {room}, rolled a {roll}")

    def make_guess():
        guess_char = char_entry.get()
        guess_weap = weap_entry.get()
        guess_room = current_room.get()

        if guess_char == hidden_character and guess_weap == hidden_weapon and guess_room == hidden_room:
            messagebox.showinfo("Cluedo", "Correct guess! You win!")
            window.destroy()
        else:
            messagebox.showwarning("Wrong", "Wrong guess. Try again.")
            CROSS_OUT["characters"].append(guess_char)
            CROSS_OUT["weapons"].append(guess_weap)
            CROSS_OUT["rooms"].append(guess_room)

    tk.Label(window, text="Current Room:").pack()
    tk.Label(window, textvariable=current_room).pack()
    tk.Button(window, text="Roll Dice and Move", command=update_game).pack(pady=5)

    clue_label = tk.Label(window, text="Clue: ???")
    clue_label.pack()

    tk.Label(window, text="Make a Guess:").pack()
    char_entry = tk.Entry(window)
    weap_entry = tk.Entry(window)
    char_entry.pack()
    weap_entry.pack()

    tk.Button(window, text="Guess", command=make_guess).pack(pady=5)
    status_label = tk.Label(window, text="")
    status_label.pack()

# ---------- Snakes and Ladders ----------
def play_snakes_gui(parent):
    window = tk.Toplevel(parent)
    window.title("Snakes and Ladders")
    window.geometry("300x200")

    player_pos = [0, 0]
    turn = [0]
    board_size = 100

    snakes = {16: 6, 47: 26, 49: 11, 56: 53, 62: 19, 64: 60, 87: 24, 93: 73, 95: 75, 98: 78}
    ladders = {1: 38, 4: 14, 9: 31, 21: 42, 28: 84, 36: 44, 51: 67, 71: 91, 80: 100}

    status = tk.StringVar()

    def next_turn():
        roll = roll_dice()
        player = turn[0]
        pos = player_pos[player] + roll
        if pos > board_size:
            pos = player_pos[player]
        if pos in snakes:
            pos = snakes[pos]
        elif pos in ladders:
            pos = ladders[pos]
        player_pos[player] = pos

        status.set(f"Player {player+1} rolled {roll} → square {pos}")
        if pos == board_size:
            messagebox.showinfo("Game Over", f"Player {player+1} wins!")
            window.destroy()
        elif roll != 6:
            turn[0] = 1 - player

    tk.Label(window, text="Snakes & Ladders").pack()
    tk.Button(window, text="Roll Dice", command=next_turn).pack(pady=10)
    tk.Label(window, textvariable=status).pack()

# ---------- Chess ----------
def play_chess_gui(parent):
    window = tk.Toplevel(parent)
    window.title("Chess")
    window.geometry("400x300")

    board = [[" " for _ in range(8)] for _ in range(8)]
    board[0] = ["R", "N", "B", "Q", "K", "B", "N", "R"]
    board[1] = ["P"] * 8
    board[6] = ["p"] * 8
    board[7] = ["r", "n", "b", "q", "k", "b", "n", "r"]

    def print_board():
        output.delete("1.0", tk.END)
        for row in board:
            output.insert(tk.END, " ".join(row) + "\n")

    def move_piece():
        move = entry.get().strip()
        try:
            start, end = move.split()
            sc, sr = ord(start[0]) - ord('a'), 8 - int(start[1])
            ec, er = ord(end[0]) - ord('a'), 8 - int(end[1])
            board[er][ec] = board[sr][sc]
            board[sr][sc] = " "
            print_board()
        except:
            messagebox.showwarning("Invalid", "Move format invalid")

    tk.Label(window, text="Enter Move (e.g., e2 e4):").pack()
    entry = tk.Entry(window)
    entry.pack()
    tk.Button(window, text="Move", command=move_piece).pack()

    output = tk.Text(window, height=10, width=25)
    output.pack()
    print_board()

# ---------- Football ----------
def play_football_gui(parent):
    window = tk.Toplevel(parent)
    window.title("Football")
    window.geometry("300x200")

    score1 = 0
    score2 = 0
    round_label = tk.Label(window, text="Turn 1")
    score_label = tk.Label(window, text="Team 1: 0 | Team 2: 0")
    turn = [1]

    def play_turn():
        nonlocal score1, score2
        if turn[0] > 10:
            if score1 > score2:
                winner = "Team 1 wins!"
            elif score2 > score1:
                winner = "Team 2 wins!"
            else:
                winner = "It's a draw!"
            messagebox.showinfo("Result", winner)
            window.destroy()
            return
        score1 += random.randint(0, 1)
        score2 += random.randint(0, 1)
        round_label.config(text=f"Turn {turn[0]}")
        score_label.config(text=f"Team 1: {score1} | Team 2: {score2}")
        turn[0] += 1

    round_label.pack()
    score_label.pack()
    tk.Button(window, text="Next Turn", command=play_turn).pack()

# ---------- Uno ----------
def play_uno_gui(parent):
    window = tk.Toplevel(parent)
    window.title("Uno")
    window.geometry("400x300")

    colors = ["Red", "Yellow", "Green", "Blue"]
    values = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "Skip", "Reverse", "Draw Two"]
    deck = [f"{c} {v}" for c in colors for v in values] * 2
    random.shuffle(deck)

    player = [deck.pop() for _ in range(7)]
    computer = [deck.pop() for _ in range(7)]
    discard = [deck.pop()]
    top_card = tk.StringVar(value=f"Top Card: {discard[-1]}")
    player_hand = tk.StringVar(value=", ".join(player))

    def draw_card():
        if deck:
            card = deck.pop()
            player.append(card)
            player_hand.set(", ".join(player))

    def play_card():
        card = entry.get()
        if card in player and valid_play(card, discard[-1]):
            player.remove(card)
            discard.append(card)
            top_card.set(f"Top Card: {card}")
            player_hand.set(", ".join(player))
            if not player:
                messagebox.showinfo("Uno", "You win!")
                window.destroy()

    def valid_play(card, top):
        color, value = card.split()
        top_color, top_value = top.split()
        return color == top_color or value == top_value

    tk.Label(window, textvariable=top_card).pack()
    tk.Label(window, textvariable=player_hand).pack()
    entry = tk.Entry(window)
    entry.pack()
    tk.Button(window, text="Play", command=play_card).pack()
    tk.Button(window, text="Draw", command=draw_card).pack()

# ---------- Launch GUI ----------
if __name__ == "__main__":
    show_main_menu()