import tkinter as tk
from tkmacosx import Button
from PIL import ImageTk, Image
import platform
from MiniMax import *
from Logic import *

class Graphics:

    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Connect 4")
        self.root.resizable(False, False)

        # Create the game board frame and buttons
        self.game_frame = tk.Frame(self.root)
        self.game_frame.pack(side="left")
        self.start_game()

        # Create the AI menu
        self.ai_frame = tk.Frame(self.root)
        self.ai_frame.pack(side="right")
        self.ai_frame.config(width=300, height=150)
        self.ai_frame.pack_propagate(0)
        self.create_ai_frame()

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
        self.turn_label = tk.Label(self.game_frame, text=f"Player {self.game.player}'s turn", font=("Arial", 16))
        self.turn_label.grid(row=6, columnspan=7)

        # Create the menu buttons
        start_game_button = tk.Button(self.game_frame, text="New Game", command=self.start_game)
        start_game_button.grid(row=7, columnspan=7)

        settings_button = tk.Button(self.game_frame, text="Settings", command=self.settings)
        settings_button.grid(row=8, columnspan=7)

    def make_move(self, column):
        mm = MiniMax()
        self.game.make_move(column)

        # Update the button and label text to reflect the new state of the game
        for i in range(6):
            if self.game.board[i][column] == 'red':
                self.buttons[i][column].config(bg='red')
            elif self.game.board[i][column] == 'yellow':
                self.buttons[i][column].config(bg='yellow')

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
        else:
            self.turn_label.config(text=f"Player {self.game.player}'s turn")
        print(mm.get_best_move(self.game,3))

    def create_ai_frame(self):
        # Create an object of tkinter ImageTk
        self.img = ImageTk.PhotoImage(Image.open("images/clippy.png").resize((100,100), Image.ANTIALIAS))

        # Create a label to display the image
        self.img_label = tk.Label(self.ai_frame, image=self.img)
        self.img_label.pack(side="bottom")

        self.clippy_text_label = tk.Label(self.ai_frame, text="Lorem ipsum.", height=100, wraplength=290)
        self.clippy_text_label.pack(side="top")

    def set_suggestion(self, text: str):
        self.clippy_text_label.config(text=text)

    def settings(self):
        pass
