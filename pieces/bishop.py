from piece import Piece, VIDE, BLANC


class Bishop(Piece):
	_positional_eval = [[-20, -10, -10, -10, -10, -10, -10, -20],
						[-10, 0, 0, 0, 0, 0, 0, -10],
						[-10, 0, 5, 10, 10, 5, 0, -10],
						[-10, 5, 5, 10, 10, 5, 5, -10],
						[-10, 0, 10, 10, 10, 10, 0, -10],
						[-10, 10, 10, 10, 10, 10, 10, -10],
						[-10, 5, 0, 0, 0, 0, 5, -10],
						[-20, -10, -10, -10, -10, -10, -10, -20]]

	def __init__(self, color: int, position: tuple[int, int], tilesize: int):
		self.name = "b" * (color == 1) + "w" * (color == 0) + "B.png"
		super(Bishop, self).__init__(tilesize, self.name, "bishop")

		self.current_square = position
		self.color = color
		self.letter = "B"
		self.worth = 300

	@staticmethod
	def generate_moves_for_piece(color: int, position: tuple[int, int], board: list[list[Piece]],
								 only_captures: bool = False) -> list[tuple[int, int]]:
		moves = []
		x, y = position
		droite = 8 - x
		gauche = x + 1
		haut = y + 1
		bas = 8 - y

		for i in range(1, min(droite, haut)):
			if board[y - i][x + i] == VIDE:
				if not only_captures:
					moves.append((x + i, y - i))
			else:
				if board[y - i][x + i].color != color:
					moves.append((x + i, y - i))
				break

		for i in range(1, min(haut, gauche)):
			if board[y - i][x - i] == VIDE:
				if not only_captures:
					moves.append((x - i, y - i))
			else:
				if board[y - i][x - i].color != color:
					moves.append((x - i, y - i))
				break

		for i in range(1, min(gauche, bas)):
			if board[y + i][x - i] == VIDE:
				if not only_captures:
					moves.append((x - i, y + i))
			else:
				if board[y + i][x - i].color != color:
					moves.append((x - i, y + i))
				break

		for i in range(1, min(bas, droite)):
			if board[y + i][x + i] == VIDE:
				if not only_captures:
					moves.append((x + i, y + i))
			else:
				if board[y + i][x + i].color != color:
					moves.append((x + i, y + i))
				break

		return moves

	def generate_all_moves(self, board: list[list[Piece]]) -> list[tuple[int, int]]:
		return self.generate_moves_for_piece(self.color, self.current_square, board)

	def get_positional_score(self, x: int, y: int) -> int:
		return self._positional_eval[y][x] if self.color == BLANC else self._positional_eval[7 - y][x]

	def __repr__(self):
		return "Black " * (self.color == 1) + "White " * (self.color == 0) + super(Bishop, self).__repr__()
