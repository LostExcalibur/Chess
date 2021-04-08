import piece


class Bishop(piece.Piece):
    def __init__(self, color: int, position: tuple[int, int], tilesize: int):
        self.name = "b" * (color == 1) + "w" * (color == 0) + "B.png"
        super(Bishop, self).__init__(tilesize, self.name, "bishop")

        self.current_square = position
        self.color = color

    def generate_all_moves(self, board) -> list[tuple[int, int]]:
        moves = []
        x, y = self.current_square
        droite = 8 - x
        gauche = x + 1
        haut = y + 1
        bas = 8 - y

        for i in range(1, min(droite, haut)):
            if board[y - i][x + i] == piece.VIDE:
                moves.append((x + i, y - i))
            elif board[y - i][x + i] != piece.VIDE:
                if board[y - i][x + i].color != self.color:
                    moves.append((x + i, y - i))
                break

        for i in range(1, min(haut, gauche)):
            if board[y - i][x - i] == piece.VIDE:
                moves.append((x - i, y - i))
            elif board[y - i][x - i] != piece.VIDE:
                if board[y - i][x - i].color != self.color:
                    moves.append((x - i, y - i))
                break

        for i in range(1, min(gauche, bas)):
            if board[y + i][x - i] == piece.VIDE:
                moves.append((x - i, y + i))
            elif board[y + i][x - i] != piece.VIDE:
                if board[y + i][x - i].color != self.color:
                    moves.append((x - i, y + i))
                break

        for i in range(1, min(bas, droite)):
            if board[y + i][x + i] == piece.VIDE:
                moves.append((x + i, y + i))
            elif board[y + i][x + i] != piece.VIDE:
                if board[y + i][x + i].color != self.color:
                    moves.append((x + i, y + i))
                break

        return moves

    def __repr__(self):
        return "Black " * (self.color == 1) + "White " * (self.color == 0) + super(Bishop, self).__repr__()
