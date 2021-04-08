import piece


class Rook(piece.Piece):
    def __init__(self, color: int, position: tuple[int, int], tilesize: int):
        self.name = "b" * (color == 1) + "w" * (color == 0) + "R.png"
        super(Rook, self).__init__(tilesize, self.name, "rook")

        self.current_square = position
        self.color = color

    def generate_all_moves(self, board) -> list[tuple[int, int]]:
        pass

    def __repr__(self):
        return "Black " * (self.color == 1) + "White " * (self.color == 0) + super(Rook, self).__repr__()
