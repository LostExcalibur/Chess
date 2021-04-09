import piece


class Bishop(piece.Piece):
    def __init__(self, color: int, position: tuple[int, int], tilesize: int):
        self.name = "b" * (color == 1) + "w" * (color == 0) + "B.png"
        super(Bishop, self).__init__(tilesize, self.name, "bishop")

        self.current_square = position
        self.color = color

    @staticmethod
    def generate_moves_for_piece(color: int, position: tuple[int, int], board, only_captures: bool = False) -> list[tuple[int, int]]:
        moves = []
        x, y = position
        droite = 8 - x
        gauche = x + 1
        haut = y + 1
        bas = 8 - y

        for i in range(1, min(droite, haut)):
            if board[y - i][x + i] == piece.VIDE:
                if not only_captures:
                    moves.append((x + i, y - i))
            else:
                if board[y - i][x + i].color != color:
                    moves.append((x + i, y - i))
                break

        for i in range(1, min(haut, gauche)):
            if board[y - i][x - i] == piece.VIDE:
                if not only_captures:
                    moves.append((x - i, y - i))
            else:
                if board[y - i][x - i].color != color:
                    moves.append((x - i, y - i))
                break

        for i in range(1, min(gauche, bas)):
            if board[y + i][x - i] == piece.VIDE:
                if not only_captures:
                    moves.append((x - i, y + i))
            else:
                if board[y + i][x - i].color != color:
                    moves.append((x - i, y + i))
                break

        for i in range(1, min(bas, droite)):
            if board[y + i][x + i] == piece.VIDE:
                if not only_captures:
                    moves.append((x + i, y + i))
            else:
                if board[y + i][x + i].color != color:
                    moves.append((x + i, y + i))
                break

        return moves

    def generate_all_moves(self, board) -> list[tuple[int, int]]:
        return self.generate_moves_for_piece(self.color, self.current_square, board)

    def __repr__(self):
        return "Black " * (self.color == 1) + "White " * (self.color == 0) + super(Bishop, self).__repr__()
