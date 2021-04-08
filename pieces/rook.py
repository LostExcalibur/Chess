import piece


class Rook(piece.Piece):
    def __init__(self, color: int, position: tuple[int, int], tilesize: int):
        self.name = "b" * (color == 1) + "w" * (color == 0) + "R.png"
        super(Rook, self).__init__(tilesize, self.name, "rook")

        self.current_square = position
        self.color = color

    @staticmethod
    def generate_moves_for_piece(color: int, position: tuple[int, int], board) -> list[tuple[int, int]]:
        moves = []
        x, y = position
        droite = 8 - x
        gauche = x + 1
        haut = y + 1
        bas = 8 - y
        for i in range(1, droite):
            if board[y][x + i] == piece.VIDE:
                moves.append((x + i, y))
            elif board[y][x + i] != piece.VIDE:
                if board[y][x + i].color != color:
                    moves.append((x + i, y))
                break

        for i in range(1, gauche):
            if board[y][x - i] == piece.VIDE:
                moves.append((x - i, y))
            elif board[y][x - i] != piece.VIDE:
                if board[y][x - i].color != color:
                    moves.append((x - i, y))
                break

        for i in range(1, haut):
            if board[y - i][x] == piece.VIDE:
                moves.append((x, y - i))
            elif board[y - i][x] != piece.VIDE:
                if board[y - i][x].color != color:
                    moves.append((x, y - i))
                break

        for i in range(1, bas):
            if board[y + i][x] == piece.VIDE:
                moves.append((x, y + i))
            elif board[y + i][x] != piece.VIDE:
                if board[y + i][x].color != color:
                    moves.append((x, y + i))
                break
        return moves

    def generate_all_moves(self, board) -> list[tuple[int, int]]:
        return self.generate_moves_for_piece(self.color, self.current_square, board)

    def __repr__(self):
        return "Black " * (self.color == 1) + "White " * (self.color == 0) + super(Rook, self).__repr__()
