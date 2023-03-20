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
        Evaluates the given board for the given player.
        Returns a score representing the strength of the player's position.
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
        Returns a score representing the strength of the player's position in the window.
        """
        plus = 'red'
        neg = 'yellow'
        score = 0
        
        if window.count(plus) == 3 and window.count(' ') == 1:
            score += 10
        elif window.count(plus) == 2 and window.count(' ') == 2:
            score += 5
        elif window.count(plus) == 1 and window.count(' ') == 3:
            score += 2
        
        if window.count(neg) == 3 and window.count(' ') == 1:
            score -= 10
        elif window.count(neg) == 2 and window.count(' ') == 2:
            score -= 5
        elif window.count(neg) == 1 and window.count(' ') == 3:
            score -= 2
        
        return score
