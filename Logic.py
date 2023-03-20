class Logic:

    def __init__(self):
        self.board = [[' ' for j in range(7)] for i in range(6)]
        self.player = 1

    def print_board(self):
        for row in self.board:
            print("|".join(row))
        print('')

    def make_move(self, column):
        if not 0 <= column <= 6:
            raise ValueError("Column must be between 0 and 6")

        for i in range(5, -1, -1):
            if self.board[i][column] == ' ':
                self.board[i][column] = 'red' if self.player == 1 else 'yellow'
                self.player = 2 if self.player == 1 else 1
                # print("place loc: ", i,column)
                return True
            
        print("Column is full")
        return False
        

    def unmake_move(self, column):
        if not 0 <= column <= 6:
            raise ValueError("Column must be between 0 and 6")

        for i in range(6):
            if self.check_node(i , column):
                self.board[i][column] = ' '
                self.player = 2 if self.player == 1 else 1
                # print("remove loc: ", i,column)
                return
    
        raise ValueError("Column is empty")#should be impossible
    
    def check_node(self, i , column):
        if self.player == 2:
            return self.board[i][column] == 'red'
        return self.board[i][column] == 'yellow'
    
    def check_win(self):
        # check rows
        for i in range(6):
            for j in range(4):
                if self.board[i][j] == self.board[i][j+1] == self.board[i][j+2] == self.board[i][j+3] != ' ':
                    return self.board[i][j]

        # check columns
        for i in range(3):
            for j in range(7):
                if self.board[i][j] == self.board[i+1][j] == self.board[i+2][j] == self.board[i+3][j] != ' ':
                    return self.board[i][j]

        # check diagonals
        for i in range(3):
            for j in range(4):
                if self.board[i][j] == self.board[i+1][j+1] == self.board[i+2][j+2] == self.board[i+3][j+3] != ' ':
                    return self.board[i][j]

        for i in range(3, 6):
            for j in range(4):
                if self.board[i][j] == self.board[i-1][j+1] == self.board[i-2][j+2] == self.board[i-3][j+3] != ' ':
                    return self.board[i][j]

        for i in range(7):
            if self.board[0][i] == ' ':
                return None
        print('draw')
        return 'draw'
