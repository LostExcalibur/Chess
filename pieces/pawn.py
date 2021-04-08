import piece


class Pawn(piece.Piece):
    def __init__(self, color: int, position: tuple[int, int], tilesize: int):
        self.name = "b" * (color == 1) + "w" * (color == 0) + "P.png"
        super(Pawn, self).__init__(tilesize, self.name, "pawn")

        self.current_square = position
        self.color = color

    def generate_all_moves(self, board) -> list[tuple[int, int]]:
        moves = []
        x, y = self.current_square
        if self.color == piece.BLANC:
            if y > 0:
                if board[y - 1][x] == piece.VIDE:
                    moves.append((x, y - 1))
                if x < 7 and board[y - 1][x + 1] != piece.VIDE:
                    if board[y - 1][x + 1].color != self.color:
                        moves.append((x + 1, y - 1))
                if x > 0 and board[y - 1][x - 1] != piece.VIDE:
                    if board[y - 1][x - 1].color != self.color:
                        moves.append((x - 1, y - 1))
        elif self.color == piece.NOIR:
            if y < 7:
                if board[y + 1][x] == piece.VIDE:
                    moves.append((x, y + 1))
                if x < 7 and board[y + 1][x + 1] != piece.VIDE:
                    if board[y + 1][x + 1].color != self.color:
                        moves.append((x + 1, y + 1))
                if x > 0 and board[y + 1][x - 1] != piece.VIDE:
                    if board[y + 1][x - 1].color != self.color:
                        moves.append((x - 1, y + 1))
        return moves

    def __repr__(self):
        return "Black " * (self.color == 1) + "White " * (self.color == 0) + super(Pawn, self).__repr__()
