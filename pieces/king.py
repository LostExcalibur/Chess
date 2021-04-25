# encoding=latin-1

from piece import Piece, VIDE
from pieces.rook import Rook


class King(Piece):
    def __init__(self, color: int, position: tuple[int, int], tilesize: int):
        self.name = "b" * (color == 1) + "w" * (color == 0) + "K.png"
        super(King, self).__init__(tilesize, self.name, "king")

        self.current_square = position
        self.color = color

    def generate_all_moves(self, board: list[list[Piece]]) -> list[tuple[int, int]]:
        return self.generate_moves_for_piece(self.color, self.current_square, board)

    @staticmethod
    def generate_moves_for_piece(color: int, position: tuple[int, int], board: list[list[Piece]], only_captures: bool = False) -> list[tuple[int, int]]:
        moves = []
        x, y = position
        gauche = - min(1, x)
        droite = min(1, 7 - x)
        haut = - min(1, y)
        bas = min(1, 7 - y)
        for i in range(gauche, droite + 1):
            for j in range(haut, bas + 1):
                if i == j == 0:
                    continue
                if board[y + j][x + i] == VIDE:
                    if not only_captures:
                        moves.append((x + i, y + j))
                elif board[y + j][x + i].color != color:
                    moves.append((x + i, y + j))
        return moves

    @staticmethod
    def can_castle(position: tuple, board: list[list[Piece]], state: int) -> tuple[bool, bool]:
        """
        Vérifie si le roi peut roquer, sans vérifier les échecs ou si le roi ou la tour s'est déplacé.

        :param position: La position actuelle du roi
        :param board: L'état actuel de l'échiquier
        :param state: La légalité du roque, queenside puis kingside
        :return: La pseudolégalité du roque en terme de déplacement
        """
        queenside = True
        kingside  = True
        x, y = position
        # Queenside
        if state >> 1:
            for i in range(1, 4):
                if board[y][x - i] != VIDE:
                    queenside = False
            if queenside:
                if not isinstance(board[y][0], Rook) or not board[y][0].color == board[y][x].color:
                    queenside = False
        # If kingside
        if state & 1:
            for i in range(1, 3):
                if board[y][x + i] != VIDE:
                    kingside = False
            if kingside:
                if not isinstance(board[y][7], Rook) or not board[y][7].color == board[y][x].color:
                    kingside = False
        return queenside, kingside

    def __repr__(self):
        return "Black " * (self.color == 1) + "White " * (self.color == 0) + super(King, self).__repr__()
