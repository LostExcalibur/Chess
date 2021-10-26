from itertools import product

from piece import BLANC, Piece, VIDE


class Knight(Piece):
	_positional_eval = [[-50, -40, -30, -30, -30, -30, -40, -50],
						[-40, -20, 0, 0, 0, 0, -20, -40],
				   		[-30, 0, 10, 15, 15, 10, 0, -30],
				   		[-30, 5, 15, 20, 20, 15, 5, -30],
				   		[-30, 0, 15, 20, 20, 15, 0, -30],
				   		[-30, 5, 10, 15, 15, 10, 5, -30],
				   		[-40, -20, 0, 5, 5, 0, -20, -40],
				   		[-50, -40, -30, -30, -30, -30, -40, -50]]

	def __init__(self, color: int, position: tuple[int, int], tilesize: int):
		self.name = "b" * (color == 1) + "w" * (color == 0) + "N.png"
		super(Knight, self).__init__(tilesize, self.name, "knight")

		self.current_square = position
		self.color = color
		self.letter = "N"
		self.worth = 300

	# J'ai évidemment pas trouvé ça tout seul, crédit :
	# https://stackoverflow.com/a/19372692/14606122
	@staticmethod
	def generate_moves_for_piece(color: int, position: tuple[int, int], board, only_captures: bool = False) -> list[
		tuple[int, int]]:
		x, y = position
		moves = list(product([x - 1, x + 1], [y - 2, y + 2])) + list(product([x - 2, x + 2], [y - 1, y + 1]))
		moves = [(x, y) for x, y in moves if 0 <= x < 8 and 0 <= y < 8 and
				 (board[y][x] == VIDE and not only_captures or board[y][x] != VIDE and board[y][x].color != color)]
		return moves

	def generate_all_moves(self, board: list[list[Piece]]) -> list[tuple[int, int]]:
		return self.generate_moves_for_piece(self.color, self.current_square, board)

	def get_positional_score(self, x: int, y: int) -> int:
		return self._positional_eval[y][x] if self.color == BLANC else self._positional_eval[7 - y][x]

	def __repr__(self):
		return "Black " * (self.color == 1) + "White " * (self.color == 0) + super(Knight, self).__repr__()
