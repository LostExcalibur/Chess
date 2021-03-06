from piece import Piece, VIDE
from itertools import product


class Knight(Piece):
    def __init__(self, color: int, position: tuple[int, int], tilesize: int):
        self.name = "b" * (color == 1) + "w" * (color == 0) + "N.png"
        super(Knight, self).__init__(tilesize, self.name, "knight")

        self.current_square = position
        self.color = color
        self.letter = "N"
        self.worth = 3

    # J'ai ?videmment pas trouv? ?a tout seul, cr?dit :
    # https://stackoverflow.com/a/19372692/14606122
    @staticmethod
    def generate_moves_for_piece(color: int, position: tuple[int, int], board, only_captures: bool = False) -> list[tuple[int, int]]:
        x, y = position
        moves = list(product([x - 1, x + 1], [y - 2, y + 2])) + list(product([x - 2, x + 2], [y - 1, y + 1]))
        moves = [(x, y) for x, y in moves if 0 <= x < 8 and 0 <= y < 8 and
                 (board[y][x] == VIDE and not only_captures or board[y][x] != VIDE and board[y][x].color != color)]
        return moves

    def generate_all_moves(self, board: list[list[Piece]]) -> list[tuple[int, int]]:
        return self.generate_moves_for_piece(self.color, self.current_square, board)

    def __repr__(self):
        return "Black " * (self.color == 1) + "White " * (self.color == 0) + super(Knight, self).__repr__()
