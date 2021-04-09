import piece
from piece import Piece


class King(Piece):
    def __init__(self, color: int, position: tuple[int, int], tilesize: int):
        self.name = "b" * (color == 1) + "w" * (color == 0) + "K.png"
        super(King, self).__init__(tilesize, self.name, "king")

        self.current_square = position
        self.color = color

    def generate_all_moves(self, board) -> list[tuple[int, int]]:
        return self.generate_moves_for_piece(self.color, self.current_square, board)

    @staticmethod
    def generate_moves_for_piece(color: int, position: tuple[int, int], board, only_captures: bool = False) -> list[tuple[int, int]]:
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
                if board[y + j][x + i] == piece.VIDE:
                    if not only_captures:
                        moves.append((x + i, y + j))
                elif board[y + j][x + i].color != color:
                    moves.append((x + i, y + j))

        return moves

    def __repr__(self):
        return "Black " * (self.color == 1) + "White " * (self.color == 0) + super(King, self).__repr__()
