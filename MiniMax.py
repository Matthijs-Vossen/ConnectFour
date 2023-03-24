import copy
import Logic
import random
import math

class MiniMax:
    def __init__(self) -> None:
        pass
    
    def make_move(self, board : Logic, col):
        bool = board.make_move(col)
        return bool
    
    def unmake_move(self, board, col):
        board.unmake_move(col)
        
    def get_best_move(self, logic : Logic, depth):
        """
        Function to find the best move using minimax with alpha beta pruning
        It will check for each possible move what minimax value the game will have
        returns the move with the greatest/lowest minimax value based on which player has to play
        """
        board = copy.deepcopy(logic)
        if board.player == 1:
            best_i = -1
            max_v = -math.inf
            for i in range(7):
                if not self.make_move(board, i):#move impossible
                    continue
                value = self.minimax(board,depth,-math.inf,math.inf,2)
                self.unmake_move(board,i)
                if value > max_v:
                    max_v = value
                    best_i = i
            return best_i, max_v
        else:
            best_i = -1
            min_v = math.inf
            for i in range(7):
                if not self.make_move(board, i):#move impossible
                    continue
                value = self.minimax(board,depth,-math.inf,math.inf,1)
                self.unmake_move(board,i)
                if value < min_v:
                    min_v = value
                    best_i = i
            return best_i, min_v

    
    def minimax(self, board, depth,a,b, player):
        """
        Recursive minimax function with alpha beta pruning
        Evaluates each move by playing each possible move and extracts the best possible strategy by evaluating the possible states the move will lead to
        The function will just evaluate the value of a given state of the board
        """
        score = board.check_win()
        if depth == 0 and score == None:
            return self.evaluate_board(board)
        
        if score == 'red':
            return 200000
        elif score == 'yellow':
            return -200000
        elif score == 'draw':
            return 0

        if player == 1:
            value = -math.inf

            for i in range(7):
                if not self.make_move(board, i):#move impossible
                    continue
                value = max(value, self.minimax(board,depth-1,a,b,2))
                self.unmake_move(board,i)

                if value > b:
                    break
                a = max(a, value)
            return value
        else:
            value = math.inf

            for i in range(7):
                if not self.make_move(board, i):#move impossible
                    continue
                value = min(value,self.minimax(board,depth-1,a,b,1))
                self.unmake_move(board,i)

                if value < a:
                    break
                b = min(b, value)
            return value
    
    def evaluate_board(self, b):
        """
        Evaluates the given board.
        Returns a score representing the strength of the position.
        A positive score means 'red' is winning, a negative score means 'yellow' is winning.
        It calculates the score by evaluating all the possible squares in lines of 4 on the board
        All these evaluations are summed together to get the final score
        See evaluate_window() to see how the 4 squares are evaluated
        """
        score = 0
        # Check rows for wins
        for row in range(6):
            for col in range(4):
                window = [b.board[row][col+i] for i in range(4)]
                score += self.evaluate_window(window)
        
        # Check columns for wins
        for col in range(7):
            for row in range(3):
                window = [b.board[row+i][col] for i in range(4)]
                score += self.evaluate_window(window)
        
        # Check diagonals (up-right)
        for row in range(3):
            for col in range(4):
                window = [b.board[row+i][col+i] for i in range(4)]
                score += self.evaluate_window(window)
        
        # Check diagonals (up-left)
        for row in range(3):
            for col in range(3, 7):
                window = [b.board[row+i][col-i] for i in range(4)]
                score += self.evaluate_window(window)
        
        return score


    def evaluate_window(self, window):
        """
        Evaluates a window of four pieces for the given player.
        Returns a score representing the strength of the position in the window.
        A positive score means 'red' is winning, a negative score means 'yellow' is winning.
        It gives a value of +/- 10 if a player has 3 stones in a row
        It gives a value of +/- 5 if a player has 3 stones in a row
        It gives a value of +/- 2 if a player has 3 stones in a row
        """
        plus = window.count('red')
        neg = window.count('yellow')
        no = window.count(' ')
        
        if plus == 3 and no == 1:
            return 10
        elif plus == 2 and no == 2:
            return 5
        elif plus == 1 and no == 3:
            return 2
        
        if neg == 3 and no == 1:
            return -10
        elif neg == 2 and no == 2:
            return -5
        elif neg == 1 and no == 3:
            return -2
        
        return 0
