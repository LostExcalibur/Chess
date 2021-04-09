import piece


class Potential(piece.Piece):
    def __init__(self, color: int, position: tuple[int, int]):
        super().__init__()
        self.color = color
        self.current_square = position
