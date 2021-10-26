from piece import BLANC, Piece, VIDE


class Rook(Piece):
	_positional_eval = [[0, 0, 0, 0, 0, 0, 0, 0],
						[5, 10, 10, 10, 10, 10, 10, 5],
						[-5, 0, 0, 0, 0, 0, 0, -5],
						[-5, 0, 0, 0, 0, 0, 0, -5],
						[-5, 0, 0, 0, 0, 0, 0, -5],
						[-5, 0, 0, 0, 0, 0, 0, -5],
						[-5, 0, 0, 0, 0, 0, 0, -5],
						[0, 0, 0, 5, 5, 0, 0, 0]]

	def __init__(self, color: int, position: tuple[int, int], tilesize: int):
		self.name = "b" * (color == 1) + "w" * (color == 0) + "R.png"
		super(Rook, self).__init__(tilesize, self.name, "rook")

		self.current_square = position
		self.color = color
		self.letter = "R"
		self.worth = 500

	@staticmethod
	def generate_moves_for_piece(color: int, position: tuple[int, int], board: list[list[Piece]],
								 only_captures: bool = False) -> list[tuple[int, int]]:
		moves = []
		x, y = position
		droite = 8 - x
		gauche = x + 1
		haut = y + 1
		bas = 8 - y
		for i in range(1, droite):
			if board[y][x + i] == VIDE:
				if not only_captures:
					moves.append((x + i, y))
			else:
				if board[y][x + i].color != color:
					moves.append((x + i, y))
				break

		for i in range(1, gauche):
			if board[y][x - i] == VIDE:
				if not only_captures:
					moves.append((x - i, y))
			else:
				if board[y][x - i].color != color:
					moves.append((x - i, y))
				break

		for i in range(1, haut):
			if board[y - i][x] == VIDE:
				if not only_captures:
					moves.append((x, y - i))
			else:
				if board[y - i][x].color != color:
					moves.append((x, y - i))
				break

		for i in range(1, bas):
			if board[y + i][x] == VIDE:
				if not only_captures:
					moves.append((x, y + i))
			else:
				if board[y + i][x].color != color:
					moves.append((x, y + i))
				break
		return moves

	def generate_all_moves(self, board: list[list[Piece]]) -> list[tuple[int, int]]:
		return self.generate_moves_for_piece(self.color, self.current_square, board)

	def get_positional_score(self, x: int, y: int) -> int:
		return self._positional_eval[y][x] if self.color == BLANC else self._positional_eval[7 - y][x]

	def __repr__(self):
		return "Black " * (self.color == 1) + "White " * (self.color == 0) + super(Rook, self).__repr__()
