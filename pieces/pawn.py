from piece import Piece, VIDE, BLANC, NOIR


class Pawn(Piece):
	_positional_eval = [[0, 0, 0, 0, 0, 0, 0, 0],
						[50, 50, 50, 50, 50, 50, 50, 50],
						[10, 10, 20, 30, 30, 20, 10, 10],
						[5, 5, 10, 25, 25, 10, 5, 5],
						[0, 0, 0, 20, 20, 0, 0, 0],
						[5, -5, -10, 0, 0, -10, -5, 5],
						[5, 10, 10, -20, -20, 10, 10, 5],
						[0, 0, 0, 0, 0, 0, 0, 0]]

	def __init__(self, color: int, position: tuple[int, int], tilesize: int):
		self.name = "b" * (color == 1) + "w" * (color == 0) + "P.png"
		super(Pawn, self).__init__(tilesize, self.name, "pawn")

		self.current_square = position
		self.color = color
		self.en_passant_target = None
		self.worth = 100

	@staticmethod
	def generate_moves_for_piece(color: int, position: tuple[int, int], board: list[list[Piece]],
								 only_captures: bool = False) -> list[tuple[int, int]]:
		moves = []
		x, y = position
		if color == BLANC:
			if board[y - 1][x] == VIDE and not only_captures:
				moves.append((x, y - 1))
				if y == 6 and board[y - 2][x] == VIDE and not only_captures:  # Premier déplacement
					moves.append((x, y - 2))
			if x < 7 and board[y - 1][x + 1] != VIDE:
				if board[y - 1][x + 1].color != color:
					moves.append((x + 1, y - 1))
			if x > 0 and board[y - 1][x - 1] != VIDE:
				if board[y - 1][x - 1].color != color:
					moves.append((x - 1, y - 1))
		elif color == NOIR:
			if board[y + 1][x] == VIDE and not only_captures:
				moves.append((x, y + 1))
				if y == 1 and board[y + 2][x] == VIDE and not only_captures:  # Premier déplacement
					moves.append((x, y + 2))
			if x < 7 and board[y + 1][x + 1] != VIDE:
				if board[y + 1][x + 1].color != color:
					moves.append((x + 1, y + 1))
			if x > 0 and board[y + 1][x - 1] != VIDE:
				if board[y + 1][x - 1].color != color:
					moves.append((x - 1, y + 1))
		return moves

	def generate_all_moves(self, board: list[list[Piece]]) -> list[tuple[int, int]]:
		moves = self.generate_moves_for_piece(self.color, self.current_square, board)
		if self.en_passant_target and Pawn.can_en_passant(self.color, self.current_square, self.en_passant_target):
			moves.append(self.en_passant_target)
		return moves

	def get_positional_score(self, x: int, y: int) -> int:
		return self._positional_eval[y][x] if self.color == BLANC else self._positional_eval[7 - y][x]

	@staticmethod
	def can_en_passant(color: int, position: tuple[int, int], en_passant_square: tuple[int, int]):
		x, y = position
		return (color == BLANC and en_passant_square in [(x + 1, y - 1), (x - 1, y - 1)]) or \
			   (color == NOIR and en_passant_square in [(x + 1, y + 1), (x - 1, y + 1)])

	def __repr__(self):
		return "Black " * (self.color == 1) + "White " * (self.color == 0) + super(Pawn, self).__repr__()
