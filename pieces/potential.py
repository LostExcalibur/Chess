import piece


class Potential(piece.Piece):
    def __init__(self, color: int, position: tuple[int, int]):
        super().__init__(None, None, "potential")
        self.color = color
        self.current_square = position
