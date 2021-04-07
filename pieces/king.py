from piece import Piece


class King(Piece):
    def __init__(self, color: int, position: tuple[int, int], tilesize: int):
        self.name = "b" * (color == 1) + "w" * (color == 0) + "K.png"
        super(King, self).__init__(tilesize, self.name)

        self.current_square = position
