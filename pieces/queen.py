from piece import Piece
from pieces.rook import Rook
from pieces.bishop import Bishop


class Queen(Piece):
    def __init__(self, color: int, position: tuple[int, int], tilesize: int):
        self.name = "b" * (color == 1) + "w" * (color == 0) + "Q.png"
        super(Queen, self).__init__(tilesize, self.name, "queen")

        self.current_square = position
        self.color = color

    @staticmethod
    def generate_moves_for_piece(color: int, position: tuple[int, int], board: list[list[Piece]], only_captures: bool = False) -> list[tuple[int, int]]:
        moves = Rook.generate_moves_for_piece(color, position, board, only_captures)
        moves.extend(Bishop.generate_moves_for_piece(color, position, board, only_captures))
        return moves

    def generate_all_moves(self, board: list[list[Piece]]) -> list[tuple[int, int]]:
        return self.generate_moves_for_piece(self.color, self.current_square, board)

    def __repr__(self):
        return "Black " * (self.color == 1) + "White " * (self.color == 0) + super(Queen, self).__repr__()
