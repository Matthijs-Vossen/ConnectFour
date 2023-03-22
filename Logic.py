
class Logic:
    """A class representing the game logic for Connect 4.

    This class manages the game board and allows players to make and unmake moves. It also includes methods for printing the board and checking if a node is occupied by a specific player.

    Attributes:
        board (list): A 2D list representing the game board.
        player (int): The current player (1 or 2).
    """

    def __init__(self):
        """Initialize the game logic.

        This method initializes the game board as an empty 6x7 grid and sets the current player to 1.

        Args:
            None

        Returns:
            None
        """
        
        # Initialize empty game board
        self.board = [[' ' for j in range(7)] for i in range(6)]
        
        # Set current player to 1
        self.player = 1

    def print_board(self):
        """Print the game board.

        This method prints the current state of the game board to the console.

        Args:
            None

        Returns:
            None
        """
        
        # Print each row of the game board
        for row in self.board:
            print("|".join(row))
        print('')

    def make_move(self, column: int) -> bool:
        """Make a move on the game board.

        This method places a piece on the specified column of the game board. It returns True if successful and False if unsuccessful (e.g. if column is full).

        Args:
            column (int): The column index where to place a piece.

        Returns:
            bool: True if successful, False otherwise.
        """
        
        # Check if column index is valid
        if not 0 <= column <= 6:
            raise ValueError("Column must be between 0 and 6")

        # Place piece on lowest available row in specified column
        for i in range(5, -1, -1):
            if self.board[i][column] == ' ':
                self.board[i][column] = 'red' if self.player == 1 else 'yellow'
                self.player = 2 if self.player == 1 else 1
                return True

        # Column is full; move unsuccessful
        return False

    def unmake_move(self, column: int):
        """Unmake a move on the game board.

        This method removes a piece from specified column of the game board. It raises an error if unsuccessful (e.g. if column is empty).

        Args:
            column (int): The column index from where to remove a piece.

        Returns:
            None
        """
            
        # Check if column index is valid
        if not 0 <= column <= 6:
                raise ValueError("Column must be between 0 and 6")

        # Remove piece from highest occupied row in specified column
        for i in range(6):
                if self.check_node(i ,column):
                    self.board[i][column] = ' '
                    self.player = 2 if self.player==1 else 1 
                    return
        
        # Column is empty; move unsuccessful 
        raise ValueError("Column is empty")

    def check_node(self, i: int, column: int) -> bool:
        """Check if a node is occupied by a specific player.

        This method checks if the node at the specified row and column is occupied by the opposite player of the current player.

        Args:
            i (int): The row index of the node to be checked.
            j (int): The column index of the node to be checked.

        Returns:
            bool: True if node is occupied by opposite player, False otherwise.
        """
        
        # Check if node is occupied by opposite player
        return ((self.player == 2 and self.board[i][column] == 'red') or
                (self.player == 1 and self.board[i][column] == 'yellow'))
    
    def check_win(self):
        """
        Check if there is a winner in the game.

        This method checks rows, columns and diagonals for four consecutive
        pieces of the same color. If a winner is found, it returns the color
        of the winner. If there is no winner but the board is full, it returns
        'draw'. Otherwise, it returns None.

        Returns:
            str: The color of the winner ('R' or 'Y'), 'draw' if there is a draw,
            or None if there is no winner yet.
        """
        
        # check rows
        for i in range(6):
            for j in range(4):
                if self.board[i][j] == self.board[i][j+1] == \
                self.board[i][j+2] == self.board[i][j+3] != ' ':
                    return self.board[i][j]

        # check columns
        for i in range(3):
            for j in range(7):
                if self.board[i][j] == self.board[i+1][j] == \
                self.board[i+2][j] == self.board[i+3][j] != ' ':
                    return self.board[i][j]

        # check diagonals
        for i in range(3):
            for j in range(4):
                if self.board[i][j] == self.board[i+1][j+1] == \
                self.board[i+2][j+2] == self.board[i+3][j+3] != ' ':
                    return self.board[i][j]
                    
        for i in range(3, 6):
            for j in range(4):
                if self.board[i][j] == self.board[i-1][j+1] == \
                self.board[i-2][j+2] ==self.board[i-3][j+3] != ' ': 
                    return self.board[i][j]

        #check if board is full 
        for i in range(7):
            if self.board[0][i]== ' ': 
                return None 

        print('draw')
        return'draw'
