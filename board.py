from piece import *

BLACK = pygame.Color(0, 0, 0)
BROWN = pygame.Color(181, 136, 99)
WHITE = pygame.Color(255, 255, 255)
LAQUE = pygame.Color(240, 217, 181)


class Board:
	def __init__(self, width: int, height: int):
		pygame.init()
		self.caption = "Chess"
		self.size = (width, height)
		self.width = width
		self.height = height
		self.screen = pygame.display.set_mode(self.size)
		self.tilesize = int(min(width, height) / 8)
		self.board = self.build_board()
		self.running = True
		self.pieces = []
		self.create_pieces()

	def build_board(self):
		board = pygame.Surface((self.tilesize * 8, self.tilesize * 8))
		board.fill(BROWN)
		for x in range(8):
			for y in range(8):
				if (x + y) % 2 == 1:
					pygame.draw.rect(board, LAQUE, pygame.Rect(x * self.tilesize, y * self.tilesize,
					                                           self.tilesize, self.tilesize))
		board = pygame.transform.flip(board, True, False)
		return board

	def run(self):
		pygame.display.set_caption(self.caption)
		while self.running:
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					self.running = False
			self.screen.blit(self.board, self.board.get_rect())
			for piece in self.pieces:
				self.screen.blit(piece.image,
				                 (piece.current_square[0] * self.tilesize,
				                  piece.current_square[1] * self.tilesize))
			pygame.display.update()

	def create_pieces(self):
		self.pieces = self.parse_FEN("rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1")
		# self.pieces.append(Piece(1 << 5, 0, self.tilesize))

	def parse_FEN(self, fen: str) -> list[Piece]:
		pieces = []
		gamestate = 0b11111111

		split = fen.split(" ")
		lines = split[0].split("/")

		# On construit d'abord les pieces
		for l, line in enumerate(lines):
			if line.isnumeric():  # Il y a que des entiers, donc seulement un 8 cad ligne video
				continue
			skip = 0
			for f, char in enumerate(line):
				f: int
				char: str
				if skip > 0:
					skip -= 1
					continue
				if char.isnumeric():
					skip = int(char) - 1
					continue
				pieces.append(Piece(PIECES[char.upper()], int(char.islower()), self.tilesize, (f, l)))

		return pieces
