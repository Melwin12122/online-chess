import pygame
import os
from .constants import CELL_SIZE


class Piece:
    newGame = True

    def __init__(self, row, col, colour):
        self.row = row
        self.col = col
        self.colour = colour
        self.img = None
        self.king = False
        self.queen = False
        self.pawn = False
        self.knight = False
        self.rook = False
        self.bishop = False
        self.moved = False
        self.move_list = [] # Moves which could be moved
        self.possible_move = [] # Moves beyond opponent piece
        self.saving_move = [] # Moves which could backup a same piece
        if Piece.newGame:
            Piece.black_pieces = []
            Piece.white_pieces = []
            Piece.b_check = False
            Piece.w_check = False
            Piece.b_checkmate = False
            Piece.w_checkmate = False
            Piece.b_stalemate = False
            Piece.w_stalemate = False
            Piece.newGame = False

        if self.colour == 'w':
            Piece.white_pieces.append(self)
        elif self.colour == 'b':
            Piece.black_pieces.append(self)

    def draw(self, win):
        x = self.col * CELL_SIZE
        y = self.row * CELL_SIZE

        win.blit(self.img, (x, y))

    def cause_check(self, moves):
        temp2 = []
        if self.colour == 'w':
            for wp in Piece.white_pieces:
                if wp.king:
                    for bp in Piece.black_pieces:
                        if (wp.row, wp.col) in bp.possible_move: 
                            temp = self.find_moves(wp, bp)
                            if (self.row, self.col) in temp:
                                if (bp.row, bp.col) in moves:
                                    temp2.append((bp.row, bp.col))
                                for move in temp:
                                    if move in moves:
                                        temp2.append(move)
                                return True, temp2
            
        elif self.colour == 'b':
            for bp in Piece.black_pieces:
                if bp.king:
                    for wp in Piece.white_pieces:
                        if (bp.row, bp.col) in wp.possible_move:
                            temp = self.find_moves(bp, wp)
                            if (self.row, self.col) in temp:
                                if (wp.row, wp.col) in moves:
                                    temp2.append((wp.row, wp.col))
                                for move in temp:
                                    if move in moves:
                                        temp2.append(move)
                                return True, temp2

        return False, ()

    def check_moves(self, moves):
        temp3 = []
        if self.colour == 'w':
            if Piece.w_check:
                for wp in Piece.white_pieces:
                    if wp.king:
                        for bp in Piece.black_pieces:
                            if (wp.row, wp.col) in bp.move_list:
                                if (bp.row, bp.col) in moves:
                                    temp3.append((bp.row, bp.col))
                                block_moves = self.find_moves(wp, bp)
                                for move in moves:
                                    if move in block_moves:
                                        temp3.append(move)
        elif self.colour == 'b':
            if Piece.b_check:
                for bp in Piece.black_pieces:
                    if bp.king:
                        for wp in Piece.white_pieces:
                            if (bp.row, bp.col) in wp.move_list:
                                if (wp.row, wp.col) in moves:
                                    temp3.append((wp.row, wp.col))
                                block_moves = self.find_moves(bp, wp)
                                for move in moves:
                                    if move in block_moves:
                                        temp3.append(move)
        return temp3


    def find_moves(self, one, other):
        moves = []
        if one.row == other.row:
            incr = -1 if other.col > one.col else 1
            for i in range(other.col+incr, one.col, incr):
                moves.append((one.row, i))
        elif one.col == other.col:
            incr = -1 if other.row > one.row else 1
            for i in range(other.row+incr, one.row, incr):
                moves.append((i, one.col))
        elif abs(one.row - other.row) == abs(one.col - other.col):
            r = r_incr = -1 if other.row > one.row else 1
            c = c_incr = -1 if other.col > one.col else 1
            if other.col < one.col:
                for i in range(other.col+1, one.col):
                    moves.append((other.row+r_incr, other.col+c_incr))
                    r_incr += r
                    c_incr += c
            elif other.col > one.col:
                for i in range(one.col+1, other.col):
                    moves.append((other.row+r_incr, other.col+c_incr))
                    r_incr += r
                    c_incr += c
        return moves

    def move_straight(self, board, moves, temp, temp2):
        r = self.row
        c = self.col
        beyond = False
        # Up 
        while r > 0:
            r -= 1
            if not beyond:
                if board[r][c] == 0:
                    moves.append((r, c))
                elif board[r][c].colour == self.colour:
                    temp2.append((r, c))
                    temp.append((r, c))
                    break
                elif board[r][c].colour != self.colour:
                    moves.append((r, c))
                    beyond = True
            else:
                if board[r][c] == 0:
                    temp.append((r, c))
                elif board[r][c].colour != self.colour:
                    temp.append((r, c))
                    break
                elif board[r][c].colour == self.colour and board[r+1][c] != 0 and board[r+1][c].king:
                    temp2.append((r, c))
                    break
        
        r = self.row
        beyond = False
        # Down
        while r < 7:
            r += 1
            if not beyond:
                if board[r][c] == 0:
                    moves.append((r, c))
                elif board[r][c].colour == self.colour:
                    temp.append((r, c))
                    temp2.append((r, c))
                    break
                elif board[r][c].colour != self.colour:
                    moves.append((r, c))
                    beyond = True
            else:
                if board[r][c] == 0:
                    temp.append((r, c))
                elif board[r][c].colour != self.colour:
                    temp.append((r, c))
                    break
                elif board[r][c].colour == self.colour and board[r-1][c] != 0 and board[r-1][c].king:
                    temp2.append((r, c))
                    break

        r = self.row
        c = self.col
        beyond = False
        # Left
        while c > 0:
            c -= 1
            if not beyond:
                if board[r][c] == 0:
                    moves.append((r, c))
                elif board[r][c].colour == self.colour:
                    temp.append((r, c))
                    temp2.append((r, c))
                    break
                elif board[r][c].colour != self.colour:
                    moves.append((r, c))
                    beyond = True
            else:
                if board[r][c] == 0:
                    temp.append((r, c))
                elif board[r][c].colour != self.colour:
                    temp.append((r, c))
                    break
                elif board[r][c].colour == self.colour and board[r][c+1] != 0 and board[r][c+1].king:
                    temp2.append((r, c))
                    break
        
        c = self.col
        beyond = False
        # Right
        while c < 7:
            c += 1
            if not beyond:
                if board[r][c] == 0:
                    moves.append((r, c))
                elif board[r][c].colour == self.colour:
                    temp.append((r, c))
                    temp2.append((r, c))
                    break
                elif board[r][c].colour != self.colour:
                    moves.append((r, c))
                    beyond = True
            else:
                if board[r][c] == 0:
                    temp.append((r, c))
                elif board[r][c].colour != self.colour:
                    temp.append((r, c))
                    break
                elif board[r][c].colour == self.colour and board[r][c-1] != 0 and board[r][c-1].king:
                    temp2.append((r, c))
                    break

    def move_diagonal(self, board, moves, temp, temp2):
        r = self.row
        lc = self.col # left column
        rc = self.col # right column
        Lbeyond = False
        Rbeyond = False

        # Diagonal Up
        while r > 0:
            r -= 1

            lc -= 1
            if lc >= 0 and not Lbeyond:
                if board[r][lc] == 0:
                    moves.append((r, lc))
                elif board[r][lc].colour == self.colour:
                    temp.append((r, lc))
                    temp2.append((r, lc))
                    lc = -1 # Stop running this block
                elif board[r][lc].colour != self.colour:
                    moves.append((r, lc))
                    Lbeyond = True
            elif lc >= 0 and Lbeyond:
                if board[r][lc] == 0:
                    temp.append((r, lc))
                elif board[r][lc].colour != self.colour:
                    temp.append((r, lc))
                    lc = -1
                    Lbeyond = False
                elif board[r][lc].colour == self.colour and board[r+1][lc+1] != 0 and board[r+1][lc+1].king:
                    temp2.append((r, lc))
                    lc = -1
                    Lbeyond = False

            rc += 1
            if rc <= 7 and not Rbeyond:
                if board[r][rc] == 0:
                    moves.append((r, rc))
                elif board[r][rc].colour == self.colour:
                    temp.append((r, rc))
                    temp2.append((r, rc))
                    rc = 8 # Stop running this block  
                elif board[r][rc].colour != self.colour:
                    moves.append((r, rc))
                    Rbeyond = True
            elif rc <= 7 and Rbeyond:
                if board[r][rc] == 0:
                    temp.append((r, rc))
                elif board[r][rc].colour != self.colour:
                    temp.append((r, rc))
                    rc = 8
                    Rbeyond = False
                elif board[r][rc].colour == self.colour and board[r+1][rc-1] != 0 and board[r+1][rc-1].king:
                    temp2.append((r, rc))
                    rc = 8
                    Rbeyond = False

        r = self.row
        lc = self.col # left column
        rc = self.col # right column
        Lbeyond = False
        Rbeyond = False

        # Diagonal Down
        while r < 7:
            r += 1

            lc -= 1
            if lc >= 0 and not Lbeyond:
                if board[r][lc] == 0:
                    moves.append((r, lc))
                elif board[r][lc].colour == self.colour:
                    temp.append((r, lc))
                    temp2.append((r, lc))
                    lc = -1 # Stop running this block
                elif board[r][lc].colour != self.colour:
                    moves.append((r, lc))
                    Lbeyond = True
            elif lc >= 0 and Lbeyond:
                if board[r][lc] == 0:
                    temp.append((r, lc))
                elif board[r][lc].colour != self.colour:
                    temp.append((r, lc))
                    lc = -1
                    Lbeyond = False
                elif board[r][lc].colour == self.colour and board[r-1][lc+1] != 0 and board[r-1][lc+1].king:
                    temp2.append((r, lc))
                    lc = -1
                    Lbeyond = False

            rc += 1
            if rc <= 7 and not Rbeyond:
                if board[r][rc] == 0:
                    moves.append((r, rc))
                elif board[r][rc].colour == self.colour:
                    temp.append((r, rc))
                    temp2.append((r, rc))
                    rc = 8 # Stop running this block
                elif board[r][rc].colour != self.colour:
                    moves.append((r, rc))
                    Rbeyond = True
            elif rc <= 7 and not  Rbeyond:
                if board[r][rc] == 0:
                    temp.append((r, rc))
                elif board[r][rc].colour != self.colour:
                    temp.append((r, rc))
                    rc = 8
                    Rbeyond = False
                elif board[r][rc].colour == self.colour and board[r-1][rc-1] != 0 and board[r-1][rc-1].king:
                    temp2.append((r, rc))
                    rc = 8
                    Rbeyond = False

class Rook(Piece):
    def __init__(self, row, col, colour):
        super().__init__(row, col, colour)
        self.rook = True
        self.img = pygame.transform.scale(pygame.image.load(os.path.join("imgs" , colour + "R.png")), (CELL_SIZE, CELL_SIZE))

    def valid_moves(self, board):

        moves = []
        temp = []
        temp2 = []
        
        self.move_straight(board ,moves, temp, temp2)

        temp3 = self.check_moves(moves)

        value, pos = self.cause_check(moves)
        
        if value:
            moves = pos 

        if (Piece.w_check and self.colour == 'w') or (Piece.b_check and self.colour == 'b'):
            self.move_list = temp3
        else:
            self.move_list = moves

        self.possible_move = temp
        self.saving_move = temp2
        

class Queen(Piece):
    def __init__(self, row, col, colour):
        super().__init__(row, col, colour)
        self.queen = True
        self.img = pygame.transform.scale(pygame.image.load(os.path.join("imgs" , colour + "Q.png")), (CELL_SIZE, CELL_SIZE))

    def valid_moves(self, board):
        moves = []
        temp = []
        temp2 = []
        
        self.move_straight(board, moves, temp, temp2)
        self.move_diagonal(board, moves, temp, temp2)
        
        temp3 = self.check_moves(moves)
                                
        value, pos = self.cause_check(moves)
        
        if value:
            moves = pos

        if (Piece.w_check and self.colour == 'w') or (Piece.b_check and self.colour == 'b'):
            self.move_list = temp3
        else:
            self.move_list = moves

        self.possible_move = temp
        self.saving_move = temp2

class King(Piece):
    def __init__(self, row, col, colour):
        super().__init__(row, col, colour)
        self.king = True
        self.castled = False
        self.specialmoves = []
        self.img = pygame.transform.scale(pygame.image.load(os.path.join("imgs" , colour + "K.png")), (CELL_SIZE, CELL_SIZE))

    def valid_moves(self, board, turn):
        r = self.row
        c = self.col 
        moves = []
        temp = []
        temp2 = []

        if r >= 1 and c >= 1 and (board[r-1][c-1] == 0 or board[r-1][c-1].colour != self.colour):
            if self.king_pos(r-1, c-1, board):
                moves.append((r-1, c-1))
            else:
                temp.append((r-1, c-1))
        

        if r >= 1 and (board[r-1][c] == 0 or board[r-1][c].colour != self.colour):
            if self.king_pos(r-1, c, board):
                moves.append((r-1, c))
            else:
                temp.append((r-1, c))

        if r >= 1 and c <= 6 and (board[r-1][c+1] == 0 or board[r-1][c+1].colour != self.colour):
            if self.king_pos(r-1, c+1, board):
                moves.append((r-1, c+1))
            else:
                temp.append((r-1, c+1))

        if c >= 1 and (board[r][c-1] == 0 or board[r][c-1].colour != self.colour):
            if self.king_pos(r, c-1, board):
                moves.append((r, c-1))
            else:
                temp.append((r, c-1))

        if c <= 6 and (board[r][c+1] == 0 or board[r][c+1].colour != self.colour):
            if self.king_pos(r, c+1, board):
                moves.append((r, c+1))
            else:
                temp.append((r, c+1))
            
        if r <= 6 and c >= 1 and (board[r+1][c-1] == 0 or board[r+1][c-1].colour != self.colour):
            if self.king_pos(r+1, c-1, board):
                moves.append((r+1, c-1))
            else:
                temp.append((r+1, c-1))
        
        if r <= 6 and (board[r+1][c] == 0 or board[r+1][c].colour != self.colour):
            if self.king_pos(r+1, c, board):
                moves.append((r+1, c))
            else:
                temp.append((r+1, c))
            
        if r <= 6 and c <= 6 and (board[r+1][c+1] == 0 or board[r+1][c+1].colour != self.colour):
            if self.king_pos(r+1, c+1, board):
                moves.append((r+1, c+1))
            else:
                temp.append((r+1, c+1))

        if not self.moved and not self.castled:
            if self.colour == 'w' and not Piece.w_check:
                for wp in Piece.white_pieces:
                    if wp.rook and not wp.moved:
                        if (wp.col == 7 and wp.row == 7):
                            for i in range(5, 7):
                                if board[wp.row][i] != 0:
                                    break
                            else:
                                for bp in Piece.black_pieces:
                                    if (self.row, 6) in bp.move_list or (self.row, 5) in bp.move_list:
                                        break
                                else:
                                    temp2.append((self.row, 6))
                        elif (wp.col == 0 and wp.row == 0):
                            for i in range(1, 3):
                                if board[wp.row][i] != 0:
                                    break
                            else:
                                for bp in Piece.black_pieces:
                                    if (self.row, 1) in bp.move_list or (self.row, 2) in bp.move_list:
                                        break
                                else:
                                    temp2.append((self.row, 1))
                        elif (wp.col == 0 and wp.row == 7):
                            for i in range(1, 4):
                                if board[wp.row][i] != 0:
                                    break
                            else:
                                for bp in Piece.black_pieces:
                                    if (self.row, 2) in bp.move_list or (self.row, 3) in bp.move_list:
                                        break
                                else:
                                    temp2.append((self.row, 2))
                        elif (wp.col == 7 and wp.row == 0):
                            for i in range(4, 7):
                                if board[wp.row][i] != 0:
                                    break
                            else:
                                for bp in Piece.black_pieces:
                                    if (self.row, 4) in bp.move_list or (self.row, 5) in bp.move_list:
                                        break
                                else:
                                    temp2.append((self.row, 5))

            elif self.colour == 'b' and not Piece.b_check:
                for bp in Piece.black_pieces:
                    if bp.rook and not bp.moved:
                        if (bp.col == 7 and bp.row == 0):
                            for i in range(5, 7):
                                if board[bp.row][i] != 0:
                                    break
                            else:
                                for wp in Piece.white_pieces:
                                    if (self.row, 6) in wp.move_list or (self.row, 5) in wp.move_list:
                                        break
                                else:
                                    temp2.append((self.row, 6))
                        elif (bp.col == 0 and bp.row == 7):
                            for i in range(1, 3):
                                if board[bp.row][i] != 0:
                                    break
                            else:
                                for wp in Piece.white_pieces:
                                    if (self.row, 1) in wp.move_list or (self.row, 2) in wp.move_list:
                                        break
                                else:
                                    temp2.append((self.row, 1))
                        elif (bp.col == 0 and bp.row == 0):
                            for i in range(1, 4):
                                if board[bp.row][i] != 0:
                                    break
                            else:
                                for wp in Piece.white_pieces:
                                    if (self.row, 2) in wp.move_list or (self.row, 3) in wp.move_list:
                                        break
                                else:
                                    temp2.append((self.row, 2))
                        elif (bp.col == 7 and bp.row == 7):
                            for i in range(4, 7):
                                if board[bp.row][i] != 0:
                                    break
                            else:
                                for wp in Piece.white_pieces:
                                    if (self.row, 4) in wp.move_list or (self.row, 5) in wp.move_list:
                                        break
                                else:
                                    temp2.append((self.row, 5))

        if self.colour == 'b':
            for wp in Piece.white_pieces:
                if (self.row, self.col) in wp.move_list or (wp.pawn and (self.row, self.col) in wp.specialmoves):
                    Piece.b_check = True
                    break
            else:
                Piece.b_check = False
        
            if Piece.b_check and moves == []:
                for bp in Piece.black_pieces:
                    if bp.move_list != []:
                        break
                else:
                    Piece.b_checkmate = True

            if not Piece.b_check and moves == [] and turn == self.colour:
                for bp in Piece.black_pieces:
                    if bp.move_list != []:
                        break
                else:
                    Piece.b_stalemate = True
        elif self.colour == 'w':
            for bp in Piece.black_pieces:
                if (self.row, self.col) in bp.move_list or (bp.pawn and (self.row, self.col) in bp.specialmoves):
                    Piece.w_check = True
                    break
            else:
                Piece.w_check = False
                
            if Piece.w_check and moves == []:
                for wp in Piece.white_pieces:
                    if wp.move_list != []:
                        break
                else:
                    Piece.w_checkmate = True
            
            if not Piece.w_check and moves == [] and turn == self.colour:
                for wp in Piece.white_pieces:
                    if wp.move_list != []:
                        break
                else:
                    Piece.w_stalemate = True

        self.move_list = moves
        self.possible_move = temp
        self.specialmoves = temp2

    def king_pos(self, r, c, board):
        if self.colour == 'w':
            for bp in Piece.black_pieces:
                if bp.king:
                    if r in range(bp.row-1, bp.row+2):
                        if c in range(bp.col-1, bp.col+2):
                            return False      
                if bp.pawn:
                    if (r, c) in ((bp.row+1, bp.col-1), (bp.row+1, bp.col+1)):
                        return False
                    if (r, c) == (bp.row+1, bp.col):
                        return True

                if (r, c) in bp.move_list:
                    return False
                
                pos = self.find_pos(bp, (r, c))
                if (self.row, self.col) in pos:
                    return False
        
                if Piece.w_check and (r, c) in bp.possible_move:
                    if self.row == bp.row:
                        incr = -1 if bp.col > self.col else 1
                        if (r, c) == (self.row, self.col+incr):
                            return False
                    elif self.col == bp.col:
                        incr = -1 if bp.row > self.row else 1
                        if (r, c) == (self.row+incr, self.col):
                            return False
                    elif abs(self.row - bp.row) == abs(self.col - bp.col):
                        c_incr = -1 if bp.col > self.col else 1
                        r_incr = -1 if bp.row > self.row else 1
                        if (r, c) == (self.row+r_incr, self.col+c_incr):
                            return False

                if (r, c) == (bp.row, bp.col):
                    for bp2 in Piece.black_pieces:
                        if (r, c) in bp2.saving_move:
                            return False
                
        if self.colour == 'b':
            for wp in Piece.white_pieces:
                if wp.king:
                    if r in range(wp.row-1, wp.row+2):
                        if c in range(wp.col-1, wp.col+2):
                            return False 
                if wp.pawn:
                    if (r, c) in ((wp.row-1, wp.col-1), (wp.row-1, wp.col+1)):
                        return False
                    if (r, c) == (wp.row-1, wp.col):
                        return True

                if (r, c) in wp.move_list:
                    return False

                pos = self.find_pos(wp, (r, c))
                if (self.row, self.col) in pos:
                    return False

                if Piece.b_check and (r, c) in wp.possible_move:
                    if self.row == wp.row:
                        incr = -1 if wp.col > self.col else 1
                        if (r, c) == (self.row, self.col+incr):
                            return False
                    elif self.col == wp.col:
                        incr = -1 if wp.row > self.row else 1
                        if (r, c) == (self.row+incr, self.col):
                            return False
                    elif abs(self.row - wp.row) == abs(self.col - wp.col):
                        c_incr = -1 if wp.col > self.col else 1
                        r_incr = -1 if wp.row > self.row else 1
                        if (r, c) == (self.row+r_incr, self.col+c_incr):
                            return False

                if (r, c) == (wp.row, wp.col):
                    for wp2 in Piece.white_pieces:
                        if (r, c) in wp2.saving_move:
                            return False
        return True

    def find_pos(self, one, other):
        moves = []
        row = other[0]
        col = other[1]
        
        if one.row == row and (one.rook or one.queen):
            incr = -1 if col > one.col else 1
            for i in range(col+incr, one.col, incr):
                moves.append((one.row, i))
        elif one.col == col and (one.rook and one.queen):
            incr = -1 if row > one.row else 1
            for i in range(row+incr, one.row, incr):
                moves.append((i, one.col))
        elif abs(one.row - row) == abs(one.col - col) and (one.bishop or one.queen):
            r = r_incr = -1 if row > one.row else 1
            c = c_incr = -1 if col > one.col else 1
            if col < one.col:
                for i in range(col+1, one.col):
                    moves.append((row+r_incr, col+c_incr))
                    r_incr += r
                    c_incr += c
            elif col > one.col:
                for i in range(one.col+1, col):
                    moves.append((row+r_incr, col+c_incr))
                    r_incr += r
                    c_incr += c
        return moves

        
class Knight(Piece):
    def __init__(self, row, col, colour):
        super().__init__(row, col, colour)
        self.knight = True
        self.img = pygame.transform.scale(pygame.image.load(os.path.join("imgs" , colour + "Kn.png")), (CELL_SIZE, CELL_SIZE))

    def valid_moves(self, board):
        r = self.row
        c = self.col
        moves = []
        temp = []

        # Up
        if r >= 2:
            if c >= 1 and (board[r-2][c-1] == 0 or board[r-2][c-1].colour != self.colour):
                moves.append((r-2, c-1))
            elif c >= 1 and (board[r-2][c-1] == 0 or board[r-2][c-1].colour == self.colour):
                temp.append((r-2, c-1))
        
            if c <= 6 and (board[r-2][c+1] == 0 or board[r-2][c+1].colour != self.colour):
                moves.append((r-2, c+1))
            elif c <= 6 and (board[r-2][c+1] == 0 or board[r-2][c+1].colour == self.colour):
                temp.append((r-2, c+1))
        
        # Down
        if r <= 5:
            if c >= 1 and (board[r+2][c-1] == 0 or board[r+2][c-1].colour != self.colour):
                moves.append((r+2, c-1))
            elif c >= 1 and (board[r+2][c-1] == 0 or board[r+2][c-1].colour == self.colour):
                temp.append((r+2, c-1))

            if c <= 6 and (board[r+2][c+1] == 0 or board[r+2][c+1].colour != self.colour):
                moves.append((r+2, c+1))
            elif c <= 6 and (board[r+2][c+1] == 0 or board[r+2][c+1].colour == self.colour):
                temp.append((r+2, c+1))

        # Left
        if c >= 2:
            if r >= 1 and (board[r-1][c-2] == 0 or board[r-1][c-2].colour != self.colour):
                moves.append((r-1, c-2))
            elif r >= 1 and (board[r-1][c-2] == 0 or board[r-1][c-2].colour == self.colour):
                temp.append((r-1, c-2))

            if r <= 6 and (board[r+1][c-2] == 0 or board[r+1][c-2].colour != self.colour):
                moves.append((r+1, c-2))
            elif r <= 6 and (board[r+1][c-2] == 0 or board[r+1][c-2].colour == self.colour):
                temp.append((r+1, c-2))

        # Right
        if c <= 5:
            if r >= 1 and (board[r-1][c+2] == 0 or board[r-1][c+2].colour != self.colour):
                moves.append((r-1, c+2))
            elif r >= 1 and (board[r-1][c+2] == 0 or board[r-1][c+2].colour == self.colour):
                temp.append((r-1, c+2))

            if r <= 6 and (board[r+1][c+2] == 0 or board[r+1][c+2].colour != self.colour):
                moves.append((r+1, c+2))
            elif r <= 6 and (board[r+1][c+2] == 0 or board[r+1][c+2].colour == self.colour):
                temp.append((r+1, c+2))

        temp3 = self.check_moves(moves)

        value, pos = self.cause_check(moves)
        
        if value:
            moves = pos

        if (Piece.w_check and self.colour == 'w') or (Piece.b_check and self.colour == 'b'):
            self.move_list = temp3
        else:
            self.move_list = moves

        self.possible_move = temp
        self.saving_move = self.possible_move

class Bishop(Piece):
    def __init__(self, row, col, colour):
        super().__init__(row, col, colour)
        self.bishop = True
        self.img = pygame.transform.scale(pygame.image.load(os.path.join("imgs" , colour + "B.png")), (CELL_SIZE, CELL_SIZE))

    def valid_moves(self, board):
        moves = []
        temp = []
        temp2 = []

        self.move_diagonal(board, moves, temp, temp2)

        temp3 = self.check_moves(moves)

        value, pos = self.cause_check(moves)
        
        if value:
            moves = pos

        if (Piece.w_check and self.colour == 'w') or (Piece.b_check and self.colour == 'b'):
            self.move_list = temp3
        else:
            self.move_list = moves


        self.possible_move = temp 
        self.saving_move = temp2

class Pawn(Piece):
    def __init__(self, row, col, colour):
        super().__init__(row, col, colour)
        self.pawn = True
        self.specialmoves = []
        self.enpassant = False
        self.img = pygame.transform.scale(pygame.image.load(os.path.join("imgs" , colour + "P.png")), (CELL_SIZE, CELL_SIZE))


    def valid_moves(self, board, colour):
        r = self.row
        c = self.col
        moves = []
        temp2 = []
        temp3 = []

        if self.colour == colour:
            if not self.moved:
                for i in range(1, 3):
                    if board[r-i][c] != 0:
                        break
                    moves.append((r-i, c))
                if c >= 1 and board[r-1][c-1] != 0 and board[r-1][c-1].colour != self.colour:
                    moves.append((r-1, c-1))
                if c<= 6 and board[r-1][c+1] != 0 and board[r-1][c+1].colour != self.colour:
                    moves.append((r-1, c+1))
                if c >= 1 and board[r-1][c-1] != 0 and board[r-1][c-1].colour == self.colour:
                    temp2.append((r-1, c-1))
                if c<= 6 and board[r-1][c+1] != 0 and board[r-1][c+1].colour == self.colour:
                    temp2.append((r-1, c+1))
                
            else:
                if r == 1:
                    if board[r-1][c] == 0:
                        temp3.append((r-1, c))
                    if c >= 1 and board[r-1][c-1] != 0 and board[r-1][c-1].colour != self.colour:
                        temp3.append((r-1, c-1))
                    if c<= 6 and board[r-1][c+1] != 0 and board[r-1][c+1].colour != self.colour:
                        temp3.append((r-1, c+1))
                    if c >= 1 and board[r-1][c-1] != 0 and board[r-1][c-1].colour == self.colour:
                        temp2.append((r-1, c-1))
                    if c<= 6 and board[r-1][c+1] != 0 and board[r-1][c+1].colour == self.colour:
                        temp2.append((r-1, c+1))
                else:
                    if r >= 1 and board[r-1][c] == 0:
                        moves.append((r-1, c))
                    if r >= 1 and c >= 1 and board[r-1][c-1] != 0 and board[r-1][c-1].colour != self.colour:
                        moves.append((r-1, c-1))
                    if r >= 1 and c<= 6 and board[r-1][c+1] != 0 and board[r-1][c+1].colour != self.colour:
                        moves.append((r-1, c+1))
                    if r >= 1 and c >= 1 and board[r-1][c-1] != 0 and board[r-1][c-1].colour == self.colour:
                        temp2.append((r-1, c-1))
                    if r >= 1 and c<= 6 and board[r-1][c+1] != 0 and board[r-1][c+1].colour == self.colour:
                        temp2.append((r-1, c+1))
                    for bp in Piece.black_pieces:
                        if bp.pawn and bp.row == self.row and abs(self.col - bp.col) == 1 and bp.enpassant:
                            temp3.append((self.row-1, bp.col))

        elif self.colour != colour:
            if not self.moved:
                for i in range(1, 3):
                    if board[r+i][c] != 0:
                        break
                    moves.append((r+i, c))
                if c >= 1 and board[r+1][c-1] != 0 and board[r+1][c-1].colour != self.colour:
                    moves.append((r+1, c-1))
                if c<= 6 and board[r+1][c+1] != 0 and board[r+1][c+1].colour != self.colour:
                    moves.append((r+1, c+1))
                if c >= 1 and board[r+1][c-1] != 0 and board[r+1][c-1].colour == self.colour:
                    temp2.append((r+1, c-1))
                if c<= 6 and board[r+1][c+1] != 0 and board[r+1][c+1].colour == self.colour:
                    temp2.append((r+1, c+1))
            else:
                if r == 6:
                    if board[r+1][c] == 0:
                        temp3.append((r+1, c))
                    if c >= 1 and board[r+1][c-1] != 0 and board[r+1][c-1].colour != self.colour:
                        temp3.append((r+1, c-1))
                    if c <= 6 and board[r+1][c+1] != 0 and board[r+1][c+1].colour != self.colour:
                        temp3.append((r+1, c+1))
                    if c >= 1 and board[r+1][c-1] != 0 and board[r+1][c-1].colour == self.colour:
                        temp2.append((r+1, c-1))
                    if c <= 6 and board[r+1][c+1] != 0 and board[r+1][c+1].colour == self.colour:
                        temp2.append((r+1, c+1))
                else:
                    if  r <= 6 and board[r+1][c] == 0:
                        moves.append((r+1, c))
                    if r <= 6 and c >= 1 and board[r+1][c-1] != 0 and board[r+1][c-1].colour != self.colour:
                        moves.append((r+1, c-1))
                    if r <= 6 and c<= 6 and board[r+1][c+1] != 0 and board[r+1][c+1].colour != self.colour:
                        moves.append((r+1, c+1))
                    if r <= 6 and c >= 1 and board[r+1][c-1] != 0 and board[r+1][c-1].colour == self.colour:
                        temp2.append((r+1, c-1))
                    if r <= 6 and c<= 6 and board[r+1][c+1] != 0 and board[r+1][c+1].colour == self.colour:
                        temp2.append((r+1, c+1))
                    for wp in Piece.white_pieces:
                        if wp.pawn  and wp.row == self.row and abs(self.col - wp.col) == 1 and wp.enpassant:
                            temp3.append((self.row+1, wp.col))
                    

        temp4 = self.check_moves(moves)

        value, pos = self.cause_check(moves)
        
        if value:
            moves = pos 
    
        if (Piece.w_check and self.colour == 'w') or (Piece.b_check and self.colour == 'b'):
            self.move_list = temp4
        else:
            self.move_list = moves

        self.saving_move = temp2
        self.specialmoves = temp3
