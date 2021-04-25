from piece import Piece


class Potential(Piece):
    def __init__(self, color: int, position: tuple[int, int]):
        super().__init__(None, None, "potential")
        self.color = color
        self.current_square = position
