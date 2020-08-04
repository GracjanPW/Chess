from copy import deepcopy
class GameState:
    def __init__(self):
        self.board = [
            ['bR','bN','bB','bQ','bK','bB','bN','bR'],
            ['bP','bP','bP','bP','bP','bP','bP','bP'],
            ['--','--','--','--','--','--','--','--'],
            ['--','--','--','--','--','--','--','--'],
            ['--','--','--','--','--','--','--','--'],
            ['--','--','--','--','--','--','--','--'],
            ['wP','wP','wP','wP','wP','wP','wP','wP'],
            ['wR','wN','wB','wQ','wK','wB','wN','wR'],
        ]
        self.viewboard = deepcopy(self.board)
        self.whiteToMove = True
        self.moveLog = []
        self.viewmove = 0
        self.viewmode = False

    def make_move(self, move):
        
        self.board[move.start[0]][move.start[1]] = "--"
        self.board[move.end[0]][move.end[1]] = move.pieceMoved
        self.moveLog.append(move)
        self.whiteToMove = not self.whiteToMove
        self.viewmove = len(self.moveLog)
        self.viewboard = deepcopy(self.board)

    
    def undo_move(self):
        if self.viewmove > 0:
            self.viewmove -= 1
            
            move = self.moveLog[self.viewmove]
            self.viewboard[move.start[0]][move.start[1]] = self.viewboard[move.end[0]][move.end[1]]
            self.viewboard[move.end[0]][move.end[1]] = move.pieceCaptured
            self.viewmode = True

    def redo_move(self):
        if self.viewmove < len(self.moveLog):
            
            move = self.moveLog[self.viewmove]

            self.viewboard[move.start[0]][move.start[1]] = "--"
            self.viewboard[move.end[0]][move.end[1]] = move.pieceMoved
            self.viewmove += 1
            if self.viewmove == len(self.moveLog):
                self.viewmode = False
    
    def unmake_move(self):
        if len(self.moveLog) > 0:
            move = self.moveLog.pop()
            self.board[move.start[0]][move.start[1]] = self.board[move.end[0]][move.end[1]]
            self.board[move.end[0]][move.end[1]] = move.pieceCaptured
            self.viewmove = len(self.moveLog)
            self.viewboard = deepcopy(self.board)
            self.whiteToMove = not self.whiteToMove

    def possible_moves(self, col, row, c ,piece, board):
        if piece == 'P':
            return self.pawn(row, col,c, board)
        elif piece == 'N':
            return self.knight(row, col, c, board)
        elif piece == 'B':
            return self.bishop(row, col, c,board)
        elif piece == 'R':
            return self.rook(row, col, c, board)
        elif piece == 'Q':
            return self.queen(row, col, c, board)
        elif piece == 'K':
            return self.king(row, col, c, board)
        else:
            return []

    def legal_moves(self, col1, row1):
        c, piece = self.board[row1][col1][0],self.board[row1][col1][1]
        valid = []
        moves =  self.possible_moves(col1, row1, c, piece, self.board)
        print('\nmoves: ',moves)
        for move in moves:
            print('\nmove: ',move, '\nColor: ', c, '\npiece: ',piece)
            check = False
            board = deepcopy(self.board)
            board[row1][col1] = "--"
            board[move[0]][move[1]] = c+piece
            print('\n')
            for i in board:
                print(','.join(i))
            king = [(ix,iy) for ix in range(0,8) for iy in range(0,8) if board[ix][iy] == c+'K'][0]
            print('\nking at: ',king)
            for row in range(0,8):
                for col in range(0,8):
                    if board[row][col][0] != c and board[row][col][0] != '-':
                        c1, piece1 = board[row][col][0],board[row][col][1]
                        moves1 =  self.possible_moves(col, row, c1, piece1, board)
                        print('\npeice: ',piece1)
                        print('\nwith moves: ',moves1)
                        if king in moves1:
                            check = True
            if check:
                pass
            else:
                valid.append(move)
        return valid
        
    def pawn(self, row, col, c, board):
        moves = []
        if c == 'b':
            try:
                if board[row+1][col] == "--":
                    if row == 1 and board[row+2][col] == "--":
                        moves.append((row+1,col))
                        moves.append((row+2,col))
                    else:    
                        moves.append((row+1,col))
            except:
                pass
            try:
                if board[row+1][col-1][0] == 'w':
                    moves.append((row+1, col-1))
            except:
                pass
            try:
                if board[row+1][col+1][0] == 'w':
                    moves.append((row+1, col+1))
            except:
                pass
        else:
            try:
                if board[row-1][col] == "--":
                    if row == 6 and board[row-2][col] == "--":
                        moves.append((row-1,col))
                        moves.append((row-2,col))
                    else:
                        moves.append((row-1,col))
            except:
                pass
            try:
                if board[row-1][col-1][0] == 'b':
                    moves.append((row-1, col-1))
            except:
                pass
            try:
                if board[row-1][col+1][0] == 'b':
                    moves.append((row-1, col+1))
            except:
                pass
        moves1 = []
        for i in moves:
            if i[0] < 0 or i[1] < 0:
                pass
            else:
                moves1.append(i)
        return moves1
    
    def knight(self, row, col, c, board):
        index = (row, col)
        poss_moves = [(index[0]+2,index[1]+1),(index[0]+2,index[1]-1),
                 (index[0]-2,index[1]+1),(index[0]-2,index[1]-1),
                 (index[0]+1,index[1]+2),(index[0]-1,index[1]+2),
                 (index[0]+1,index[1]-2),(index[0]-1,index[1]-2)]
        moves = []
        for i in range(0,8):
            try:
                row,col = poss_moves[i][0],poss_moves[i][1]
                if board[row][col] == '--' or board[row][col][0] != c:
                    moves.append(poss_moves[i])
            except:
                pass

        moves1 = []
        for i in moves:
            if i[0] < 0 or i[1] < 0:
                pass
            else:
                moves1.append(i)
        return moves1

    def bishop(self, row, col, c, board):
        moves = []
        index = (row, col)
        row = 0
        col = 0
        try:
            while True:
                row +=1
                col +=1
                if board[index[0]+row][index[1]+col] == '--':
                    moves.append((index[0]+row,index[1]+col))
                elif board[index[0]+row][index[1]+col][0] != c:
                    moves.append((index[0]+row,index[1]+col))
                    break
                else:
                    break
        except:
            pass
        row = 0
        col = 0
        try:
            while True:
                row -=1
                col +=1
                if board[index[0]+row][index[1]+col] == '--':
                    moves.append((index[0]+row,index[1]+col))
                elif board[index[0]+row][index[1]+col][0] != c:
                    moves.append((index[0]+row,index[1]+col))
                    break
                else:
                    break
        except:
            pass

        col = 0
        row = 0
        try:
            while True:
                col -=1
                row +=1
                if board[index[0]+row][index[1]+col] == '--':
                    moves.append((index[0]+row,index[1]+col))
                elif board[index[0]+row][index[1]+col][0] != c:
                    moves.append((index[0]+row,index[1]+col))
                    break
                else:
                    break
        except:
            pass
        col = 0
        row = 0
        try:
            while True:
                col -=1
                row -=1
                if board[index[0]+row][index[1]+col] == '--':
                    moves.append((index[0]+row,index[1]+col))
                elif board[index[0]+row][index[1]+col][0] != c:
                    moves.append((index[0]+row,index[1]+col))
                    break
                else:
                    break
        except:
            pass
        moves1 = []
        for i in moves:
            if i[0] < 0 or i[1] < 0:
                pass
            else:
                moves1.append(i)
        return moves1

    def rook(self, row, col, c, board):
        moves = []
        index = (row,col)
        row = 0
        col = 0
        try:
            while True:
                row +=1
                if board[index[0]+row][index[1]] == '--':
                    moves.append((index[0]+row,index[1]))
                elif board[index[0]+row][index[1]][0] != c:
                    moves.append((index[0]+row,index[1]))
                    break
                else:
                    break
        except:
            pass
        row = 0
        try:
            while True:
                row -=1
                if board[index[0]+row][index[1]] == '--':
                    moves.append((index[0]+row,index[1]))
                elif board[index[0]+row][index[1]][0] != c:
                    moves.append((index[0]+row,index[1]))
                    break
                else:
                    break
        except:
            pass

        col = 0
        try:
            while True:
                col +=1
                if board[index[0]][index[1]+col] == '--':
                    moves.append((index[0],index[1]+col))
                elif board[index[0]][index[1]+col][0] != c:
                    moves.append((index[0],index[1]+col))
                    break
                else:
                    break
        except:
            pass
        col = 0
        try:
            while True:
                col -=1
                if board[index[0]][index[1]+col] == '--':
                    moves.append((index[0],index[1]+col))
                elif board[index[0]][index[1]+col][0] != c:
                    moves.append((index[0],index[1]+col))
                    break
                else:
                    break
        except:
            pass
        
        moves1 = []
        for i in moves:
            if i[0] < 0 or i[1] < 0:
                pass
            else:
                moves1.append(i)
        return moves1
    
    def queen(self, row, col, c, board):
        moves = []
        index = (row, col)
        row = 0
        col = 0
        try:
            while True:
                row +=1
                col +=1
                if board[index[0]+row][index[1]+col] == '--':
                    moves.append((index[0]+row,index[1]+col))
                elif board[index[0]+row][index[1]+col][0] != c:
                    moves.append((index[0]+row,index[1]+col))
                    break
                else:
                    break
        except:
            pass
        row = 0
        col = 0
        try:
            while True:
                row -=1
                col +=1
                if board[index[0]+row][index[1]+col] == '--':
                    moves.append((index[0]+row,index[1]+col))
                elif board[index[0]+row][index[1]+col][0] != c:
                    moves.append((index[0]+row,index[1]+col))
                    break
                else:
                    break
        except:
            pass

        col = 0
        row = 0
        try:
            while True:
                col -=1
                row +=1
                if board[index[0]+row][index[1]+col] == '--':
                    moves.append((index[0]+row,index[1]+col))
                elif board[index[0]+row][index[1]+col][0] != c:
                    moves.append((index[0]+row,index[1]+col))
                    break
                else:
                    break
        except:
            pass
        col = 0
        row = 0
        try:
            while True:
                col -=1
                row -=1
                if board[index[0]+row][index[1]+col] == '--':
                    moves.append((index[0]+row,index[1]+col))
                elif board[index[0]+row][index[1]+col][0] != c:
                    moves.append((index[0]+row,index[1]+col))
                    break
                else:
                    break
        except:
            pass
        row = 0
        col = 0
        try:
            while True:
                row +=1
                if board[index[0]+row][index[1]] == '--':
                    moves.append((index[0]+row,index[1]))
                elif board[index[0]+row][index[1]][0] != c:
                    moves.append((index[0]+row,index[1]))
                    break
                else:
                    break
        except:
            pass
        row = 0
        try:
            while True:
                row -=1
                if board[index[0]+row][index[1]] == '--':
                    moves.append((index[0]+row,index[1]))
                elif board[index[0]+row][index[1]][0] != c:
                    moves.append((index[0]+row,index[1]))
                    break
                else:
                    break
        except:
            pass

        col = 0
        try:
            while True:
                col +=1
                if board[index[0]][index[1]+col] == '--':
                    moves.append((index[0],index[1]+col))
                elif board[index[0]][index[1]+col][0] != c:
                    moves.append((index[0],index[1]+col))
                    break
                else:
                    break
        except:
            pass
        col = 0
        try:
            while True:
                col -=1
                if board[index[0]][index[1]+col] == '--':
                    moves.append((index[0],index[1]+col))
                elif board[index[0]][index[1]+col][0] != c:
                    moves.append((index[0],index[1]+col))
                    break
                else:
                    break
        except:
            pass
        moves1 = []
        for i in moves:
            if i[0] < 0 or i[1] < 0:
                pass
            else:
                moves1.append(i)
        return moves1

    def king(self, row, col, c, board):
        moves = []
        index = (row,col)
        poss_moves = [(index[0]+1,index[1]+1),(index[0]+1,index[1]),(index[0]+1,index[1]-1),
                      (index[0],index[1]+1)                      ,(index[0],index[1]-1),
                      (index[0]-1,index[1]+1),(index[0]-1,index[1]),(index[0]-1,index[1]-1)]
        for i in range(0,8):
            try:
                row,col = poss_moves[i][0],poss_moves[i][1]
                if board[row][col] == '--' or board[row][col][0] != c:
                    moves.append(poss_moves[i])
            except:
                pass
        moves1 = []
        for i in moves:
            if i[0] < 0 or i[1] < 0:
                pass
            else:
                moves1.append(i)
        return moves1 


class Move:
    ranksToRows = {
        "1":7, "2":6, "3":5, "4":4, "5":3, "6":2, "7":1, "8":0,
    }
    rowsToRanks = {
        v : k for k, v in ranksToRows.items()
    }
    filesToCols = {
        "h":7, "g":6, "f":5, "e":4, "d":3, "c":2, "b":1, "a":0,
    }
    colsToFiles = {
        v : k for k, v in filesToCols.items()
    }
    def __init__(self, start, end, board):
        self.start = start
        self.end = end
        self.pieceMoved = board[start[0]][start[1]]
        self.pieceCaptured = board[end[0]][end[1]]
    
    def get_chess_notation(self):
        return self.get_rank_file(self.start[0], self.start[1]) + self.get_rank_file(self.end[0], self.end[1]) 

    def get_rank_file(self, r, c):
        return self.colsToFiles[c] + self.rowsToRanks[r]