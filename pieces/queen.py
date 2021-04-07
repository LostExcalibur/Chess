import piece


class Queen(piece.Piece):
    def __init__(self, color: int, position: tuple[int, int], tilesize: int):
        self.name = "b" * (color == 1) + "w" * (color == 0) + "Q.png"
        super(Queen, self).__init__(tilesize, self.name)

        self.current_square = position
