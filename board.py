# encoding=latin-1

import pygame.transform
from easygui import choicebox

from piece import *


BROWN = pygame.Color(181, 136, 99)
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
        self.white_pieces: list[Piece] = []
        self.black_pieces: list[Piece] = []
        self.en_passant_square = None
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

    def build_board(self) -> pygame.Surface:
        """
        Construit la surface qui contient les sprites des cases, que l'on stocke dans une variable
        plut�t que de la g�n�rer � chaque frame, ce qui serait vraiment pas efficace

        :return: La surface de l'�chiquier
        """
        board = pygame.Surface((self.tilesize * 8, self.tilesize * 8))
        board.fill(BROWN)
        for x in range(8):
            for y in range(8):
                if (x + y) % 2:
                    pygame.draw.rect(board, LAQUE, pygame.Rect(x * self.tilesize, y * self.tilesize,
                                                               self.tilesize, self.tilesize))
        # Il faut la retourner selon les x, car pygame a son axe vertical (y) vers le bas
        board = pygame.transform.flip(board, True, False)
        return board

    def run(self) -> None:
        """
        La boucle principale du plateau.
        """
        pygame.display.set_caption(self.caption)
        icon = pygame.image.load(path.join("resources", "chess.jpg"))
        pygame.display.set_icon(pygame.transform.scale(icon, (32, 32)))
        last_clicked = None
        legal_moves = None
        while self.running:
            # Boucle d'�v�nements
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        self.print_board()
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == pygame.BUTTON_LEFT:
                    self.temp_board = self.board_surface.copy()
                    x, y = event.pos[0] // self.tilesize, event.pos[1] // self.tilesize
                    x: int
                    y: int
                    if last_clicked is not None and legal_moves:  # Le joueur avait cliqu� sur une autre pi�ce avant
                        if (x, y) in legal_moves:  # et essaie de la d�placer
                            self.temp_board = self.board_surface.copy()  # On nettoie la surface du plateau
                            current_x, current_y = last_clicked.current_square
                            tobetaken = self.board[y][x]
                            # On va prendre en-passant
                            if (x, y) == self.en_passant_square and type(last_clicked) == Pawn:
                                tobetaken = self.board[y - 1][x] if (self.gamestate >> 6) else self.board[y + 1][x]

                            if tobetaken != VIDE:
                                self.pieces.remove(tobetaken)
                                (self.black_pieces if tobetaken.color == NOIR else self.white_pieces).remove(tobetaken)
                            self.board[y][x] = last_clicked
                            last_clicked.current_square = (x, y)
                            self.board[current_y][current_x] = VIDE

                            self.en_passant_square = None
                            if type(last_clicked) == Pawn and (y == current_y + 2 or y == current_y - 2):
                                self.en_passant_square = (x, y - 1) if last_clicked.color == NOIR else (x, y + 1)

                            # On met � jour l'�tat du jeu :
                            # - On passe au joueur suivant
                            self.gamestate ^= (1 << 6)
                            # - On d�tecte les �checs :
                            if self.gamestate >> 6:
                                # Les noirs vont jouer, donc on v�rifie que les blancs ont gagn� ou pas au tour qu'ils viennent de jouer
                                if self.is_in_check(self.black_king.current_square, NOIR, self.white_pieces):
                                    if self.is_checkmate(NOIR):
                                        self.running = False
                                        print("Les blancs gagnent par �chec et mat")
                                    else:
                                        self.gamestate |= 1 << 5
                                # Les blancs viennent de jouer, donc ils ne sont forc�ment plus en �chec
                                # sinon il y aurait eu mat au coup pr�c�dent
                                self.gamestate &= 0b1101111

                            else:
                                if self.is_in_check(self.white_king.current_square, BLANC, self.black_pieces):
                                    self.color_squares([self.white_king.current_square])
                                    if self.is_checkmate(BLANC):
                                        self.running = False
                                        print("Les noirs gagnent par �chec et mat")
                                    else:
                                        self.gamestate |= 1 << 4
                                self.gamestate &= 0b1011111

                            # Promotion de pion :
                            if type(last_clicked) == Pawn:
                                if (last_clicked.color == BLANC and y == 0) or (last_clicked.color == NOIR and y == 7):
                                    new_piece = choicebox("What do you want to promote to ?",
                                                          choices=["Queen", "Rook", "Bishop", "Knight"])
                                    if new_piece is None:  # Le joueur a cliqu� "Cancel", donc par d�faut on fait une dame
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
                        if isinstance(selected_piece, Pawn) and self.en_passant_square:
                            selected_piece: Pawn
                            selected_piece.en_passant_target = self.en_passant_square
                        pseudolegal_moves = selected_piece.generate_all_moves(self.board)
                        if isinstance(selected_piece, King):
                            # On enleve les cases o� le roi est en �chec
                            ennemy_pieces = self.white_pieces.copy() if selected_piece.color == NOIR else self.black_pieces.copy()
                            legal_moves = list(
                                filter(lambda position: (not self.is_in_check(position, selected_piece.color, ennemy_pieces)),
                                       pseudolegal_moves))
                        else:
                            legal_moves = self.generate_legal_moves(selected_piece, pseudolegal_moves)
                        if legal_moves:
                            self.color_squares(legal_moves)
                        last_clicked = selected_piece

            # Affichage
            if self.gamestate & (1 << 5):
                self.color_squares([self.black_king.current_square])
            elif self.gamestate & (1 << 4):
                self.color_squares([self.white_king.current_square])
            self.screen.blit(self.temp_board, self.temp_board.get_rect())
            for piece in self.pieces:
                self.screen.blit(piece.image,
                                 (piece.current_square[0] * self.tilesize,
                                  piece.current_square[1] * self.tilesize))
            pygame.display.update()

    def parse_FEN(self, fen: str) -> tuple[list[Piece], int]:
        """
        Construit les pi�ces comme d�crit dans le FEN pass�, et l'�tat actuel de la partie (roque, en-passant, nombre de coups)

        :param fen: La position sous forme de FEN
        :return: Le tuple contenant la liste des pi�ces et l'�tat de la partie
        """
        pieces = []
        # De gauche � droite :
        # A qui de jouer : 1 noirs, 0 blancs
        # Echecs ? Noirs puis blancs
        # Roque cot� reine puis roi, noirs puis blancs
        gamestate = 0b0001111

        # Un FEN a la structure suivante :
        # pieces/pieces/pieces/pieces prochain_joueur qui_peut_roquer_et_o� case_pour_enpassant halfmove move_number
        split = fen.split(" ")
        lines = split[0].split("/")

        # Construction des pi�ces
        y = 0
        while y < 8:  # Vertical
            x = 0
            line: str = lines[y]
            if line.isnumeric():  # Il y a que des entiers, donc seulement un 8 cad ligne vide
                y += 1
                continue
            for char in line:  # Horizontal
                if char.isnumeric():
                    # On doit sauter ce nombre de cases horizontalement
                    x += int(char)
                    continue
                # Si le caract�re de la pi�ce est en minuscule, c'est une pi�ce noire, blache sinon
                # Et on construit la pi�ce correspondante
                piece = Piece.new_piece(int(char.islower()), PIECES[char.upper()], (x, y), self.tilesize)
                # On stocke les rois noirs et blancs, c'est pratique de les avoir dans des variables
                if type(piece) == King:
                    if piece.color == NOIR:
                        self.black_king = piece
                    else:
                        self.white_king = piece
                # On place la pi�ce sur l'�chiquier
                self.board[y][x] = piece
                pieces.append(piece)
                # On l'ajoute �galement � la liste des pi�ces de m�me couleur
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

        # Le reste c'est en passant et le nombre de coup, pour l'instant �a m'int�resse pas
        # Mtn �a m'int�resse
        # En passant :
        if split[3] != '-':
            i, j = 0, 0
            sp = list(split[3])  # On s�pare caract�re par caract�re
            for char in sp:
                char: str
                if char.isnumeric():  # C'est la ligne, donc y
                    j = 8 - int(char)
                else:  # Lettre donc colonne
                    # Attention, les y sont vers le bas dans pygame !
                    i = ord(char) - ord('a')
            self.en_passant_square = (i, j)

        # Reste le nombre de coups � traiter
        return pieces, gamestate

    def color_squares(self, squares):
        for x, y in squares:
            pygame.draw.rect(self.temp_board, RED,
                             pygame.Rect(x * self.tilesize, y * self.tilesize, self.tilesize, self.tilesize))

    def is_in_check(self, position: tuple[int, int], color: int, ennemy_pieces) -> bool:
        """
        V�rifie si une case particuli�re de l'�chiquier est en prise par l'autre couleur.
        La case peut �tre d�j� occup�e par une pi�ce de la couleur attaquante, dans le cas d'une capture.

        :param position: La case de l'�chiquier � v�rifier
        :param color: La couleur de la pi�ce � la position
        :param ennemy_pieces: La liste des pi�ces ennemies
        :return:
        """
        x, y = position
        # On sauvegarde l'�ventuelle pi�ce ennemie � la position pass�e
        current = self.board[y][x]
        # On place une pi�ce potentielle de la couleur attaqu�e � la position
        self.board[y][x] = Potential(color, position)
        if current in ennemy_pieces:
            # On retire la pi�ce sauvegard�e des attaquants, pour ne pas fausser l'�valuation dans le cas d'une prise
            ennemy_pieces.remove(current)
        in_check = []
        for piece in ennemy_pieces:
            # Si on a trouv� avant de processer toutes les pi�ces ennemies, pas besoin de continuer
            if position in in_check:
                # On replace ce que l'on a remplac�
                self.board[y][x] = current
                if current:  # Si current == piece.VIDE (0), on le rajoute pas
                    ennemy_pieces.append(current)
                return True
            # Le roi ne peut pas mettre en �chec l'autre roi, pas besoin de v�rifier.
            if isinstance(piece, King): continue
            in_check.extend(piece.generate_moves_for_piece(piece.color, piece.current_square, self.board, True))
        # On replace la pi�ce initialement � la position
        self.board[y][x] = current
        if current:  # Si current == piece.VIDE (0), on le rajoute pas
            ennemy_pieces.append(current)
        return position in in_check

    def is_checkmate(self, color: int) -> bool:
        """
        V�rifie si le roi de la couleur fournie est actuellement en �chec et mat.

        :param color: La couleur attaqu�e
        :return: Si le roi est en �chec et mat
        """
        # On suppose que le roi est d�ja en �chec
        king = self.black_king if color == NOIR else self.white_king
        ennemy_pieces = self.white_pieces.copy() if color == NOIR else self.black_pieces.copy()
        # On g�n�re la liste des d�placements possibles du roi, auxquels on enl�ve ceux qui le mettent en �chec.
        king_moves = list(
                filter(lambda position: (not self.is_in_check(position, color, ennemy_pieces)), king.generate_all_moves(self.board)))
        if king_moves:
            # Si le roi peut bouger, pas besoin de v�rifier plus.
            return False
        # Le roi peut pas bouger, le seul moyen de pas etre en �chec est de bouger une pi�ce
        pieces = self.white_pieces if color == BLANC else self.black_pieces
        for piece in pieces:
            # On sait d�j� que le roi ne peut pas bouger
            if isinstance(piece, King):
                continue
            # noinspection PyTypeChecker
            if self.generate_legal_moves(piece, piece.generate_all_moves(self.board)):
                return False
        return True

    def generate_legal_moves(self, piece, pseudolegal_moves: list[tuple[int, int]]) -> list[tuple[int, int]]:
        """
        G�n�re, � partir de la liste des d�placements pseudo-l�gaux d'une pi�ce, la liste de ses d�placements l�gaux.
        Un d�placement est l�gal si il ne met ou laisse pas le roi en �chec.

        :param piece: La pi�ce concern�e
        :param pseudolegal_moves: La liste de ses d�placements pseudo-l�gaux, cad sans tenir compte des �checs/clouages etc
        :return: La liste (�ventuellement vide) des d�placements possible
        """
        legal = []
        king = self.black_king if piece.color == NOIR else self.white_king
        ennemy_pieces = self.white_pieces.copy() if piece.color == NOIR else self.black_pieces.copy()
        # On retire la pi�ce de sa case actuelle, puisqu'elle va se d�placer
        self.board[piece.current_square[1]][piece.current_square[0]] = VIDE

        for position in pseudolegal_moves:
            (x, y) = position
            # On sauvegarde la pi�ce actuellement sur la case.
            current = self.board[y][x]
            # On y place une pi�ce temporaire de la couleur de la pi�ce se d�pla�ant.
            self.board[y][x] = Potential(piece.color, position)
            if current in ennemy_pieces:
                # On retire l'�ventuelle pi�ce prise des pi�ces ennemies pour ne pas fausser l'�valuation.
                ennemy_pieces.remove(current)
            # Si le roi n'est pas en �chec apr�s le d�placement, il est l�gal
            if not self.is_in_check(king.current_square, piece.color, ennemy_pieces):
                legal.append(position)
            # On replace la pi�ce sauvegard�e
            self.board[y][x] = current
            if current:  # Si current == piece.VIDE (0), on le rajoute pas
                ennemy_pieces.append(current)
        # Enfin, on replace la pi�ce d�plac�e
        self.board[piece.current_square[1]][piece.current_square[0]] = piece
        return legal

    def print_board(self):
        for line in self.board:
            print(line)
