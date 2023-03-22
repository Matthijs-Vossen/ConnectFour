import tkinter as tk
from tkmacosx import Button
from PIL import ImageTk, Image
import platform
from MiniMax import *
from Logic import *
from Lines import *

class Graphics:

    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Connect 4")
        self.root.resizable(False, False)

        # Create MiniMax object
        self.mm = MiniMax()
        self.ai_depth = 5

        # Create the game board frame and buttons
        self.game_frame = tk.Frame(self.root)
        self.game_frame.pack(side="left")
        self.start_game()

        # Create the AI menu
        self.ai_frame = tk.Frame(self.root)
        self.ai_frame.pack(side="right")
        self.ai_frame.config(width=300, height=220)
        self.ai_frame.pack_propagate(0)
        self.create_ai_frame()

        self.lines = Lines('lines/clippy_lines.txt')

        self.root.mainloop()

    def start_game(self):
        self.game = Logic()
        try:
            self.turn_label.destroy()
        except:
            pass

        w,h = 5,3
        os_windows = True
        if platform.system() == 'Darwin':
            os_windows = False
        # Create the game board as a grid of buttons
        self.buttons = []
        for i in range(6):
            row = []
            for j in range(7):
                if os_windows:
                    button = tk.Button(self.game_frame, width=w, height=h, bg='white',
                                    command=lambda column=j: self.make_move(column))
                else:
                    button = Button(self.game_frame, width=50, height=50, bg='white',
                                command=lambda column=j: self.make_move(column))
                button.grid(row=i, column=j, padx=2, pady=2)
                row.append(button)
            self.buttons.append(row)

        # Create a label to display the current player's turn
        self.turn_label = tk.Label(self.game_frame, text="", font=("Arial", 16))
        self.turn_label.grid(row=6, columnspan=7)

        # Create the menu buttons
        start_game_button = tk.Button(self.game_frame, text="New Game", command=self.start_game)
        start_game_button.grid(row=7, columnspan=7)

        settings_button = tk.Button(self.game_frame, text="Settings", command=self.settings)
        settings_button.grid(row=8, columnspan=7)

        settings_button = tk.Button(self.game_frame, text="Hint", command=self.set_suggestion)
        settings_button.grid(row=9, columnspan=7)

    def make_move(self, column):
        self.set_feedback(column)
        self.game.make_move(column)

        self.update_graphics(column)
        self.check_winner(column)

        ai_move, _ = self.mm.get_best_move(self.game, self.ai_depth)
        self.game.make_move(ai_move)
        
        self.update_graphics(ai_move)
        self.check_winner(ai_move)

    def update_graphics(self, column):
        for i in range(6):
            if self.game.board[i][column] == 'red':
                self.buttons[i][column].config(bg='red')
            elif self.game.board[i][column] == 'yellow':
                self.buttons[i][column].config(bg='yellow')

    def check_winner(self, column):
        winner = self.game.check_win()
        if winner:
            self.turn_label.config(text=f"{winner} player wins!")
            for i in range(6):
                for j in range(7):
                    color = self.game.board[i][j]
                    if color != ' ':
                        self.buttons[i][j]['state'] = tk.DISABLED
                        self.buttons[i][j].config(bg=color)
                    else:
                        self.buttons[i][j].config(state='disabled')

    def create_ai_frame(self):
        # Create an object of tkinter ImageTk
        self.img = ImageTk.PhotoImage(Image.open("images/clippy.png").resize((100,100), Image.ANTIALIAS))

        # Create a label to display the image
        self.img_label = tk.Label(self.ai_frame, image=self.img)
        self.img_label.pack(side="bottom")

        self.clippy_text_label = tk.Label(self.ai_frame, text="“Oh great, another game of Connect Four. Hi, I’m Clippy - your paperclip assistant. I guess I’m here to provide you with hints and suggestions as you play against the computer. Not like I have anything better to do. Let’s just get this over with.”", height=250, wraplength=290)
        self.clippy_text_label.pack(side="top")

    def set_suggestion(self):
        move, _ = self.mm.get_best_move(self.game, 3)
        line = self.lines.get_random_suggestion(move)
        self.clippy_text_label.config(text=line)

    def set_feedback(self, player_move):
        move, _ = self.mm.get_best_move(self.game, 3)
        if move != player_move:
            line = self.lines.get_random_feedback(move)
            self.clippy_text_label.config(text=line)
        else:
            self.clippy_text_label.config(text="")

    def settings(self):
        pass
