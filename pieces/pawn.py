import piece


class Pawn(piece.Piece):
    def __init__(self, color: int, position: tuple[int, int], tilesize: int):
        self.name = "b" * (color == 1) + "w" * (color == 0) + "P.png"
        super(Pawn, self).__init__(tilesize, self.name, "pawn")

        self.current_square = position
        self.color = color

    @staticmethod
    def generate_moves_for_piece(color: int, position: tuple[int, int], board) -> list[tuple[int, int]]:
        moves = []
        x, y = position
        if color == piece.BLANC:
            if y > 0:
                if y == 6 and board[y - 2][x] == piece.VIDE:  # Premier déplacement
                    moves.append((x, y - 2))
                if board[y - 1][x] == piece.VIDE:
                    moves.append((x, y - 1))
                if x < 7 and board[y - 1][x + 1] != piece.VIDE:
                    if board[y - 1][x + 1].color != color:
                        moves.append((x + 1, y - 1))
                if x > 0 and board[y - 1][x - 1] != piece.VIDE:
                    if board[y - 1][x - 1].color != color:
                        moves.append((x - 1, y - 1))
        elif color == piece.NOIR:
            if y < 7:
                if y == 1 and board[y + 2][x] == piece.VIDE:  # Premier déplacement
                    moves.append((x, y + 2))
                if board[y + 1][x] == piece.VIDE:
                    moves.append((x, y + 1))
                if x < 7 and board[y + 1][x + 1] != piece.VIDE:
                    if board[y + 1][x + 1].color != color:
                        moves.append((x + 1, y + 1))
                if x > 0 and board[y + 1][x - 1] != piece.VIDE:
                    if board[y + 1][x - 1].color != color:
                        moves.append((x - 1, y + 1))
        return moves

    def generate_all_moves(self, board) -> list[tuple[int, int]]:
        return self.generate_moves_for_piece(self.color, self.current_square, board)

    def __repr__(self):
        return "Black " * (self.color == 1) + "White " * (self.color == 0) + super(Pawn, self).__repr__()
