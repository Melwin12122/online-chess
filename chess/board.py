import pygame
from .constants import ROWS, COLS, CELL_SIZE, BLACK, WHITE, BROWN, RED, YELLOW, BLUE, PURPLE
from .piece import Rook, King, Queen, Bishop, Pawn, Knight, Piece
from tkinter import Tk, Label, Button

class Board:
    
    def __init__(self, colour):
        self.board = [[0 for _ in range(COLS)] for _ in range(ROWS)]
        self.selected = []
        self.turn = 'w'
        Piece.newGame = True

        opp_c = 'b' if colour == 'w' else 'w'
        self.c = colour

        self.board[0][0] = Rook(0, 0, opp_c)
        self.board[0][1] = Knight(0, 1, opp_c)
        self.board[0][2] = Bishop(0, 2, opp_c)
        if self.c == 'w':
            self.board[0][3] = Queen(0, 3, opp_c)
            self.board[0][4] = King(0, 4, opp_c)
        else:
            self.board[0][3] = King(0, 3, opp_c)
            self.board[0][4] = Queen(0, 4, opp_c)

        self.board[0][5] = Bishop(0, 5, opp_c)
        self.board[0][6] = Knight(0, 6, opp_c)
        self.board[0][7] = Rook(0, 7, opp_c)

        self.board[1][0] = Pawn(1, 0, opp_c)
        self.board[1][1] = Pawn(1, 1, opp_c)
        self.board[1][2] = Pawn(1, 2, opp_c)
        self.board[1][3] = Pawn(1, 3, opp_c)
        self.board[1][4] = Pawn(1, 4, opp_c)
        self.board[1][5] = Pawn(1, 5, opp_c)
        self.board[1][6] = Pawn(1, 6, opp_c)
        self.board[1][7] = Pawn(1, 7, opp_c)

        self.board[7][0] = Rook(7, 0, colour)
        self.board[7][1] = Knight(7, 1, colour)
        self.board[7][2] = Bishop(7, 2, colour)
        if self.c == 'w':
            self.board[7][3] = Queen(7, 3, colour)
            self.board[7][4] = King(7, 4, colour)
        else:
            self.board[7][3] = King(7, 3, colour)
            self.board[7][4] = Queen(7, 4, colour)
        self.board[7][5] = Bishop(7, 5, colour)
        self.board[7][6] = Knight(7, 6, colour)
        self.board[7][7] = Rook(7, 7, colour)

        self.board[6][0] = Pawn(6, 0, colour)
        self.board[6][1] = Pawn(6, 1, colour)
        self.board[6][2] = Pawn(6, 2, colour)
        self.board[6][3] = Pawn(6, 3, colour)
        self.board[6][4] = Pawn(6, 4, colour)
        self.board[6][5] = Pawn(6, 5, colour)
        self.board[6][6] = Pawn(6, 6, colour)
        self.board[6][7] = Pawn(6, 7, colour)
        self.pawn_promo = None


    def draw(self, win, r1, c1, r2, c2):
        win.fill(BROWN)
        for row in range(ROWS):
            for col in range(row % 2, COLS, 2):
                pygame.draw.rect(win, WHITE, (CELL_SIZE * col, CELL_SIZE * row, CELL_SIZE, CELL_SIZE))

        if r1 is not None:        
            pygame.draw.rect(win, (0, 255, 0), (CELL_SIZE * c1, CELL_SIZE * r1, CELL_SIZE, CELL_SIZE))
            pygame.draw.rect(win, (35, 77, 37), (CELL_SIZE * c2, CELL_SIZE * r2, CELL_SIZE, CELL_SIZE))

        if self.selected != []:
            pygame.draw.rect(win, YELLOW, (CELL_SIZE * self.selected[0][1], CELL_SIZE * self.selected[0][0], CELL_SIZE, CELL_SIZE))

        if len(self.selected) == 1:
            row = self.selected[0][0]
            col = self.selected[0][1]
            for r, c in self.board[row][col].move_list:
                pygame.draw.rect(win, YELLOW, (CELL_SIZE * c, CELL_SIZE * r, CELL_SIZE, CELL_SIZE))
                if self.board[r][c] != 0: # Opposition piece
                    pygame.draw.rect(win, RED, (CELL_SIZE * c, CELL_SIZE * r, CELL_SIZE, CELL_SIZE))
            if self.board[row][col].king or self.board[row][col].pawn:
                for r, c in self.board[row][col].specialmoves:
                    pygame.draw.rect(win, PURPLE, (CELL_SIZE * c, CELL_SIZE * r, CELL_SIZE, CELL_SIZE))

        for row in range(ROWS):
            for col in range(COLS):
                if self.board[row][col] != 0:
                    if self.board[row][col].king:
                        if self.board[row][col].colour == 'b' and self.board[row][col].b_check:
                            pygame.draw.rect(win, BLUE, (CELL_SIZE * col, CELL_SIZE * row, CELL_SIZE, CELL_SIZE))
                            if self.board[row][col].b_checkmate:
                                self.checkmate("White")
                                return 'cm'
                        elif self.board[row][col].colour == 'w' and self.board[row][col].w_check:
                            pygame.draw.rect(win, BLUE, (CELL_SIZE * col, CELL_SIZE * row, CELL_SIZE, CELL_SIZE))
                            if self.board[row][col].w_checkmate:
                                self.checkmate("Black")
                                return 'cm'
                        if self.board[row][col].colour == 'b':
                            if self.board[row][col].b_stalemate:
                                self.stalemate()
                                return 'sm'
                        elif self.board[row][col].colour == 'w':
                            if self.board[row][col].w_stalemate:
                                self.stalemate()
                                return 'sm'
                    self.board[row][col].draw(win)
                    if self.board[row][col].king:
                        self.board[row][col].valid_moves(self.board, self.turn)
                    elif self.board[row][col].pawn:
                        self.board[row][col].valid_moves(self.board, self.c)
                    else:
                        self.board[row][col].valid_moves(self.board)
                pygame.draw.rect(win, BLACK, (CELL_SIZE * col, CELL_SIZE * row, CELL_SIZE, CELL_SIZE), 2) # border
                    
    
    def checkmate(self, winner):
        root = Tk()

        Label(text="CHECKMATE").grid(row=0, column=0)
        Label(text=f"{winner} wins!").grid(row=1, column=0)

        root.mainloop()

    def stalemate(self):
        root = Tk()

        Label(text="STALEMATE").grid(row=0, column=0)
        Label(text="DRAW!").grid(row=1, column=0)

        root.mainloop()
    

    def select(self, row, col, pop=True):
        # UNSELECT and same team selection
        pos = list()
        if self.board[row][col] != 0 or self.selected != []:
            if self.selected == [] and self.occupied(row, col):
                if (self.turn == 'w' and self.board[row][col].colour == 'w') or (self.turn == 'b' and self.board[row][col].colour == 'b'):
                    self.selected.append((row, col))
            elif len(self.selected) == 1 and (row, col) == self.selected[0]:
                self.selected = []
            elif len(self.selected) == 1 and self.board[row][col] != 0 and self.turn == self.board[row][col].colour:
                self.selected = list()
                self.selected.append((row, col))
            elif len(self.selected) == 1 and (row, col) in self.board[self.selected[0][0]][self.selected[0][1]].move_list:
                self.selected.append((row, col))
                r1, c1 = self.selected[0][0], self.selected[0][1]
                r2, c2 = self.selected[1][0], self.selected[1][1]
                self.change_pos(r1, c1, r2, c2)
                pos = self.selected[:]
                self.selected = []
            elif len(self.selected) == 1 and self.board[self.selected[0][0]][self.selected[0][1]].king:
                r = self.selected[0][0]
                c = self.selected[0][1]
                self.board[r][c].valid_moves(self.board, self.turn)
                if (row, col) in self.board[r][c].specialmoves:      
                    self.board[row][col] = self.board[r][c]  
                    self.board[row][col].col = col
                    self.board[row][col].castled = True
                    self.board[row][col].moved = True
                    self.board[r][c] = 0 
                    print(r, c, row, col)
                    if col > c:
                        print(r, c, row, col)
                        if self.board[row][col+1] != 0 and self.board[row][col+1].rook:
                            self.board[row][col-1] = self.board[row][col+1]
                            self.board[row][col+1] = 0
                        elif self.board[row][col+2] != 0 and self.board[row][col+2].rook:
                            self.board[row][col-1] = self.board[row][col+2]
                            self.board[row][col+2] = 0
                        self.board[row][col-1].col = col - 1
                        self.board[row][col-1].moved = True
                    elif col < c:
                        if self.board[row][col-1] != 0 and self.board[row][col-1].rook:
                            self.board[row][col+1] = self.board[row][col-1]
                            self.board[row][col-1] = 0
                        elif self.board[row][col-2] != 0 and self.board[row][col-2].rook:
                            self.board[row][col+1] = self.board[row][col-2]
                            self.board[row][col-2] = 0
                        self.board[row][col+1].col = col + 1
                        self.board[row][col+1].moved = True
                    self.turn = 'w' if self.turn == 'b' else 'b'
                    self.selected.append((row, col))
                    pos = self.selected[:]
                    self.selected = []
            elif len(self.selected) == 1 and self.board[self.selected[0][0]][self.selected[0][1]].pawn:
                r = self.selected[0][0]
                c = self.selected[0][1]
                if (row, col) in self.board[r][c].specialmoves and (r == 1 or r == 6):
                    self.selected.append((row, col))
                    print(self.board[r][c].specialmoves)
                    self.board[r][c].row = self.board[r][c].col = None
                    if pop:
                        self.popup()
                    if self.board[row][col] != 0:
                        self.board[row][col].row = self.board[row][col].col = None
                        if self.board[row][col].colour == 'b':
                            self.board[r][c].black_pieces.remove(self.board[row][col])
                        elif self.board[row][col].colour == 'w':
                            self.board[r][c].white_pieces.remove(self.board[row][col])
                    if self.board[r][c].colour == 'w':
                        self.board[r][c].white_pieces.remove(self.board[r][c])
                        self.board[r][c] = 0
                        if self.pawn_promo == 'queen' or self.pawn_promo is None:
                            self.board[row][col] = Queen(row, col, 'w')
                        elif self.pawn_promo == 'rook':
                            self.board[row][col] = Rook(row, col, 'w')
                        elif self.pawn_promo == 'knight':
                            self.board[row][col] = Knight(row, col, 'w')
                        elif self.pawn_promo == 'bishop':
                            self.board[row][col] = Bishop(row, col, 'w')
                        self.turn = 'w' if self.turn == 'b' else 'b'
                        pos = self.selected[:]
                        self.selected = []
                    elif self.board[r][c].colour == 'b':
                        self.board[r][c].black_pieces.remove(self.board[r][c])
                        self.board[r][c] = 0
                        if self.pawn_promo == 'queen' or self.pawn_promo is None:
                            self.board[row][col] = Queen(row, col, 'b')
                        elif self.pawn_promo == 'rook':
                            self.board[row][col] = Rook(row, col, 'b')
                        elif self.pawn_promo == 'knight':
                            self.board[row][col] = Knight(row, col, 'b')
                        elif self.pawn_promo == 'bishop':
                            self.board[row][col] = Bishop(row, col, 'b')
                        self.turn = 'w' if self.turn == 'b' else 'b'
                        pos = self.selected[:]
                        self.selected = []
                elif (row, col) in self.board[r][c].specialmoves:
                    self.selected.append((row, col))
                    if self.board[r][c].colour == 'b':
                        self.board[row-1][col].row = self.board[row-1][col].col = None
                        self.board[row-1][col].white_pieces.remove(self.board[row-1][col])
                        self.board[row-1][col] = 0
                    elif self.board[r][c].colour == 'w':
                        self.board[row+1][col].row = self.board[row+1][col].col = None
                        self.board[row+1][col].black_pieces.remove(self.board[row+1][col])
                        self.board[row+1][col] = 0
                    self.board[row][col] = self.board[r][c]
                    self.board[r][c] = 0
                    self.board[row][col].row = row
                    self.board[row][col].col = col 
                    self.turn = 'w' if self.turn == 'b' else 'b'
                    pos = self.selected[:]
                    self.selected = [] 
            elif len(self.selected) == 1 and not self.occupied(row, col):
                pass

    
        return pos
          
    def occupied(self, row, col):
        if self.board[row][col] != 0:
            return True
        return False

    def change_pos(self, r1, c1, r2, c2):
        if self.board[r2][c2] != 0:
            self.board[r2][c2].move_list = list()
            self.board[r2][c2].possible_move = list()
            self.board[r2][c2].row = None
            self.board[r2][c2].col = None

        self.board[r1][c1].row = r2
        self.board[r1][c1].col = c2

        if self.board[r2][c2] != 0:
            if self.board[r2][c2].colour == 'w':
                self.board[r2][c2].white_pieces.remove(self.board[r2][c2])
            elif self.board[r2][c2].colour == 'b':
                self.board[r2][c2].black_pieces.remove(self.board[r2][c2])        
                    
        self.board[r2][c2] = self.board[r1][c1]
        self.board[r1][c1] = 0
        self.board[r2][c2].moved = True
        self.turn = 'w' if self.turn == 'b' else 'b'

        if self.board[r2][c2].pawn:
            if abs(r2 - r1) == 2:
                self.board[r2][c2].enpassant = True
    

        for bp in self.board[r2][c2].black_pieces:
            if bp.pawn and bp is not self.board[r2][c2]:
                bp.enpassant = False

        for wp in self.board[r2][c2].white_pieces:
            if wp.pawn and wp is not self.board[r2][c2]:
                wp.enpassant = False


    def popup(self):
        root = Tk()

        root.overrideredirect(True)

        Label(root, text="Choose one!").grid(row=0, column=0, columnspan=2)
        Button(root, text="QUEEN", padx=50, pady=30, command=lambda: self.click("queen", root)).grid(row=1, column=0)
        Button(root, text="ROOK", padx=50, pady=30, command=lambda: self.click("rook", root)).grid(row=1, column=1)
        Button(root, text="KNIGHT", padx=50, pady=30, command=lambda: self.click("knight", root)).grid(row=2, column=0)
        Button(root, text="BISHOP", padx=50, pady=30, command=lambda: self.click("bishop", root)).grid(row=2, column=1)

        root.mainloop()
    
    def click(self, str1, root):
        root.destroy()
        self.pawn_promo = str1