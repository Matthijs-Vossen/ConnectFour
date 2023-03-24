import tkinter as tk
from tkmacosx import Button
from PIL import ImageTk, Image
import platform
from MiniMax import *
from Logic import *
from Lines import *

class Graphics:
    """A class representing the graphics for the Connect Four game.

    This class generates the graphics and interactions to allow users to play a game of Connect 4 against an AI opponent. 
    The AI difficulty can be adjusted in the settings menu. The game also includes Clippy, who provides suggestions and 
    feedback to the player.

    Attributes:
        root (tk.Tk): The root window for the game.
        mm (MiniMax): A MiniMax object used for determining the AI's moves.
        ai_depth (int): The depth of the MiniMax algorithm used by the AI.
        suggestion_move (int): The column index of the suggested move for the player.
        game_frame (tk.Frame): The frame containing the game board and buttons.
        ai_frame (tk.Frame): The frame containing the AI menu.
        lines (Lines): A Lines object containing Clippy's suggestion and feedback lines.
    """

    def __init__(self):
        """Initialize a Connect 4 game.

        This method creates a Tkinter window and sets up the game board, AI menu, and a Lines object for retrieving Clippy lines.
        It also creates a MiniMax object and sets the AI depth to 3.

        Args:
            None

        Returns:
            None
        """
        self.root = tk.Tk()
        self.root.title("Connect Four")
        self.root.resizable(False, False)

        # Create MiniMax object
        self.mm = MiniMax()
        self.ai_depth = 3
        self.suggestion_move = -1
        self.move_count = 0
        self.style = "Play against the computer"

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

        # Create Clippy lines
        self.lines = Lines('lines/clippy_lines.txt')

        # Start the main event loop
        self.root.mainloop()

    def start_game(self):
        """Start a new Connect 4 game.

        This method initializes a new game board with 6 rows and 7 columns, as well as a label to display
        the current player's turn. It also creates buttons for starting a new game, adjusting settings, and
        getting a hint. When a button is clicked, it calls the corresponding method.

        Args:
            None

        Returns:
            None
        """
        # Create a new game logic object
        self.game = Logic()

        # Destroy the turn label if it already exists
        try:
            self.turn_label.destroy()
        except:
            pass

        # Set button size based on OS
        w, h = 5, 3
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

        hint_button = tk.Button(self.game_frame, text="Hint", command=self.set_suggestion)
        hint_button.grid(row=9, columnspan=7)


    def make_move(self, column: int):
        """Make a move in the Connect 4 game.

        This method takes a column number as input, updates the game logic, and updates the graphics of the game board
        to reflect the new move. It then checks for a winner and, if there is none, makes a move for the AI player using
        the MiniMax algorithm.

        Args:
            column (int): The column number in which to make the move.

        Returns:
            None
        """
        self.move_count += 1
        # Update the game logic and graphics for the player's move
        if self.move_count > 1:
            self.set_feedback(column)

        move_made = self.game.make_move(column)
        self.update_graphics(column)
        win = self.check_winner()
        if win:
            return
        
        if self.style != "Play against yourself" and move_made:
            # Make a move for the AI player
            ai_move, score = self.mm.get_best_move(self.game, self.ai_depth)
            self.game.make_move(ai_move)
            self.update_graphics(ai_move)
            self.check_winner()

    def update_graphics(self, column: int):
        """Update the graphics of the game board to reflect a move.

        This method takes a column number as input and updates the color of the button(s) in that column to reflect the
        player who made the most recent move.

        Args:
            column (int): The column number to update.

        Returns:
            None
        """
        for i in range(6):
            if self.game.board[i][column] == 'red':
                self.buttons[i][column].config(bg='red')
            elif self.game.board[i][column] == 'yellow':
                self.buttons[i][column].config(bg='yellow')

    def check_winner(self):
        """Check if there is a winner and update the game state accordingly.

        This method takes a column number as input, checks if there is a winner in the game, and updates the game state and
        graphics accordingly. If there is a winner, it displays a message declaring the winner and disables the buttons on
        the game board.

        Args:
            None

        Returns:
            None
        """
        winner = self.game.check_win()
        if winner:
            if winner == 'yellow':
                self.turn_label.config(text="Computer wins!")
            else:
                self.turn_label.config(text="You win!")
            for i in range(6):
                for j in range(7):
                    color = self.game.board[i][j]
                    if color != ' ':
                        self.buttons[i][j]['state'] = tk.DISABLED
                        self.buttons[i][j].config(bg=color)
                    else:
                        self.buttons[i][j].config(state='disabled')
        return winner != None

    def create_ai_frame(self):
        """Create and set up the AI frame with an image of Clippy and a label for its text.

        Args:
            None

        Returns:
            None

        """
        # Create an object of tkinter ImageTk
        self.img = ImageTk.PhotoImage(Image.open("images/clippy.png").resize((100, 100), Image.ANTIALIAS))

        # Create a label to display the image
        self.img_label = tk.Label(self.ai_frame, image=self.img)
        self.img_label.pack(side="bottom")

        # Create a label for Clippy's text
        self.clippy_text_label = tk.Label(
            self.ai_frame, 
            text="\"Oh great, another game of Connect Four. Hi, I'm Clippy - your paperclip assistant. I guess I'm here to provide you with hints and suggestions as you play against the computer or yourself. Not like I have anything better to do. Let's just get this over with.\"",
            height=250, 
            wraplength=290
        )
        self.clippy_text_label.pack(side="top")

    def set_suggestion(self):
        """Set suggestion for the next move.

        This method uses the MiniMax algorithm to determine the best move for the AI player and sets it as a suggestion. It also updates Clippy's text label with a random suggestion line.

        Args:
            None

        Returns:
            None
        """
        # Get best move using MiniMax algorithm
        move, _ = self.mm.get_best_move(self.game, self.ai_depth + 1)

        # Set suggestion move
        self.suggestion_move = move

        nrows = len(self.game.board)
        for i in range(nrows):
            if self.game.board[i][move] != ' ':
                self.buttons[i-1][move].focus_set()
                break
            elif i == nrows-1:
                self.buttons[nrows-1][move].focus_set()
                break
        
        #self.game.board
        
        # Get random suggestion line from Clippy lines
        line = self.lines.get_random_suggestion(move+1)
        
        # Update Clippy text label with suggestion line
        self.clippy_text_label.config(text=line)

    def set_feedback(self, player_move: int):
        """Set feedback for the player's move.

        This method compares the player's move with the suggested move and updates Clippy's text label with a random feedback line if they are different. It also resets the suggestion move.

        Args:
            player_move (int): The column index of the player's move.

        Returns:
            None
        """
        
        # If no suggestion was made previously,
        # get best move using MiniMax algorithm
        if self.suggestion_move == -1:
            move, _ = self.mm.get_best_move(self.game, self.ai_depth + 1)
        else:
            move = self.suggestion_move

        # If suggested and actual moves are different,
        # update Clippy text label with feedback line
        if move != player_move:
            line = self.lines.get_random_feedback(move+1)
            self.clippy_text_label.config(text=line)
        else:
            self.clippy_text_label.config(text="")

        # Reset suggestion move
        self.suggestion_move = -1

    def settings(self):
        """Display the settings menu.

        This method clears the current game frame and creates a new frame for the settings menu. It allows the user to select the AI difficulty using a dropdown menu and includes a 'return' button to return to the game.

        Args:
            None

        Returns:
            None
        """
        
        # Clear the current game frame
        for widget in self.game_frame.winfo_children():
            widget.destroy()

        # Create a new frame for the settings menu
        settings_frame = tk.Frame(self.game_frame)
        settings_frame.pack(side="left")

        # Create label for AI difficulty selection
        self.ai_difficulty_label = tk.Label(settings_frame, text="Select AI Difficulty:")
        self.ai_difficulty_label.grid(row=0, column=0, padx=5, pady=5)

        # Create dropdown menu for AI difficulty selection
        self.style_var = tk.StringVar(settings_frame)
        self.style_var.set(str(self.style))
        style_dropdown = tk.OptionMenu(settings_frame, self.style_var,
                                            "Play against the computer", "Play against yourself")
        style_dropdown.grid(row=0, column=2, padx=5, pady=5)


        # Create dropdown menu for AI difficulty selection
        self.ai_difficulty_var = tk.StringVar(settings_frame)
        self.ai_difficulty_var.set(str(self.ai_depth))
        ai_difficulty_dropdown = tk.OptionMenu(settings_frame, self.ai_difficulty_var,
                                            "1", "2", "3", "4", "5")
        ai_difficulty_dropdown.grid(row=0, column=1, padx=5, pady=5)

        self.clippy_text_label.config(text="Can't even beat the computer huh? Interesting...")

        # Create 'return' button to return to game
        return_button = tk.Button(settings_frame,
                                text="Return",
                                command=lambda: self.return_to_game(settings_frame))
        return_button.grid(row=1,
                        column=0,
                        columnspan=2,
                        padx=5,
                        pady=5)


    def return_to_game(self, settings_frame: tk.Frame):
        """Return to game from settings menu.

        This method destroys the settings frame and returns to the game frame. It also updates the AI depth based on user selection in the settings menu.

        Args:
            settings_frame (tk.Frame): The frame containing the settings menu.

        Returns:
            None
        """
        
        # Update AI depth based on user selection
        self.ai_depth = int(self.ai_difficulty_var.get())
        self.style = str(self.style_var.get())
        
        # Destroy settings frame and return to game
        settings_frame.destroy()

        # Remove any text from 
        self.clippy_text_label.config(text="\"Oh great, another game of Connect Four. Hi, I'm Clippy - your paperclip assistant. I guess I'm here to provide you with hints and suggestions as you play against the computer or yourself. Not like I have anything better to do. Let's just get this over with.\"")

        # Start game with updated AI depth
        self.start_game()

