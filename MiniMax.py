import copy
import Logic
import random

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
        player = logic.player
        best_i = -1
        best_v = -1
        if player == 1:#maximizing player
            maxV = -10000000
            maxI = -1
            for i in range(0,7):
                if not self.make_move(board, i):#move impossible
                    continue
                value = self.minimax(board, depth - 1,-100000000, 100000000, player)
                self.unmake_move(board, i)
                print(value)
                if value > maxV:
                    maxV = value
                    maxI = i
            best_i = maxI
            best_v = maxV
        else:
            minV = 10000000
            minI = -1
            for i in range(0,7):
                if not self.make_move(board, i):#move impossible
                    continue
                value = self.minimax(board, depth - 1,-100000000, 100000000, player)
                self.unmake_move(board, i)
                
                if value < minV:
                    minV = value
                    minI = i
            best_i = minI
            best_v = minV
        return best_i, best_v
    
    def minimax(self, board, depth,a,b, player):
        # print(depth)
        if depth == 0 or board.check_win() != None:
            # print("win condition", depth)
            return self.evaluate(board)
        if player == 1:
            value = -100000
            for i in range(7):
                if not self.make_move(board, i):
                    continue
                value = max(value, self.minimax(board, depth - 1,a,b, 1))
                self.unmake_move(board, i)
                if value > b:
                    break
                a = max(a, value)
            return value
        else:
            value = 100000
            for i in range(7):
                if not self.make_move(board, i):
                    continue
                value = min(value, self.minimax(board, depth - 1,a,b, 1))
                self.unmake_move(board, i)
                if value < a:
                    break
                b = min(b, value)
            return value
    
    def evaluate(self, board):
        score = board.check_win()
        if score == None:
            return self.evaluate_board(board)
        
        if score == 'red':
            return 200000
        elif score == 'yellow':
            return -200000
        else:
            return 0
    
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
