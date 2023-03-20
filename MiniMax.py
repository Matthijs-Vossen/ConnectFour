import copy
import Logic
import random

class MiniMax:
    def __init__(self) -> None:
        pass
    
    def make_move(self, board : Logic, col):
        # print("make ", col)
        # print("player ",board.player)
        bool = board.make_move(col)
        # board.print_board()  
        return bool
    def unmake_move(self, board, col):
        # print("unmake ", col)
        # print("player ",board.player)
        board.unmake_move(col)
        # board.print_board()  
        
    def get_best_move(self, logic : Logic, depth):
        board = copy.deepcopy(logic)
        
        player = logic.player
        best_i = -1
        best_v = -1
        if player == 1:
            maxV = -10000000
            maxI = -1
            for i in range(0,6):
                if not self.make_move(board, i):#move impossible
                    continue
                value = self.minimax(board, depth - 1,-100000000, 100000000, player)
                self.unmake_move(board, i)
                
                if value > maxV:
                    maxV = value
                    maxI = i
            best_i = maxI
            best_v = maxV
        else:
            minV = 10000000
            minI = -1
            for i in range(0,6):
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
        if player == 0:
            value = -100000000
            for i in range(7):
                if not self.make_move(board, i):
                    continue
                value = max(value, self.minimax(board, depth - 1,a,b, 1))
                self.unmake_move(board, i)
                if value > b:
                    return value
                a = max(a, value)
            return value
        else:
            value = 100000000
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
            return 100000000
        elif score == 'yellow':
            return -100000000
        else:
            return 0
    
    def evaluate_board(self, board):
        #check for draw
        return random.randrange(-10,10)