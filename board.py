import pygame.transform

from piece import *

BLACK = pygame.Color(0, 0, 0)
BROWN = pygame.Color(181, 136, 99)
WHITE = pygame.Color(255, 255, 255)
LAQUE = pygame.Color(240, 217, 181)
RED   = pygame.Color(255, 0, 0)


class Board:
	def __init__(self, width: int, height: int):
		pygame.init()
		self.caption = "Chess"
		self.size = (width, height)
		self.width = width
		self.height = height
		self.screen = pygame.display.set_mode(self.size, pygame.RESIZABLE)
		self.tilesize = int(min(width, height) / 8)
		self.board_surface = self.build_board()
		self.temp_board = self.board_surface.copy()
		self.running = True
		self.pieces: list[Piece] = []
		self.board = [[VIDE, VIDE, VIDE, VIDE, VIDE, VIDE, VIDE, VIDE],
					  [VIDE, VIDE, VIDE, VIDE, VIDE, VIDE, VIDE, VIDE],
					  [VIDE, VIDE, VIDE, VIDE, VIDE, VIDE, VIDE, VIDE],
					  [VIDE, VIDE, VIDE, VIDE, VIDE, VIDE, VIDE, VIDE],
					  [VIDE, VIDE, VIDE, VIDE, VIDE, VIDE, VIDE, VIDE],
					  [VIDE, VIDE, VIDE, VIDE, VIDE, VIDE, VIDE, VIDE],
					  [VIDE, VIDE, VIDE, VIDE, VIDE, VIDE, VIDE, VIDE],
					  [VIDE, VIDE, VIDE, VIDE, VIDE, VIDE, VIDE, VIDE]]
		self.beginning_FEN = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"
		self.testing_FEN = "r1bqkbnr/pppp1pp1/2n4p/4p3/2B1P3/5N2/PPPP1PPP/RNBQK2R w KQkq - 0 1"
		self.pieces, self.gamestate = \
			self.parse_FEN("rnbqkbnr/pppPpppp/8/8/8/8/PPPP1PPP/RNBQKBNR w KQkq - 0 1")

	def build_board(self):
		board = pygame.Surface((self.tilesize * 8, self.tilesize * 8))
		board.fill(BROWN)
		for x in range(8):
			for y in range(8):
				if (x + y) % 2:
					pygame.draw.rect(board, LAQUE, pygame.Rect(x * self.tilesize, y * self.tilesize,
					                                           self.tilesize, self.tilesize))
		board = pygame.transform.flip(board, True, False)
		return board

	def run(self):
		pygame.display.set_caption(self.caption)
		last_clicked = None
		while self.running:
			# Boucle d'évènements
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					self.running = False
				if event.type == pygame.MOUSEBUTTONDOWN and event.button == pygame.BUTTON_LEFT:
					self.temp_board = self.board_surface.copy()
					x, y = event.pos[0] // self.tilesize, event.pos[1] // self.tilesize
					# noinspection PyTypeChecker
					selected_piece: Piece = self.board[y][x]
					if selected_piece != VIDE:
						if selected_piece == last_clicked:
							self.temp_board = self.board_surface.copy()
							last_clicked = None
							continue
						squares = selected_piece.generate_all_moves(self.board)
						if squares:
							self.color_squares(squares)
						last_clicked = selected_piece

			# Affichage
			self.screen.blit(self.temp_board, self.temp_board.get_rect())
			for piece in self.pieces:
				self.screen.blit(piece.image,
				                 (piece.current_square[0] * self.tilesize,
				                  piece.current_square[1] * self.tilesize))
			pygame.display.update()

	def parse_FEN(self, fen: str) -> tuple[list[Piece], int]:
		pieces = []
		# De gauche à droite :
		# A qui de jouer : 1 noirs, 0 blancs
		# Echecs ? Noirs puis blancs
		# Roque coté reine puis roi, noirs puis blancs
		gamestate = 0b0001111

		split = fen.split(" ")
		lines = split[0].split("/")

		y = 0
		while y < 8:  # Vertical
			x = 0
			line: str = lines[y]
			if line.isnumeric():  # Il y a que des entiers, donc seulement un 8 cad ligne vide
				y += 1
				continue
			for char in line:  # Horizontal
				if char.isnumeric():
					x += int(char)
					continue
				piece = Piece.new_piece(int(char.islower()), PIECES[char.upper()], (x, y), self.tilesize)
				self.board[y][x] = piece
				pieces.append(piece)
				x += 1
			y += 1

		# A qui de jouer :
		if split[1] == 'w':  # Blancs
			gamestate &= 0b0111111
		elif split[1] == 'b':  # Noirs
			gamestate |= 0b1000000
		else:
			raise ValueError(f"Invalid fen :\n{fen}")

		# Roque
		if split[2] == '-':  # Personne peut roquer
			gamestate &= 0b1110000
		else:
			if "Q" in split[2]:
				gamestate |= 0b0000010
			if "K" in split[2]:
				gamestate |= 0b0000001
			if "q" in split[2]:
				gamestate |= 0b0001000
			if "k" in split[2]:
				gamestate |= 0b0000100

		# Le reste c'est en passant et le nombre de coup, pour l'instant ça m'intéresse pas

		return pieces, gamestate

	def color_squares(self, squares):
		for x, y in squares:
			pygame.draw.rect(self.temp_board, RED,
							 pygame.Rect(x * self.tilesize, y * self.tilesize, self.tilesize, self.tilesize))
