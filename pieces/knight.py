import piece


class Knight(piece.Piece):
    def __init__(self, color: int, position: tuple[int, int], tilesize: int):
        self.name = "b" * (color == 1) + "w" * (color == 0) + "N.png"
        super(Knight, self).__init__(tilesize, self.name, "knight")

        self.current_square = position
        self.color = color

    def __repr__(self):
        return "Black " * (self.color == 1) + "White " * (self.color == 0) + super(Knight, self).__repr__()
