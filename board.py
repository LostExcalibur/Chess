# encoding=latin-1

import pygame.transform
from easygui import choicebox

from piece import *

BLACK = pygame.Color(0, 0, 0)
BROWN = pygame.Color(181, 136, 99)
WHITE = pygame.Color(255, 255, 255)
LAQUE = pygame.Color(240, 217, 181)
RED = pygame.Color(255, 0, 0)


class Board:
    def __init__(self, width: int, height: int):
        pygame.init()
        self.caption = "Chess"
        self.size = (width, height)
        self.width = width
        self.height = height
        self.screen = pygame.display.set_mode(self.size)
        self.tilesize = int(min(width, height) / 8)
        self.board_surface = self.build_board()
        self.temp_board = self.board_surface.copy()
        self.running = True
        self.pieces: list[Piece] = []
        self.white_pieces = []
        self.black_pieces = []
        self.board = [[VIDE, VIDE, VIDE, VIDE, VIDE, VIDE, VIDE, VIDE],
                      [VIDE, VIDE, VIDE, VIDE, VIDE, VIDE, VIDE, VIDE],
                      [VIDE, VIDE, VIDE, VIDE, VIDE, VIDE, VIDE, VIDE],
                      [VIDE, VIDE, VIDE, VIDE, VIDE, VIDE, VIDE, VIDE],
                      [VIDE, VIDE, VIDE, VIDE, VIDE, VIDE, VIDE, VIDE],
                      [VIDE, VIDE, VIDE, VIDE, VIDE, VIDE, VIDE, VIDE],
                      [VIDE, VIDE, VIDE, VIDE, VIDE, VIDE, VIDE, VIDE],
                      [VIDE, VIDE, VIDE, VIDE, VIDE, VIDE, VIDE, VIDE]]
        self.beginning_FEN = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"
        self.testing_FEN = "r1bqkbnr/pppp1pp1/2n4p/4p3/2B1P3/5N2/PPPP1PPP/RNBQK2R w KQkq - 0 1"
        self.testing_FEN2 = "rnbqkbn1/pppPppp1/5p2/7r/4R3/6P1/PPPP1PP1/RNBQKBN1 w Qq - 0 1"
        self.pieces, self.gamestate = \
            self.parse_FEN(self.beginning_FEN)

    def build_board(self):
        board = pygame.Surface((self.tilesize * 8, self.tilesize * 8))
        board.fill(BROWN)
        for x in range(8):
            for y in range(8):
                if (x + y) % 2:
                    pygame.draw.rect(board, LAQUE, pygame.Rect(x * self.tilesize, y * self.tilesize,
                                                               self.tilesize, self.tilesize))
        board = pygame.transform.flip(board, True, False)
        return board

    def run(self):
        pygame.display.set_caption(self.caption)
        last_clicked = None
        legal_moves = None
        while self.running:
            # Boucle d'évènements
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == pygame.BUTTON_LEFT:
                    self.temp_board = self.board_surface.copy()
                    x, y = event.pos[0] // self.tilesize, event.pos[1] // self.tilesize
                    x: int
                    y: int
                    if last_clicked is not None and legal_moves:  # Le joueur avait cliqué sur une autre pièce avant
                        if (x, y) in legal_moves:  # et essaie de la déplacer
                            current_x, current_y = last_clicked.current_square
                            if (tobetaken := self.board[y][x]) != VIDE:
                                self.pieces.remove(tobetaken)
                            self.board[y][x] = last_clicked
                            last_clicked.current_square = (x, y)
                            self.board[current_y][current_x] = VIDE

                            # On met à jour l'état du jeu :
                            # - On passe au joueur suivant
                            self.gamestate ^= (1 << 6)
                            # - On détecte les échecs :
                            if self.gamestate >> 6:
                                if self.is_in_check(self.black_king.current_square, NOIR):
                                    if self.is_checkmate(NOIR):
                                        self.running = False
                                        print("Les blancs gagnent par échec et mat")
                                    else:
                                        self.gamestate |= 1 << 5
                            else:
                                if self.is_in_check(self.white_king.current_square, BLANC):
                                    if self.is_checkmate(BLANC):
                                        self.running = False
                                        print("Les noirs gagnent par échec et mat")
                                    else:
                                        self.gamestate |= 1 << 4

                            # Promotion de pion :
                            if type(last_clicked) == Pawn:
                                if (last_clicked.color == BLANC and y == 0) or (last_clicked.color == NOIR and y == 7):
                                    new_piece = choicebox("What do you want to promote to ?",
                                                          choices=["Queen", "Rook", "Bishop", "Knight"])
                                    if new_piece is None:  # Le joueur a cliqué "Cancel", donc par défaut on fait une dame
                                        promoted = Queen(last_clicked.color, (x, y), self.tilesize)
                                    else:
                                        promoted = Piece.new_piece(last_clicked.color, PIECES[new_piece], (x, y),
                                                                   self.tilesize)
                                    self.pieces.remove(last_clicked)
                                    self.pieces.append(promoted)
                                    if promoted.color == BLANC:
                                        self.white_pieces.remove(last_clicked)
                                        self.white_pieces.append(promoted)
                                    else:
                                        self.black_pieces.remove(last_clicked)
                                        self.black_pieces.append(promoted)
                                    self.board[y][x] = promoted
                            last_clicked = None
                            legal_moves = None
                            continue

                        else:
                            if (x, y) != last_clicked.current_square:
                                last_clicked = legal_moves = None

                    selected_piece: Piece = self.board[y][x]
                    # gamestate >> 6 correspond au joueur actuel, 1 = noir
                    if selected_piece != VIDE and selected_piece.color == (self.gamestate >> 6):
                        if selected_piece == last_clicked:
                            self.temp_board = self.board_surface.copy()
                            last_clicked = legal_moves = None
                            continue
                        pseudolegal_moves = selected_piece.generate_all_moves(self.board)
                        if type(selected_piece) == King:
                            # On enleve les cases où le roi est en échec
                            legal_moves = list(
                                filter(lambda position: (not self.is_in_check(position, selected_piece.color)),
                                       pseudolegal_moves))
                        else:
                            legal_moves = self.generate_legal_moves(selected_piece, pseudolegal_moves)
                        if legal_moves:
                            self.color_squares(legal_moves)
                        last_clicked = selected_piece

            # Affichage
            self.screen.blit(self.temp_board, self.temp_board.get_rect())
            for piece in self.pieces:
                self.screen.blit(piece.image,
                                 (piece.current_square[0] * self.tilesize,
                                  piece.current_square[1] * self.tilesize))
            pygame.display.update()

    def parse_FEN(self, fen: str) -> tuple[list[Piece], int]:
        pieces = []
        # De gauche à droite :
        # A qui de jouer : 1 noirs, 0 blancs
        # Echecs ? Noirs puis blancs
        # Roque coté reine puis roi, noirs puis blancs
        gamestate = 0b0001111

        split = fen.split(" ")
        lines = split[0].split("/")

        y = 0
        while y < 8:  # Vertical
            x = 0
            line: str = lines[y]
            if line.isnumeric():  # Il y a que des entiers, donc seulement un 8 cad ligne vide
                y += 1
                continue
            for char in line:  # Horizontal
                if char.isnumeric():
                    x += int(char)
                    continue
                piece = Piece.new_piece(int(char.islower()), PIECES[char.upper()], (x, y), self.tilesize)
                if type(piece) == King:
                    if piece.color == NOIR:
                        self.black_king = piece
                    else:
                        self.white_king = piece
                self.board[y][x] = piece
                pieces.append(piece)
                if char.islower():
                    self.black_pieces.append(piece)
                else:
                    self.white_pieces.append(piece)
                x += 1
            y += 1

        # A qui de jouer :
        if split[1] == 'w':  # Blancs
            gamestate &= 0b0111111
        elif split[1] == 'b':  # Noirs
            gamestate |= 0b1000000
        else:
            raise ValueError(f"Invalid fen :\n{fen}")

        # Roque
        if split[2] == '-':  # Personne peut roquer
            gamestate &= 0b1110000
        else:
            if "Q" in split[2]:
                gamestate |= 0b0000010
            if "K" in split[2]:
                gamestate |= 0b0000001
            if "q" in split[2]:
                gamestate |= 0b0001000
            if "k" in split[2]:
                gamestate |= 0b0000100

        # Le reste c'est en passant et le nombre de coup, pour l'instant ça m'intéresse pas

        return pieces, gamestate

    def color_squares(self, squares):
        for x, y in squares:
            pygame.draw.rect(self.temp_board, RED,
                             pygame.Rect(x * self.tilesize, y * self.tilesize, self.tilesize, self.tilesize))

    def is_in_check(self, position: tuple[int, int], color: int) -> bool:
        x, y = position
        current = self.board[y][x]
        self.board[y][x] = Potential(color, position)
        pieces = self.white_pieces.copy() if color == NOIR else self.black_pieces.copy()
        if current in pieces:
            pieces.remove(current)
        in_check = []
        for piece in pieces:
            in_check.extend(piece.generate_moves_for_piece(piece.color, piece.current_square, self.board, True))
        self.board[y][x] = current
        pieces.append(current)
        return position in in_check

    def is_checkmate(self, color: int) -> bool:
        # On suppose que le roi est déja en échec
        king = self.black_king if color == NOIR else self.white_king
        king_moves = list(
                filter(lambda position: (not self.is_in_check(position, color)), king.generate_all_moves(self.board)))
        if king_moves:
            return False
        pieces = self.white_pieces if color == BLANC else self.black_pieces
        for piece in pieces:
            if self.generate_legal_moves(piece, piece.generate_all_moves(self.board)):
                return False
        return True

    def generate_legal_moves(self, piece: Piece, pseudolegal_moves: list[tuple[int, int]]) -> list[tuple[int, int]]:
        legal = []
        king = self.black_king if piece.color == NOIR else self.white_king
        pieces = self.white_pieces.copy() if piece.color == NOIR else self.black_pieces.copy()
        self.board[piece.current_square[1]][piece.current_square[0]] = VIDE
        for position in pseudolegal_moves:
            x, y = position
            x: int
            y: int
            current = self.board[y][x]
            self.board[y][x] = Potential(piece.color, position)
            if current in pieces:
                pieces.remove(current)
            if not self.is_in_check(king.current_square, piece.color):
                legal.append(position)
            self.board[y][x] = current
            pieces.append(current)
        self.board[piece.current_square[1]][piece.current_square[0]] = piece
        return legal
