# v6.25
import tkinter as tk
import time
import  moviepy.editor
import pygame as pg
pg.init()
class Position:
    def __init__(self, row, col):
        self.row = row
        self.col = col
    def match(self, list_pos):
        for pos in list_pos:
            if self.col == pos.col and self.row == pos.row:
                return True
        return False
    def __eq__(self, other):
        if self.row == other.row and self.col == other.col:
            return True
        return False
class Piece:
    def __init__(self, color, board, image, position=None):
        self.image = image
        self.color = color
        self.board = board
        self.has_moved = False
        self.position = position
    def possible_moves(self):
        pass
    def move(self, end_pos):
        if end_pos.match(self.possible_moves()[0]):
            return 'valid move'
        return 'invalid move'
    def __eq__(self, other):
        return True if self.position == other.position else False
class King(Piece):
    def __init__(self, color, board, image, position=None):
        super().__init__(color, board, image, position)
        self.piece_type = "king"
        self.home_back=0
        self.castling=False
    def possible_moves(self):
        moves = []
        offsets = [(1, 0), (0, 1), (-1, 0), (0, -1),
                   (1, 1), (-1, 1), (1, -1), (-1, -1)]
        for dr, dc in offsets:
            new_pos = Position(self.position.row + dr, self.position.col + dc)
            if self.board.is_inside_board(new_pos) and (
                    self.board.is_square_empty(new_pos) or self.board.is_enemy_piece(new_pos, self.color)):
                moves.append(new_pos)
        # Castling
        if not self.board.board[self.position.row][self.position.col].has_moved:
            # Check kingside castling
            if self.board.board[self.position.row][7] and not self.board.board[self.position.row][7].has_moved:
                if all(self.board.is_square_empty(Position(self.position.row, c)) for c in
                       range(self.position.col + 1, 7)):
                    moves.append(Position(self.position.row, self.position.col + 2))
            # Check queenside castling
            if self.board.board[self.position.row][0] and not self.board.board[self.position.row][0].has_moved:
                if all(self.board.is_square_empty(Position(self.position.row, c)) for c in range(1, self.position.col)):
                    moves.append(Position(self.position.row, self.position.col - 2))
        for item in moves:
            if self.board.board[item.row][item.col]:
                if self.board.board[item.row][item.col].piece_type == "king":
                    moves.remove(item)
        return moves, [], moves
class Bishop(Piece):
    def __init__(self, color, board, image, position=None):
        super().__init__(color, board, image, position)
        self.piece_type = "bishop"
    def possible_moves(self):
        ne_moves = []
        sw_moves = []
        nw_moves = []
        se_moves = []
        moves = []
        seccond_moves = []
        move = Position(self.position.row + 1, self.position.col + 1)
        while self.board.is_inside_board(move):
            if self.board.is_square_empty(move):
                moves.append(move)
                ne_moves.append(move)
            elif self.board.is_enemy_piece(move, self.color):
                moves.append(move)
                ne_moves.append(move)
                if self.board.board[move.row][move.col].piece_type == "king":
                    ne_moves.append(Position(move.row + 1, move.col + 1))
                break
            else:
                ne_moves.append(move)
                break
            move = Position(move.row + 1, move.col + 1)
        move = Position(self.position.row + 1, self.position.col - 1)
        while self.board.is_inside_board(move):
            if self.board.is_square_empty(move):
                moves.append(move)
                nw_moves.append(move)
            elif self.board.is_enemy_piece(move, self.color):
                moves.append(move)
                nw_moves.append(move)
                if self.board.board[move.row][move.col].piece_type == "king":
                    nw_moves.append(Position(move.row + 1, move.col - 1))
                break
            else:
                nw_moves.append(move)
                break
            move = Position(move.row + 1, move.col - 1)
        move = Position(self.position.row - 1, self.position.col + 1)
        while self.board.is_inside_board(move):
            if self.board.is_square_empty(move):
                moves.append(move)
                se_moves.append(move)
            elif self.board.is_enemy_piece(move, self.color):
                moves.append(move)
                se_moves.append(move)
                if self.board.board[move.row][move.col].piece_type == "king":
                    se_moves.append(Position(move.row - 1, move.col + 1))
                break
            else:
                se_moves.append(move)
                break
            move = Position(move.row - 1, move.col + 1)
        move = Position(self.position.row - 1, self.position.col - 1)
        while self.board.is_inside_board(move):
            if self.board.is_square_empty(move):
                moves.append(move)
                sw_moves.append(move)
            elif self.board.is_enemy_piece(move, self.color):
                moves.append(move)
                sw_moves.append(move)
                if self.board.board[move.row][move.col].piece_type == "king":
                    sw_moves.append(Position(move.row - 1, move.col - 1))
                break
            else:
                sw_moves.append(move)
                break
            move = Position(move.row - 1, move.col - 1)
        seccond_moves.extend(sw_moves + se_moves + nw_moves + ne_moves)
        return moves, [sw_moves, se_moves, nw_moves, ne_moves] , seccond_moves
class Pawn(Piece):
    def __init__(self, color, board, image, position=None):
        super().__init__(color, board, image, position)
        self.piece_type = "pawn"
        self.special_move = False
    def possible_moves(self):
        moves = []
        seccond_moves = []
        direction = 1 if self.color == "White" else -1
        checking_row = 3 if self.color == "Black" else 4
        # Moves for regular pawn advance
        new_pos = Position(self.position.row + direction, self.position.col)
        if self.board.is_inside_board(new_pos) and self.board.is_square_empty(new_pos):
            moves.append(new_pos)
        if not self.has_moved:
            new_pos = Position(self.position.row + 2 * direction, self.position.col)
            if self.board.is_square_empty(new_pos) and self.board.is_square_empty(
                    Position(self.position.row + direction, self.position.col)):
                moves.append(new_pos)
        # Moves for capturing diagonally
        enemy = "Black" if self.color == "White" else "White"
        piece_1 = self.board.board[self.position.row + direction][self.position.col + direction] if self.board.is_inside_board(Position(self.position.row + direction, self.position.col + direction)) else None
        piece_2 = self.board.board[self.position.row + direction][self.position.col - direction] if self.board.is_inside_board(Position(self.position.row + direction, self.position.col - direction)) else None
        if piece_1 and piece_1.color == enemy:
            moves.append(Position(self.position.row + direction, self.position.col + direction))
        if piece_2 and piece_2.color == enemy:
            moves.append(Position(self.position.row + direction, self.position.col - direction))
        if self.board.is_inside_board(Position(self.position.row, self.position.col + 1)) and isinstance(self.board.board[self.position.row][self.position.col + 1], Pawn) and self.board.board[self.position.row][self.position.col + 1].color != self.color and self.board.board[self.position.row][self.position.col + 1].special_move and self.position.row == checking_row:
            moves.append(Position(self.position.row + direction, self.position.col + 1))
            seccond_moves.append(Position(self.position.row + direction, self.position.col + 1))
        if self.board.is_inside_board(Position(self.position.row, self.position.col - 1)) and isinstance(self.board.board[self.position.row][self.position.col - 1], Pawn) and self.board.board[self.position.row][self.position.col - 1].color != self.color and self.board.board[self.position.row][self.position.col - 1].special_move and self.position.row == checking_row:
            moves.append(Position(self.position.row + direction, self.position.col - 1))
            seccond_moves.append(Position(self.position.row + direction, self.position.col - 1))
        seccond_moves.append(Position(self.position.row + direction, self.position.col + direction))
        seccond_moves.append(Position(self.position.row + direction, self.position.col - direction))
        return moves, [] , seccond_moves
class Rook(Piece):
    def __init__(self, color, board, image, position=None):
        super().__init__(color, board, image, position)
        self.piece_type = "rook"
    def possible_moves(self):
        n_moves = []
        s_moves = []
        e_moves = []
        w_moves = []
        moves = []
        seccond_moves = []
        move = Position(self.position.row, self.position.col + 1)
        while self.board.is_inside_board(move):
            if self.board.is_square_empty(move):
                moves.append(move)
                s_moves.append(move)
            elif self.board.is_enemy_piece(move, self.color):
                moves.append(move)
                s_moves.append(move)
                if self.board.board[move.row][move.col].piece_type == "king":
                    s_moves.append(Position(move.row, move.col + 1))
                break
            else:
                s_moves.append(move)
                break
            move = Position(move.row, move.col + 1)
        move = Position(self.position.row, self.position.col - 1)
        while self.board.is_inside_board(move):
            if self.board.is_square_empty(move):
                moves.append(move)
                n_moves.append(move)
            elif self.board.is_enemy_piece(move, self.color):
                moves.append(move)
                n_moves.append(move)
                if self.board.board[move.row][move.col].piece_type == "king":
                    n_moves.append(Position(move.row, move.col - 1))
                break
            else:
                n_moves.append(move)
                break
            move = Position(move.row, move.col - 1)
        move = Position(self.position.row + 1, self.position.col)
        while self.board.is_inside_board(move):
            if self.board.is_square_empty(move):
                moves.append(move)
                e_moves.append(move)
            elif self.board.is_enemy_piece(move, self.color):
                moves.append(move)
                e_moves.append(move)
                if self.board.board[move.row][move.col].piece_type == "king":
                    e_moves.append(Position(move.row + 1, move.col))
                break
            else:
                e_moves.append(move)
                break
            move = Position(move.row + 1, move.col)
        move = Position(self.position.row - 1, self.position.col)
        while self.board.is_inside_board(move):
            if self.board.is_square_empty(move):
                moves.append(move)
                w_moves.append(move)
            elif self.board.is_enemy_piece(move, self.color):
                moves.append(move)
                w_moves.append(move)
                if self.board.board[move.row][move.col].piece_type == "king":
                    w_moves.append(Position(move.row - 1, move.col))
                break
            else:
                w_moves.append(move)
                break
            move = Position(move.row - 1, move.col)
        seccond_moves.extend(n_moves + s_moves + e_moves + w_moves)
        return moves, [n_moves, s_moves, e_moves, w_moves],seccond_moves
class Knight(Piece):
    def __init__(self, color, board, image, position=None):
        super().__init__(color, board, image, position)
        self.piece_type = "knight"
    def possible_moves(self):
        moves = []
        seccond_moves = []
        offsets = [(-2, -1), (-2, 1), (2, -1), (2, 1), (-1, -2), (-1, 2), (1, -2), (1, 2)]
        for dr, dc in offsets:
            new_pos = Position(self.position.row + dr, self.position.col + dc)
            if self.board.is_inside_board(new_pos) and (self.board.is_square_empty(new_pos) or self.board.is_enemy_piece(new_pos, self.color)):
                moves.append(new_pos)
                seccond_moves.append(new_pos)
            elif self.board.is_inside_board(new_pos):
                seccond_moves.append(new_pos)
        return moves, [] , seccond_moves
class Queen(Piece):
    def __init__(self, color, board, image, position=None):
        super().__init__(color, board, image, position)
        self.piece_type = "queen"
    def possible_moves(self):
        n_moves = []
        s_moves = []
        e_moves = []
        w_moves = []
        ne_moves = []
        nw_moves = []
        se_moves = []
        sw_moves = []
        moves = []
        seccond_moves = []
        # Rook_move
        move = Position(self.position.row, self.position.col + 1)
        while self.board.is_inside_board(move):
            if self.board.is_square_empty(move):
                moves.append(move)
                n_moves.append(move)
            elif self.board.is_enemy_piece(move, self.color):
                moves.append(move)
                n_moves.append(move)
                if self.board.board[move.row][move.col].piece_type == "king":
                    n_moves.append(Position(move.row, move.col + 1))
                break
            else:
                n_moves.append(move)
                break
            move = Position(move.row, move.col + 1)
        move = Position(self.position.row, self.position.col - 1)
        while self.board.is_inside_board(move):
            if self.board.is_square_empty(move):
                moves.append(move)
                s_moves.append(move)
            elif self.board.is_enemy_piece(move, self.color):
                moves.append(move)
                s_moves.append(move)
                if self.board.board[move.row][move.col].piece_type == "king":
                    s_moves.append(Position(move.row, move.col - 1))
                break
            else:
                s_moves.append(move)
                break
            move = Position(move.row, move.col - 1)
        move = Position(self.position.row + 1, self.position.col)
        while self.board.is_inside_board(move):
            if self.board.is_square_empty(move):
                moves.append(move)
                e_moves.append(move)
            elif self.board.is_enemy_piece(move, self.color):
                moves.append(move)
                e_moves.append(move)
                if self.board.board[move.row][move.col].piece_type == "king":
                    e_moves.append(Position(move.row + 1, move.col))
                break
            else:
                e_moves.append(move)
                break
            move = Position(move.row + 1, move.col)
        move = Position(self.position.row - 1, self.position.col)
        while self.board.is_inside_board(move):
            if self.board.is_square_empty(move):
                moves.append(move)
                w_moves.append(move)
            elif self.board.is_enemy_piece(move, self.color):
                moves.append(move)
                w_moves.append(move)
                if self.board.board[move.row][move.col].piece_type == "king":
                    w_moves.append(Position(move.row - 1, move.col))
                break
            else:
                w_moves.append(move)
                break
            move = Position(move.row - 1, move.col)
        # Bishop move
        move = Position(self.position.row + 1, self.position.col + 1)
        while self.board.is_inside_board(move):
            if self.board.is_square_empty(move):
                moves.append(move)
                ne_moves.append(move)
            elif self.board.is_enemy_piece(move, self.color):
                moves.append(move)
                ne_moves.append(move)
                if self.board.board[move.row][move.col].piece_type == "king":
                    ne_moves.append(Position(move.row + 1, move.col +1))
                break
            else:
                ne_moves.append(move)
                break
            move = Position(move.row + 1, move.col + 1)
        move = Position(self.position.row + 1, self.position.col - 1)
        while self.board.is_inside_board(move):
            if self.board.is_square_empty(move):
                moves.append(move)
                se_moves.append(move)
            elif self.board.is_enemy_piece(move, self.color):
                moves.append(move)
                se_moves.append(move)
                if self.board.board[move.row][move.col].piece_type == "king":
                    se_moves.append(Position(move.row + 1, move.col - 1))
                break
            else:
                se_moves.append(move)
                break
            move = Position(move.row + 1, move.col - 1)
        move = Position(self.position.row - 1, self.position.col + 1)
        while self.board.is_inside_board(move):
            if self.board.is_square_empty(move):
                moves.append(move)
                nw_moves.append(move)
            elif self.board.is_enemy_piece(move, self.color):
                moves.append(move)
                nw_moves.append(move)
                if self.board.board[move.row][move.col].piece_type == "king":
                    nw_moves.append(Position(move.row - 1, move.col + 1))
                break
            else:
                nw_moves.append(move)
                break
            move = Position(move.row - 1, move.col + 1)
        move = Position(self.position.row - 1, self.position.col - 1)
        while self.board.is_inside_board(move):
            if self.board.is_square_empty(move):
                moves.append(move)
                sw_moves.append(move)
            elif self.board.is_enemy_piece(move, self.color):
                moves.append(move)
                sw_moves.append(move)
                if self.board.board[move.row][move.col].piece_type == "king":
                    sw_moves.append(Position(move.row - 1, move.col - 1))
                break
            else:
                sw_moves.append(move)
                break
            move = Position(move.row - 1, move.col - 1)
        seccond_moves.extend(n_moves + s_moves + e_moves + w_moves + ne_moves + nw_moves + se_moves + sw_moves)
        return moves, [n_moves, s_moves, e_moves, w_moves, ne_moves, nw_moves, se_moves, sw_moves], seccond_moves
class Board:
    def __init__(self):
        self.board = [[None for _ in range(8)] for _ in range(8)]  # initialize the board
    def place_piece(self, piece, position):
        piece.position = position
        self.board[position.row][position.col] = piece
    def remove_piece(self, position):
        self.board[position.row][position.col] = None
    def move_piece_checker(self, start_pos, end_pos):
        piece = self.board[start_pos.row][start_pos.col]
        if piece:
            if piece.move(end_pos) == 'valid move':
                return True
            else:
                return False
        return False
    def move_piece(self, start_pos, end_pos):
        piece = self.board[start_pos.row][start_pos.col]
        self.remove_piece(start_pos)
        removed_piece=self.board[end_pos.row][end_pos.col]
        self.place_piece(piece, end_pos)
        piece.position = end_pos
        piece.has_moved = True
        return removed_piece
    def is_square_empty(self, position):
        return self.board[position.row][position.col] is None
    def is_enemy_piece(self, position, color):
        if self.board[position.row][position.col]:
            return self.board[position.row][position.col].color != color
        return False
    def is_inside_board(self, position):
        return 0 <= position.row <= 7 and 0 <= position.col <= 7
    def place_queen(self, position, color, root):
        def inner():
            root.destroy()
            self.place_piece(Queen(color, self, f"{color}_queen.png"), position)
        return inner
    def place_rook(self, position, color, root):
        def inner():
            self.place_piece(Rook(color, self, f"{color}_rook.png"), position)
            root.destroy()
        return inner
    def place_knight(self, position, color, root):
        def inner():
            self.place_piece(Knight(color, self, f"{color}_knight.png"), position)
            root.destroy()
        return inner
    def place_bishop(self, position, color, root):
        def inner():
            self.place_piece(Bishop(color, self, f"{color}_bishop.png"), position)
            root.destroy()
        return inner
    def change_pawn(self):
        for col in range(8):
            if isinstance(self.board[7][col], Pawn):
                self.remove_piece(Position(7, col))
                message_root = tk.Tk()
                message_root.geometry("400x400")
                message_root.config(bg="khaki")
                messag = tk.Label(text="What kind of peices do you want?", bg="khaki", font=("Comic Sans MS", 18),fg="#0000FF")
                messag.place(x=10, y=10)
                queen_button = tk.Button(bg="khaki", fg="#0000FF", text="Queen", font=("Comic Sans MS", 18), width=25,command=self.place_queen(Position(7, col), "White", message_root))
                queen_button.place(x=10, y=50)
                rook_button = tk.Button(bg="khaki", fg="#0000FF", text="Rook", font=("Comic Sans MS", 18), width=25,command=self.place_rook(Position(7, col), "White", message_root))
                rook_button.place(x=10, y=125)
                knight_button = tk.Button(bg="khaki", fg="#0000FF", text="Knight", font=("Comic Sans MS", 18), width=25,command=self.place_knight(Position(7, col), "White", message_root))
                knight_button.place(x=10, y=200)
                bishop_button = tk.Button(bg="khaki", fg="#0000FF", text="Bishop", font=("Comic Sans MS", 18), width=25,command=self.place_bishop(Position(7, col), "White", message_root))
                bishop_button.place(x=10, y=275)
                message_root.mainloop()
            elif isinstance(self.board[0][col], Pawn):
                self.remove_piece(Position(0, col))
                message_root = tk.Tk()
                message_root.geometry("400x400")
                message_root.config(bg="khaki")
                messag = tk.Label(text="What kind of peices do you want?", bg="khaki", font=("Comic Sans MS", 18),fg="#0000FF")
                messag.place(x=10, y=10)
                queen_button = tk.Button(bg="khaki", fg="#0000FF", text="Queen", font=("Comic Sans MS", 18), width=25,command=self.place_queen(Position(7, col), "Black", message_root))
                queen_button.place(x=10, y=50)
                rook_button = tk.Button(bg="khaki", fg="#0000FF", text="Rook", font=("Comic Sans MS", 18), width=25,command=self.place_rook(Position(7, col), "Black", message_root))
                rook_button.place(x=10, y=125)
                knight_button = tk.Button(bg="khaki", fg="#0000FF", text="Knight", font=("Comic Sans MS", 18), width=25,command=self.place_knight(Position(7, col), "Black", message_root))
                knight_button.place(x=10, y=200)
                bishop_button = tk.Button(bg="khaki", fg="#0000FF", text="Bishop", font=("Comic Sans MS", 18), width=25,command=self.place_bishop(Position(7, col), "Black", message_root))
                bishop_button.place(x=10, y=275)
                message_root.mainloop()
            pg.display.update()
        return False
class ChessSet:
    def __init__(self):
        self.board = Board()
        self.setup_board()
    def setup_board(self):
        # Place white pieces
        self.board.place_piece(Rook("White", self.board, 'white_rook.png'), Position(0, 0))
        self.board.place_piece(Rook("White", self.board, 'white_rook.png'), Position(0, 7))
        self.board.place_piece(Knight("White", self.board, 'white_knight.png'), Position(0, 1))
        self.board.place_piece(Knight("White", self.board, 'white_knight.png'), Position(0, 6))
        self.board.place_piece(Bishop("White", self.board, 'white_bishop.png'), Position(0, 2))
        self.board.place_piece(Bishop("White", self.board, 'white_bishop.png'), Position(0, 5))
        self.board.place_piece(King("White", self.board, 'white_king.png'), Position(0, 4))
        self.board.place_piece(Queen("White", self.board, 'white_queen.png'), Position(0, 3))
        for col in range(8):
            self.board.place_piece(Pawn("White", self.board, 'white_pawn.png'), Position(1, col))
        # Place black pieces
        self.board.place_piece(Rook("Black", self.board, 'black_rook.png'), Position(7, 0))
        self.board.place_piece(Rook("Black", self.board, 'black_rook.png'), Position(7, 7))
        self.board.place_piece(Knight("Black", self.board, 'black_knight.png'), Position(7, 1))
        self.board.place_piece(Knight("Black", self.board, 'black_knight.png'), Position(7, 6))
        self.board.place_piece(Bishop("Black", self.board, 'black_bishop.png'), Position(7, 2))
        self.board.place_piece(Bishop("Black", self.board, 'black_bishop.png'), Position(7, 5))
        self.board.place_piece(King("Black", self.board, 'black_king.png'), Position(7, 4))
        self.board.place_piece(Queen("Black", self.board, 'black_queen.png'), Position(7, 3))
        for col in range(8):
            self.board.place_piece(Pawn("Black", self.board, 'black_pawn.png'), Position(6, col))
class Chess:
    def __init__(self):
        self.chess_set = ChessSet()
    def start_game(self):
        current_player = "White"
        pg.init()
        display = pg.display.set_mode((640, 640))
        pg.display.set_caption('chess')
        first_massage = pg.image.load('welcome_page.png')
        display.blit(first_massage, (0, 0))
        pg.display.update()
        pg.mixer.music.load('war_horn_3.mp3')
        pg.mixer.music.play()
        time.sleep(2)
        display.blit(pg.image.load('optinos.png'), (0,0))
        pg.display.update()
        start_game = False
        while not start_game:
            for event in pg.event.get():
                if event.type == pg.KEYDOWN or event.type == pg.MOUSEBUTTONDOWN:
                    start_game = True
                if event.type == pg.QUIT:
                    pg.quit()
        if start_game:
            board = pg.image.load('board.png')
            display.blit(board, (0, 0))
            counter = 0
            start_pos = Position(0, 0)
            end_pos = Position(0, 0)
            stop_game = False
            check_message_flag = False
            old_move = []
            old_moves_saver=[]
            while not stop_game:
                if self.is_check(current_player)[0] and not check_message_flag:
                    pg.mixer.music.load('کیش.mp3')
                    pg.mixer.music.play()
                    check_message = pg.image.load(f'{current_player}_king_is_in_check.png')
                    display.blit(check_message, (0, 0))
                    pg.display.update()
                    time.sleep(2)
                    check_message_flag = True
                if counter != 1:
                    board = pg.image.load('board.png')
                    display.blit(board, (0, 0))
                    for row in range(8):
                        for col in range(8):
                            if self.chess_set.board.board[row][col]:
                                image = pg.image.load(self.chess_set.board.board[row][col].image)
                                display.blit(image, (col * 80, row * 80))
                    pg.display.update()
                for event in pg.event.get():
                    if event.type == pg.MOUSEBUTTONDOWN and counter % 2 == 0:
                        start_pos = Position(event.pos[1] // 80, event.pos[0] // 80)
                        piece = self.chess_set.board.board[start_pos.row][start_pos.col]
                        if piece and piece.color == current_player:
                            counter += 1
                    elif event.type == pg.MOUSEBUTTONDOWN and counter % 2 != 0:
                        end_pos = Position(event.pos[1] // 80, event.pos[0] // 80)
                        counter += 1
                    #Ctrl+z
                    elif event.type == pg.KEYDOWN:
                        if event.key == pg.K_z and pg.key.get_mods() & pg.KMOD_CTRL and len(old_moves_saver) and counter != 1:
                            check_message_flag = False
                            old_move=old_moves_saver[-1]
                            self.chess_set.board.place_piece(old_move[3],old_move[0])
                            self.chess_set.board.remove_piece(old_move[1])
                            current_player = "Black" if current_player == "White" else "White"
                            if old_move[2]:
                                self.chess_set.board.place_piece(old_move[2], old_move[2].position)
                            if self.chess_set.board.board[old_move[0].row][old_move[0].col].piece_type == "pawn":
                                first_row = 1 if current_player == "White" else 6
                                if old_move[0].row == first_row:
                                    self.chess_set.board.board[old_move[0].row][old_move[0].col].has_moved = False
                            elif self.chess_set.board.board[old_move[0].row][old_move[0].col].piece_type == "king":
                                first_pos = Position(0, 4) if current_player == "White" else Position(7, 4)
                                castling_pos = [Position(0, 2) if current_player == "White" else Position(7, 2),Position(0, 6) if current_player == "White" else Position(7, 6)]
                                if old_move[0] == first_pos and self.chess_set.board.board[old_move[0].row][old_move[0].col].home_back == 0:
                                    self.chess_set.board.board[old_move[0].row][old_move[0].col].has_moved = False
                                elif old_move[0] == first_pos:
                                    self.chess_set.board.board[old_move[0].row][old_move[0].col].home_back -= 1
                                    if self.chess_set.board.board[old_move[0].row][old_move[0].col].home_back == 0:
                                        self.chess_set.board.board[old_move[0].row][old_move[0].col].has_moved = False
                                if old_move[0] == first_pos and old_move[1] == castling_pos[0]:
                                    self.chess_set.board.remove_piece(Position(0, 3) if current_player == "White" else Position(7, 3))
                                    self.chess_set.board.place_piece(Rook(current_player, self.chess_set.board, f'{current_player}_rook.png'), Position(0, 0) if current_player == "White" else Position(7, 0))
                                if old_move[0] == first_pos and old_move[1] == castling_pos[1]:
                                    self.chess_set.board.remove_piece(Position(0, 5) if current_player == "White" else Position(7, 5))
                                    self.chess_set.board.place_piece(Rook(current_player, self.chess_set.board, f'{current_player}_rook.png'), Position(0, 7) if current_player == "White" else Position(7, 7))
                            old_moves_saver.pop(-1)
                            continue
                    elif event.type == pg.QUIT:
                        pg.quit()
                st_pos = start_pos
                en_pos = end_pos
                if counter == 1:
                    pg.draw.rect(display, (0,100,0), ((st_pos.col * 80, st_pos.row * 80), (80, 80)), 5)
                    checking_values = self.king_savers(current_player)
                    if isinstance(self.chess_set.board.board[st_pos.row][st_pos.col], King):
                        moves = self.chess_set.board.board[st_pos.row][st_pos.col].possible_moves()[0]
                    else:
                        for i in range(8):
                            if self.chess_set.board.board[st_pos.row][st_pos.col] in checking_values[1][i] and checking_values[0][i]:
                                moves = []
                                for pos in self.chess_set.board.board[st_pos.row][st_pos.col].possible_moves()[0]:
                                    if pos in checking_values[2][i]:
                                        moves.append(pos)
                                break
                            else:
                                moves = self.chess_set.board.board[st_pos.row][st_pos.col].possible_moves()[0]
                    '''for move in moves:
                        if self.is_check(current_player, move.row, move.col)[0] and self.chess_set.board.board[st_pos.row][st_pos.col].piece_type == "king":
                            moves.remove(move)'''
                    for i in range(len(moves)):
                        for move in moves:
                            king_position = self.king_finder(current_player)
                            if self.is_check(current_player, move.row, move.col)[0] == True and self.chess_set.board.board[st_pos.row][st_pos.col].piece_type == "king":
                                moves.remove(move)
                            elif self.chess_set.board.is_square_empty(move):
                                pg.draw.rect(display, (0, 0, 255), ((move.col * 80, move.row * 80), (80, 80)), 5)
                            elif self.chess_set.board.is_enemy_piece(move, current_player) and self.chess_set.board.board[move.row][move.col].piece_type != "king":
                                pg.draw.rect(display, (255, 0, 0), ((move.col * 80, move.row * 80), (80, 80)), 5)
                    pg.display.update()
                elif counter == 2:
                    if self.chess_set.board.board[st_pos.row][st_pos.col] and self.chess_set.board.board[st_pos.row][st_pos.col].piece_type == "pawn" and self.chess_set.board.move_piece_checker(st_pos, en_pos):
                        if st_pos.col-en_pos.col == 1 and self.chess_set.board.is_square_empty(en_pos):
                            removed_piece = self.chess_set.board.board[st_pos.row][st_pos.col - 1]
                            self.chess_set.board.remove_piece(Position(st_pos.row, st_pos.col - 1))
                            piecee = self.chess_set.board.board[st_pos.row][st_pos.col]
                            a = self.chess_set.board.move_piece(st_pos, en_pos)
                            if removed_piece:
                                pg.mixer.music.load('حذف مهره.mp3')
                                pg.mixer.music.play()
                            else:
                                pg.mixer.music.load('گذاشتن مهره.mp3')
                                pg.mixer.music.play()
                            current_player = "Black" if current_player == "White" else "White"
                            old_move = []
                            old_move.extend([start_pos, end_pos, removed_piece, piecee])
                            old_moves_saver.append(old_move)
                            start_pos = Position(0, 0)
                            end_pos = Position(0, 0)
                        elif en_pos.col-st_pos.col == 1 and self.chess_set.board.is_square_empty(en_pos):
                            removed_piece = self.chess_set.board.board[st_pos.row][st_pos.col + 1]
                            self.chess_set.board.remove_piece(Position(st_pos.row, st_pos.col + 1))
                            piecee = self.chess_set.board.board[st_pos.row][st_pos.col]
                            a = self.chess_set.board.move_piece(st_pos, en_pos)
                            if removed_piece:
                                pg.mixer.music.load('حذف مهره.mp3')
                                pg.mixer.music.play()
                            else:
                                pg.mixer.music.load('گذاشتن مهره.mp3')
                                pg.mixer.music.play()
                            current_player = "Black" if current_player == "White" else "White"
                            old_move = []
                            old_move.extend([start_pos, end_pos, removed_piece, piecee])
                            old_moves_saver.append(old_move)
                            start_pos = Position(0, 0)
                            end_pos = Position(0, 0)
                        for row in range(1,7):
                            for col in range(8):
                                if isinstance(self.chess_set.board.board[row][col], Pawn) and self.chess_set.board.board[row][col].special_move:
                                    self.chess_set.board.board[row][col].special_move = False
                        if current_player == "White" and st_pos.row == 1 and en_pos.row == 3:
                            if en_pos.col + 1 < 8 and isinstance(self.chess_set.board.board[en_pos.row][en_pos.col + 1],Pawn) and self.chess_set.board.board[en_pos.row][en_pos.col + 1].color == "Black":
                                self.chess_set.board.board[st_pos.row][st_pos.col].special_move = True
                            if en_pos.col - 1 > -1 and isinstance(self.chess_set.board.board[en_pos.row][en_pos.col - 1],Pawn) and self.chess_set.board.board[en_pos.row][en_pos.col - 1].color == "Black":
                                self.chess_set.board.board[st_pos.row][st_pos.col].special_move = True
                        elif current_player == "Black" and st_pos.row == 6 and en_pos.row == 4:
                            if en_pos.col + 1 <8 and isinstance(self.chess_set.board.board[en_pos.row][en_pos.col + 1], Pawn) and self.chess_set.board.board[en_pos.row][en_pos.col + 1].color == "White":
                                self.chess_set.board.board[st_pos.row][st_pos.col].special_move = True
                            if en_pos.col - 1 > -1 and isinstance(self.chess_set.board.board[en_pos.row][en_pos.col - 1], Pawn) and self.chess_set.board.board[en_pos.row][en_pos.col - 1].color == "White":
                                self.chess_set.board.board[st_pos.row][st_pos.col].special_move = True
                    if self.chess_set.board.board[en_pos.row][en_pos.col] and self.chess_set.board.board[en_pos.row][en_pos.col].piece_type == "king" and self.chess_set.board.board[en_pos.row][en_pos.col].color != current_player:
                        start_pos = Position(0, 0)
                        end_pos = Position(0, 0)
                        counter = 0
                        continue
                    if self.chess_set.board.board[start_pos.row][start_pos.col]:
                        if not self.is_check(current_player)[0]:
                            if isinstance(self.chess_set.board.board[st_pos.row][st_pos.col], King) and self.is_check(current_player, en_pos.row, en_pos.col)[0]:
                                start_pos = Position(0, 0)
                                end_pos = Position(0, 0)
                                counter = 0
                                continue
                            if self.chess_set.board.board[start_pos.row][start_pos.col].color == current_player and self.chess_set.board.move_piece_checker(st_pos, en_pos) and en_pos in moves:
                                home_king = Position(0, 4) if current_player == "White" else Position(7, 4)
                                if self.chess_set.board.board[start_pos.row][start_pos.col].piece_type == "king" and en_pos == home_king:
                                    self.chess_set.board.board[start_pos.row][start_pos.col].home_back += 1
                                castling_pos = [Position(0, 2) if current_player == "White" else Position(7, 2),Position(0, 6) if current_player == "White" else Position(7, 6)]
                                if en_pos == castling_pos[0] and isinstance(self.chess_set.board.board[st_pos.row][st_pos.col], King) and self.chess_set.board.board[st_pos.row][st_pos.col].has_moved == False:
                                    self.chess_set.board.board[st_pos.row][st_pos.col].castling = True
                                    self.chess_set.board.remove_piece(Position(0, 0) if current_player == "White" else Position(7, 0))
                                    self.chess_set.board.place_piece(Rook(current_player, self.chess_set.board, f'{current_player}_rook.png'),Position(0, 3) if current_player == "White" else Position(7, 3))
                                elif en_pos == castling_pos[1] and isinstance(self.chess_set.board.board[st_pos.row][st_pos.col], King) and self.chess_set.board.board[st_pos.row][st_pos.col].has_moved == False:
                                    self.chess_set.board.board[st_pos.row][st_pos.col].castling = True
                                    self.chess_set.board.remove_piece(Position(0, 7) if current_player == "White" else Position(7, 7))
                                    self.chess_set.board.place_piece(Rook(current_player, self.chess_set.board, f'{current_player}_rook.png'),Position(0, 5) if current_player == "White" else Position(7, 5))
                                piecee=self.chess_set.board.board[st_pos.row][st_pos.col]
                                a=self.chess_set.board.move_piece(st_pos,en_pos)
                                if a:
                                    pg.mixer.music.load('حذف مهره.mp3')
                                    pg.mixer.music.play()
                                else:
                                    pg.mixer.music.load('گذاشتن مهره.mp3')
                                    pg.mixer.music.play()
                                current_player = "Black" if current_player == "White" else "White"
                                old_move = []
                                old_move.extend([start_pos, end_pos,a,piecee])
                                old_moves_saver.append(old_move)
                        elif self.is_check(current_player)[0] and self.is_checkmate(current_player)[0] == False:
                            if end_pos in self.is_checkmate(current_player)[1]:
                                if self.is_check(current_player, en_pos.row, en_pos.col)[0] and self.chess_set.board.board[st_pos.row][st_pos.col].piece_type == "king":
                                    check_message = pg.image.load(f'{current_player}_king_is_in_check.png')
                                    display.blit(check_message, (0, 0))
                                    pg.display.update()
                                    time.sleep(2)
                                    start_pos = Position(0, 0)
                                    end_pos = Position(0, 0)
                                    counter = 0
                                    continue
                                else:
                                    for piece in self.is_check(current_player)[1]:
                                        if (en_pos in piece.possible_moves()[0] or en_pos == piece.position) and not isinstance(self.chess_set.board.board[st_pos.row][st_pos.col], King) and self.chess_set.board.move_piece_checker(st_pos, en_pos) and en_pos in moves:
                                            piecee = self.chess_set.board.board[st_pos.row][st_pos.col]
                                            a=self.chess_set.board.move_piece(st_pos,en_pos)
                                            check_message_flag = False
                                            if a:
                                                pg.mixer.music.load('حذف مهره.mp3')
                                                pg.mixer.music.play()
                                            else:
                                                pg.mixer.music.load('گذاشتن مهره.mp3')
                                                pg.mixer.music.play()
                                            old_move = []
                                            old_move.extend([start_pos, end_pos,a,piecee])
                                            old_moves_saver.append(old_move)
                                            current_player = "Black" if current_player == "White" else "White"
                                            check_message_flag = False
                                        elif en_pos not in piece.possible_moves()[0] and not isinstance(self.chess_set.board.board[st_pos.row][st_pos.col], King):
                                            check_message = pg.image.load(f'{current_player}_king_is_in_check.png')
                                            display.blit(check_message, (0, 0))
                                            pg.display.update()
                                            time.sleep(2)
                                        elif isinstance(self.chess_set.board.board[st_pos.row][st_pos.col], King) and self.chess_set.board.move_piece_checker(st_pos, en_pos) and en_pos in moves:
                                            castling_pos = [Position(0, 2) if current_player == "White" else Position(7, 2),Position(0, 6) if current_player == "White" else Position(7, 6)]
                                            if en_pos == castling_pos[0] and self.chess_set.board.board[st_pos.row][st_pos.col].has_moved == False:
                                                self.chess_set.board.board[st_pos.row][st_pos.col].castling = True
                                                self.chess_set.board.remove_piece(Position(0, 0) if current_player == "White" else Position(7, 0))
                                                self.chess_set.board.place_piece(Rook(current_player, self.chess_set.board, f'{current_player}_rook.png'), Position(0, 4) if current_player == "White" else Position(7, 4))
                                            elif en_pos == castling_pos[1] and isinstance(self.chess_set.board.board[st_pos.row][st_pos.col], King) and self.chess_set.board.board[st_pos.row][st_pos.col].has_moved == False:
                                                self.chess_set.board.board[st_pos.row][st_pos.col].castling = True
                                                self.chess_set.board.remove_piece(Position(0, 7) if current_player == "White" else Position(7, 7))
                                                self.chess_set.board.place_piece(Rook(current_player, self.chess_set.board,f'{current_player}_rook.png'),Position(0,5) if current_player == "White" else Position(7, 5))
                                            piecee = self.chess_set.board.board[st_pos.row][st_pos.col]
                                            a=self.chess_set.board.move_piece(st_pos,en_pos)
                                            check_message_flag = False
                                            if a:
                                                pg.mixer.music.load('حذف مهره.mp3')
                                                pg.mixer.music.play()
                                            else:
                                                pg.mixer.music.load('گذاشتن مهره.mp3')
                                                pg.mixer.music.play()
                                            old_move = []
                                            old_move.extend([start_pos, end_pos,a,piecee])
                                            old_moves_saver.append(old_move)
                                            current_player = "Black" if current_player == "White" else "White"
                                            check_message_flag = False
                            else:
                                check_message = pg.image.load(f'{current_player}_king_is_in_check.png')
                                display.blit(check_message, (0, 0))
                                pg.display.update()
                                time.sleep(2)
                        counter = 0
                self.chess_set.board.change_pawn()
                if self.is_checkmate(current_player)[0]:
                    board = pg.image.load('board.png')
                    display.blit(board, (0, 0))
                    for row in range(8):
                        for col in range(8):
                            if self.chess_set.board.board[row][col]:
                                image = pg.image.load(self.chess_set.board.board[row][col].image)
                                display.blit(image, (col * 80, row * 80))
                    display.blit(pg.image.load('check_block.png'),
                                 (self.king_finder(current_player).col * 80, self.king_finder(current_player).row * 80))
                    pg.mixer.music.load('مات.mp3')
                    pg.mixer.music.play()
                    pg.display.update()
                    time.sleep(2)
                    pg.display.set_caption('checkmate')
                    clip = moviepy.editor.VideoFileClip('checkmate.mp4')
                    clip.preview()
                    pg.quit()
                    display = pg.display.set_mode((640, 640))
                    pg.display.set_caption('Game Over!')
                    last_message = pg.image.load(f'{current_player}_lost.png')
                    display.blit(last_message, (0, 0))
                    pg.display.update()
                    time.sleep(2)
                    pg.quit()
                    root = tk.Tk()
                    root.title('Play agian?')
                    root.eval('tk::PlaceWindow . center')
                    root.geometry('500x100')
                    message = tk.Label(root, text='Game Over!Do you want to play again?', font = ("Comic Sans MS", 18))
                    message.place(x=30, y=0)
                    no_button = tk.Button(root, text='No', font = ("Comic Sans MS", 18),command=root.destroy)
                    no_button.place(x=100, y=50 )
                    yes_button = tk.Button(root, text='Yes', font = ("Comic Sans MS", 18), command=play_again(root))
                    yes_button.place(x=300, y=50)
                    root.mainloop()
                    break
    def king_finder(self, current_player):
        for row in range(8):
            flag = False
            for col in range(8):
                if isinstance(self.chess_set.board.board[row][col], King):
                    if self.chess_set.board.board[row][col].color == current_player:
                        flag = True
                        king_row = row
                        king_col = col
                        break
                if flag:
                    break
        return Position(king_row, king_col)
    def king_savers(self, current_player):
        needs = [False] * 8
        n_teammates = []
        s_teammates = []
        e_teammates = []
        w_teammates = []
        ne_teammates = []
        nw_teammates = []
        se_teammates = []
        sw_teammates = []
        n_teammates_moves = []
        s_teammates_moves = []
        e_teammates_moves = []
        w_teammates_moves = []
        ne_teammates_moves = []
        nw_teammates_moves = []
        se_teammates_moves = []
        sw_teammates_moves = []
        king_position = self.king_finder(current_player)
        move = Position(king_position.row, king_position.col + 1)
        while self.chess_set.board.is_inside_board(move):
            if self.chess_set.board.is_square_empty(move) or self.chess_set.board.is_enemy_piece(move, current_player):
                n_teammates_moves.append(move)
            if self.chess_set.board.is_enemy_piece(move, current_player):
                if self.chess_set.board.board[move.row][move.col].piece_type in ["queen", "rook"]:
                    needs[0] = True
                break
            elif not self.chess_set.board.is_square_empty(move) and not self.chess_set.board.is_enemy_piece(move, current_player):
                n_teammates.append(self.chess_set.board.board[move.row][move.col])
            move = Position(move.row, move.col + 1)
        move = Position(king_position.row, king_position.col - 1)
        while self.chess_set.board.is_inside_board(move):
            if self.chess_set.board.is_square_empty(move) or self.chess_set.board.is_enemy_piece(move, current_player):
                s_teammates_moves.append(move)
            if self.chess_set.board.is_enemy_piece(move, current_player):
                if self.chess_set.board.board[move.row][move.col].piece_type in ["queen", "rook"]:
                    needs[1] = True
                break
            elif not self.chess_set.board.is_square_empty(move) and not self.chess_set.board.is_enemy_piece(move, current_player):
                s_teammates.append(self.chess_set.board.board[move.row][move.col])
            move = Position(move.row, move.col - 1)
        move = Position(king_position.row + 1, king_position.col)
        while self.chess_set.board.is_inside_board(move):
            if self.chess_set.board.is_square_empty(move) or self.chess_set.board.is_enemy_piece(move, current_player):
                e_teammates_moves.append(move)
            if self.chess_set.board.is_enemy_piece(move, current_player):
                if self.chess_set.board.board[move.row][move.col].piece_type in ["queen", "rook"]:
                    needs[2] = True
                break
            elif self.chess_set.board.is_square_empty(move) == False and self.chess_set.board.is_enemy_piece(move, current_player) == False:
                e_teammates.append(self.chess_set.board.board[move.row][move.col])
            move = Position(move.row + 1, move.col)
        move = Position(king_position.row - 1, king_position.col)
        while self.chess_set.board.is_inside_board(move):
            if self.chess_set.board.is_square_empty(move) or self.chess_set.board.is_enemy_piece(move, current_player):
                w_teammates_moves.append(move)
            if self.chess_set.board.is_enemy_piece(move, current_player):
                if self.chess_set.board.board[move.row][move.col].piece_type in ["queen", "rook"]:
                    needs[3] = True
                break
            elif not self.chess_set.board.is_square_empty(move) and not self.chess_set.board.is_enemy_piece(move, current_player):
                w_teammates.append(self.chess_set.board.board[move.row][move.col])
            move = Position(move.row - 1, move.col)
        # Bishop move
        move = Position(king_position.row + 1, king_position.col + 1)
        while self.chess_set.board.is_inside_board(move):
            if self.chess_set.board.is_square_empty(move) or self.chess_set.board.is_enemy_piece(move, current_player):
                ne_teammates_moves.append(move)
            if self.chess_set.board.is_enemy_piece(move, current_player):
                if self.chess_set.board.board[move.row][move.col].piece_type in ["queen", "bishop"]:
                    needs[4] = True
                break
            elif not self.chess_set.board.is_square_empty(move) and not self.chess_set.board.is_enemy_piece(move, current_player):
                ne_teammates.append(self.chess_set.board.board[move.row][move.col])
            move = Position(move.row + 1, move.col + 1)
        move = Position(king_position.row + 1, king_position.col - 1)
        while self.chess_set.board.is_inside_board(move):
            if self.chess_set.board.is_square_empty(move) or self.chess_set.board.is_enemy_piece(move, current_player):
                se_teammates_moves.append(move)
            if self.chess_set.board.is_enemy_piece(move, current_player):
                if self.chess_set.board.board[move.row][move.col].piece_type in ["queen", "bishop"]:
                    needs[5] = True
                break
            elif not self.chess_set.board.is_square_empty(move) and not self.chess_set.board.is_enemy_piece(move, current_player):
                se_teammates.append(self.chess_set.board.board[move.row][move.col])
            move = Position(move.row + 1, move.col - 1)
        move = Position(king_position.row - 1, king_position.col + 1)
        while self.chess_set.board.is_inside_board(move):
            if self.chess_set.board.is_square_empty(move) or self.chess_set.board.is_enemy_piece(move, current_player):
                nw_teammates_moves.append(move)
            if self.chess_set.board.is_enemy_piece(move, current_player):
                if self.chess_set.board.board[move.row][move.col].piece_type in ["queen", "bishop"]:
                    needs[6] = True
                break
            elif not self.chess_set.board.is_square_empty(move) and not self.chess_set.board.is_enemy_piece(move, current_player):
                nw_teammates.append(self.chess_set.board.board[move.row][move.col])
            move = Position(move.row - 1, move.col + 1)
        move = Position(king_position.row - 1, king_position.col - 1)
        while self.chess_set.board.is_inside_board(move):
            if self.chess_set.board.is_square_empty(move) or self.chess_set.board.is_enemy_piece(move, current_player):
                sw_teammates_moves.append(move)
            if self.chess_set.board.is_enemy_piece(move, current_player):
                if self.chess_set.board.board[move.row][move.col].piece_type in ["queen", "bishop"]:
                    needs[7] = True
                break
            elif not self.chess_set.board.is_square_empty(move) and not self.chess_set.board.is_enemy_piece(move, current_player):
                sw_teammates.append(self.chess_set.board.board[move.row][move.col])
            move = Position(move.row - 1, move.col - 1)
        if len(n_teammates) > 1:
            needs[0] = False
        if len(s_teammates) > 1:
            needs[1] = False
        if len(e_teammates) > 1:
            needs[2] = False
        if len(w_teammates) > 1:
            needs[3] = False
        if len(ne_teammates) > 1:
            needs[4] = False
        if len(se_teammates) > 1:
            needs[5] = False
        if len(nw_teammates) > 1:
            needs[6] = False
        if len(sw_teammates) > 1:
            needs[7] = False
        return needs, [n_teammates, s_teammates, e_teammates, w_teammates, ne_teammates, se_teammates, nw_teammates, sw_teammates], [n_teammates_moves, s_teammates_moves, e_teammates_moves, w_teammates_moves, ne_teammates_moves, se_teammates_moves, nw_teammates_moves, sw_teammates_moves]
    def is_check(self, current_player, row=None, col=None):
        if row!=None and col!=None:
            king_position = Position(row, col)
        else:
            king_position = self.king_finder(current_player)
        def pre_check(piece):
            if piece and king_position in piece.possible_moves()[2] and piece.color != current_player :
                return True
            return False
        one_board = [self.chess_set.board.board[row][col] for row in range(8) for col in range(8)]
        checked_pieces = list(filter(pre_check,one_board))
        if len(checked_pieces)>0:
            return True, checked_pieces
        return False, checked_pieces
    def is_checkmate(self, current_player):
        row, col = self.king_finder(current_player).row, self.king_finder(current_player).col
        saved_king = []
        if self.is_check(current_player)[0]:
            for move in self.chess_set.board.board[row][col].possible_moves()[2]:
                if not self.is_check(current_player, move.row, move.col)[0]:
                    saved_king.append(move)
            for piece in self.is_check(current_player)[1]:
                one_board = [self.chess_set.board.board[row][col] for row in range(8) for col in range(8)]
                saved_king_pieces = (list(filter(lambda piecee : piecee and piecee.color == current_player and piece.position in piecee.possible_moves()[0], one_board)))
                for item in saved_king_pieces:
                    if item.piece_type == "king" and self.is_check(current_player, piece.position.row, piece.position.col):
                        saved_king_pieces.remove(item)
                        break
                if len(saved_king_pieces) > 0 :
                    saved_king.append(piece.position)
                for moves in piece.possible_moves()[1]:
                    if self.king_finder(current_player) in moves:
                        for row in range(8):
                            for col in range(8):
                                if self.chess_set.board.board[row][col] and self.chess_set.board.board[row][col].color == current_player and self.chess_set.board.board[row][col].piece_type != "king":
                                    for item in self.chess_set.board.board[row][col].possible_moves()[0]:
                                        if item in moves and (self.king_finder(current_player).row<item.row<piece.position.row or self.king_finder(current_player).col<item.col<piece.position.col):
                                            saved_king.append(item)
            if len(saved_king) > 0:
                return False, saved_king
            return True, saved_king
        return False, []
def play_again(root):
    def inner():
        root.destroy()
        new_game = Chess()
        new_game.start_game()
    return inner
if __name__ == "__main__":
    game=Chess()
    game.start_game()