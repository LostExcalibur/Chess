# encoding=latin-1

import pygame.transform
from easygui import choicebox
from move import Move

from piece import *
from pieces.potential import Potential

BROWN = pygame.Color(181, 136, 99)
LAQUE = pygame.Color(240, 217, 181)
RED = pygame.Color(255, 0, 0)


class Board:
	def __init__(self, width: int = 600, height: int = 600):
		pygame.init()
		self.caption = "Chess"
		self.size = (width, height)
		self.width = width
		self.height = height
		self.screen = pygame.display.set_mode(self.size)
		self.tilesize = int(min(width, height) / 8)
		self.board_surface = self.build_board()
		self.capture_piece_image = pygame.transform.smoothscale(
				pygame.image.load(path.join("resources", "capture.png")),
				(self.tilesize, self.tilesize))
		self.check_image = pygame.transform.smoothscale(pygame.image.load(path.join("resources", "check.png")),
		                                                (self.tilesize, self.tilesize))
		self.move_image = pygame.transform.smoothscale(pygame.image.load(path.join("resources", "move.png")),
		                                               (self.tilesize, self.tilesize))
		self.temp_board = self.board_surface.copy()
		self.running = True
		self.pieces: list[Piece] = []
		self.white_pieces: list[Piece] = []
		self.black_pieces: list[Piece] = []
		self.en_passant_square = None
		self.black_king = self.white_king = None
		self.white_material_count = self.black_material_count = 0
		self.stalemate = False
		self.evaluation = 0
		self.movecount = 0
		self.halfmove = 0
		self.moves: list[Move] = []
		self.travelled_moves: list[Move] = []
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
		self.testing_FEN2 = "rnbqkbn1/pppPppp1/5p2/7r/4R3/6P1/PPPP1PP1/RNBQKBN1 w Qq - 0 1"
		self.castling_FEN = "rnbqk2r/pppp1ppp/4pn2/2b5/2B5/4PN2/PPPP1PPP/RNBQK2R w KQkq - 0 1"
		self.castling_FEN2 = "r3kbnr/pppqpppp/2n5/3p1b2/3P1B2/2N5/PPPQPPPP/R3KBNR w KQkq - 0 1"
		self.stalemate_FEN = "k7/8/8/8/5q2/8/8/7K b - - 0 1"
		self.pieces, self.gamestate = \
			self.parse_FEN(self.beginning_FEN)
		# self.saved_pieces = self.saved_board = self.saved_gamestate = None
		self.calculate_evaluation()

	def build_board(self) -> pygame.Surface:
		"""
		Construit la surface qui contient les sprites des cases, que l'on stocke dans une variable
		plutôt que de la générer à chaque frame, ce qui serait vraiment pas efficace

		:return: La surface de l'échiquier
		"""
		board = pygame.Surface((self.tilesize * 8, self.tilesize * 8))
		board.fill(BROWN)
		for x in range(8):
			for y in range(8):
				if (x + y) % 2:
					pygame.draw.rect(board, LAQUE, pygame.Rect(x * self.tilesize, y * self.tilesize,
					                                           self.tilesize, self.tilesize))
		# Il faut la retourner selon les x, car pygame a son axe vertical (y) vers le bas
		board = pygame.transform.flip(board, True, False)
		return board

	def run(self) -> None:
		"""
		La boucle principale du plateau.
		"""
		pygame.display.set_caption(self.caption)
		icon = pygame.image.load(path.join("resources", "chess.jpg"))
		pygame.display.set_icon(pygame.transform.scale(icon, (32, 32)))
		last_clicked = None
		legal_moves = None
		castling = None
		promoted = None
		while self.running:
			# Boucle d'évènements
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					self.running = False

				if event.type == pygame.KEYDOWN:
					self.handle_keys(event)

				if event.type == pygame.MOUSEBUTTONDOWN and event.button == pygame.BUTTON_LEFT:
					self.temp_board = self.board_surface.copy()
					x, y = event.pos[0] // self.tilesize, event.pos[1] // self.tilesize
					x: int
					y: int
					if last_clicked is not None and legal_moves and not self.travelled_moves:  # Le joueur avait cliqué sur une autre pièce avant
						if (x, y) in legal_moves:  # et essaie de la déplacer
							self.temp_board = self.board_surface.copy()  # On nettoie la surface du plateau
							current_x, current_y = last_clicked.current_square
							tobetaken = self.board[y][x]
							# On stocke l'état actuel du jeu, et on fait les modifications sur cette variable
							new_gamestate = self.gamestate

							# On va prendre en-passant
							if (x, y) == self.en_passant_square and type(last_clicked) == Pawn:
								tobetaken = self.board[y - 1][x] if (self.gamestate >> 6) else self.board[y + 1][x]

							# Si les blancs peuvent roquer, et si une tour noir bouge,
							# on enlève les droits de roque du côté correspondant
							# Si c'est le roi qui bouge, il perd tous ses droits de roque
							if self.gamestate & 0b11:
								if last_clicked == self.white_king:
									new_gamestate &= 0b1111100
									# Le roi a bougé, on vérifie si il a roqué et on déplace la tour en fonction
									# Roque kingside
									if x - self.white_king.current_square[0] > 1:
										self.move_piece(self.board[y][x + 1], (x - 1, y))
										castling = 0
									# Roque queenside
									elif x - self.white_king.current_square[0] < -1:
										self.move_piece(self.board[y][x - 2], (x + 1, y))
										castling = 1

								elif (x, y) == (0, 7) or last_clicked.current_square == (0, 7):
									new_gamestate &= 0b1111101
								elif (x, y) == (7, 7) or last_clicked.current_square == (7, 7):
									new_gamestate &= 0b1111110
							# Pareil avec les noirs
							if (self.gamestate >> 2) & 0b11:
								if last_clicked == self.black_king:
									new_gamestate &= 0b1110011
									# Roque kingside
									if x - self.black_king.current_square[0] > 1:
										self.move_piece(self.board[y][x + 1], (x - 1, y))
										castling = 0
									# Roque queenside
									elif x - self.black_king.current_square[0] < -1:
										self.move_piece(self.board[y][x - 2], (x + 1, y))
										castling = 1

								elif (x, y) == (7, 0) or last_clicked.current_square == (7, 0):
									new_gamestate &= 0b1111011
								elif (x, y) == (0, 0) or last_clicked.current_square == (0, 0):
									new_gamestate &= 0b1110111

							# Si on prend une pièce, il faut la retirer de la liste globale des pièces et de celle des pièces de cette couleur
							if tobetaken != VIDE:
								self.pieces.remove(tobetaken)
								(self.black_pieces if tobetaken.color == NOIR else self.white_pieces).remove(tobetaken)
							self.move_piece(last_clicked, (x, y))

							if type(last_clicked) == Pawn and (y == current_y + 2 or y == current_y - 2):
								self.en_passant_square = (x, y - 1) if last_clicked.color == NOIR else (x, y + 1)
							else:
								self.en_passant_square = None

							# Promotion de pion :
							if type(last_clicked) == Pawn:
								promoted = self.promote_pawn(last_clicked, True)

							# On met à jour l'état du jeu :
							# - On passe au joueur suivant
							new_gamestate ^= (1 << 6)
							# - On détecte les échecs :
							if new_gamestate >> 6:
								# Les noirs vont jouer, donc on vérifie que les blancs ont gagné ou pas au tour qu'ils viennent de jouer
								if self.is_in_check(self.black_king.current_square, NOIR, self.white_pieces):
									if self.is_checkmate(NOIR):
										self.running = False
										print("Les blancs gagnent par échec et mat")
									else:
										new_gamestate |= 1 << 5
								elif self.is_stalemate(NOIR):
									print("Il y a pat, égalité")
									self.running = False
									self.stalemate = True
								# Les blancs viennent de jouer, donc ils ne sont forcément plus en échec
								# sinon il y aurait eu mat au coup précédent
								new_gamestate &= 0b1101111

							else:
								if self.is_in_check(self.white_king.current_square, BLANC, self.black_pieces):
									if self.is_checkmate(BLANC):
										self.running = False
										print("Les noirs gagnent par échec et mat")
									else:
										new_gamestate |= 1 << 4
								elif self.is_stalemate(BLANC):
									print("Il y a pat, égalité")
									self.stalemate = True
									self.running = False
								new_gamestate &= 0b1011111
								self.movecount += 1

							self.moves.append(Move((x, y), (current_x, current_y), last_clicked, self.gamestate,
							                       new_gamestate, tobetaken if tobetaken else None, castling,
							                       promoted, bool(new_gamestate & 0b0110000)))

							last_clicked = None
							legal_moves = None
							castling = None
							promoted = None
							self.gamestate = new_gamestate
							self.halfmove = 0 if tobetaken or isinstance(last_clicked, Pawn) else self.halfmove + 1
							self.calculate_evaluation()
							# self.print_gamestate()
							continue

						else:
							if (x, y) != last_clicked.current_square:
								last_clicked = legal_moves = None

					selected_piece: Piece = self.board[y][x]
					# gamestate >> 6 correspond au joueur actuel, 1 = noir
					if selected_piece != VIDE and selected_piece.color == (self.gamestate >> 6):
						if selected_piece == last_clicked:
							self.temp_board = self.board_surface.copy()
							last_clicked = legal_moves = None
							continue
						if isinstance(selected_piece, Pawn) and self.en_passant_square:
							selected_piece: Pawn
							selected_piece.en_passant_target = self.en_passant_square
						pseudolegal_moves = selected_piece.generate_all_moves(self.board)
						if isinstance(selected_piece, King):
							ennemy_pieces = self.white_pieces.copy() if selected_piece.color == NOIR else self.black_pieces.copy()

							legal_moves = self.legal_king_moves(selected_piece, ennemy_pieces, pseudolegal_moves)
						else:
							legal_moves = self.generate_legal_moves(selected_piece, pseudolegal_moves)
						if legal_moves:
							self.draw_on_squares(legal_moves)
						last_clicked = selected_piece

			# Affichage
			if self.gamestate & (1 << 5):
				self.draw_on_squares([self.black_king.current_square], True)
			elif self.gamestate & (1 << 4):
				self.draw_on_squares([self.white_king.current_square], True)
			self.screen.blit(self.temp_board, self.temp_board.get_rect())
			for piece in self.pieces:
				self.screen.blit(piece.image,
				                 (piece.current_square[0] * self.tilesize,
				                  piece.current_square[1] * self.tilesize))
			pygame.display.update()
		self.print_gamestate()

	def parse_FEN(self, fen: str) -> tuple[list[Piece], int]:
		"""
		Construit les pièces comme décrit dans le FEN passé, et l'état actuel de la partie (roque, en-passant, nombre de coups)

		:param fen: La position sous forme de FEN
		:return: Le tuple contenant la liste des pièces et l'état de la partie
		"""
		pieces = []
		# De gauche à droite :
		# A qui de jouer : 1 noirs, 0 blancs
		# Echecs ? Noirs puis blancs
		# Roque coté reine puis roi, noirs puis blancs
		gamestate = 0b0001111

		# Un FEN a la structure suivante :
		# pieces/pieces/pieces/pieces prochain_joueur qui_peut_roquer_et_où case_pour_enpassant halfmove move_number
		split = fen.split(" ")
		lines = split[0].split("/")

		# Construction des pièces
		y = 0
		while y < 8:  # Vertical
			x = 0
			line: str = lines[y]
			if line.isnumeric():  # Il y a que des entiers, donc seulement un 8 cad ligne vide
				y += 1
				continue
			for char in line:  # Horizontal
				if char.isnumeric():
					# On doit sauter ce nombre de cases horizontalement
					x += int(char)
					continue
				# Si le caractère de la pièce est en minuscule, c'est une pièce noire, blache sinon
				# Et on construit la pièce correspondante
				piece = Piece.new_piece(int(char.islower()), PIECES[char.upper()], (x, y), self.tilesize)
				# On stocke les rois noirs et blancs, c'est pratique de les avoir dans des variables
				if type(piece) == King:
					if piece.color == NOIR:
						self.black_king = piece
					else:
						self.white_king = piece
				# On place la pièce sur l'échiquier
				self.board[y][x] = piece
				pieces.append(piece)
				# On l'ajoute également à la liste des pièces de même couleur
				if char.islower():
					self.black_pieces.append(piece)
				else:
					self.white_pieces.append(piece)
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
		# Mtn ça m'intéresse
		# En passant :
		if split[3] != '-':
			i, j = 0, 0
			sp = list(split[3])  # On sépare caractère par caractère
			for char in sp:
				char: str
				if char.isnumeric():  # C'est la ligne, donc y
					j = 8 - int(char)
				else:  # Lettre donc colonne
					# Attention, les y sont vers le bas dans pygame !
					i = ord(char) - ord('a')
			self.en_passant_square = (i, j)

		# Reste le nombre de coups à traiter

		self.halfmove = int(split[4])

		self.movecount = int(split[5])

		return pieces, gamestate

	def draw_on_squares(self, squares: list[tuple[int, int]], check: bool = False) -> None:
		# for x, y in squares:
		#     pygame.draw.rect(self.temp_board, RED,
		#                      pygame.Rect(x * self.tilesize, y * self.tilesize, self.tilesize, self.tilesize))
		for x, y in squares:
			if self.board[y][x] != VIDE:
				if not check:
					self.temp_board.blit(self.capture_piece_image, (self.tilesize * x, self.tilesize * y))
				else:
					self.temp_board.blit(self.check_image, (self.tilesize * x, self.tilesize * y))
			else:
				self.temp_board.blit(self.move_image, (self.tilesize * x, self.tilesize * y))

	def is_in_check(self, position: tuple[int, int], color: int, ennemy_pieces: list[Piece]) -> bool:
		"""
		Vérifie si une case particulière de l'échiquier est en prise par l'autre couleur.
		La case peut être déjà occupée par une pièce de la couleur attaquante, dans le cas d'une capture.

		:param position: La case de l'échiquier à vérifier
		:param color: La couleur de la pièce à la position
		:param ennemy_pieces: La liste des pièces ennemies
		:return:
		"""
		x, y = position
		# On sauvegarde l'éventuelle pièce ennemie/alliée à la position passée
		current = self.board[y][x]
		# On place une pièce potentielle de la couleur attaquée à la position
		self.board[y][x] = Potential(color, position)
		if current in ennemy_pieces:
			# On retire la pièce sauvegardée des attaquants, pour ne pas fausser l'évaluation dans le cas d'une prise
			ennemy_pieces.remove(current)
		in_check = []
		for piece in ennemy_pieces:
			# Si on a trouvé avant de processer toutes les pièces ennemies, pas besoin de continuer
			if position in in_check:
				# On replace ce que l'on a remplacé
				self.board[y][x] = current
				if current and current.color != color:  # Si current == piece.VIDE (0), on le rajoute pas
					ennemy_pieces.append(current)
				return True
			# Le roi ne peut pas mettre en échec l'autre roi, pas besoin de vérifier.
			in_check.extend(piece.generate_moves_for_piece(piece.color, piece.current_square, self.board, True))
		# On replace la pièce initialement à la position
		self.board[y][x] = current
		if current and current.color != color:  # Si current == piece.VIDE (0), on le rajoute pas
			ennemy_pieces.append(current)
		return position in in_check

	def is_checkmate(self, color: int) -> bool:
		"""
		Vérifie si le roi de la couleur fournie est actuellement en échec et mat.

		:param color: La couleur attaquée
		:return: Si le roi est en échec et mat
		"""
		# On suppose que le roi est déja en échec
		king = self.black_king if color == NOIR else self.white_king
		ennemy_pieces = self.white_pieces.copy() if color == NOIR else self.black_pieces.copy()
		# On génère la liste des déplacements possibles du roi, auxquels on enlève ceux qui le mettent en échec.
		king_moves = self.legal_king_moves(king, ennemy_pieces, king.generate_all_moves(self.board))
		if king_moves:
			# Si le roi peut bouger, pas besoin de vérifier plus.
			return False
		# Le roi peut pas bouger, le seul moyen de pas etre en échec est de bouger une pièce
		pieces = self.white_pieces if color == BLANC else self.black_pieces
		for piece in pieces:
			# On sait déjà que le roi ne peut pas bouger
			if isinstance(piece, King):
				continue
			# noinspection PyTypeChecker
			if self.generate_legal_moves(piece, piece.generate_all_moves(self.board)):
				return False
		return True

	def generate_legal_moves(self, piece, pseudolegal_moves: list[tuple[int, int]]) -> list[tuple[int, int]]:
		"""
		Génère, à partir de la liste des déplacements pseudo-légaux d'une pièce (autre que le roi), la liste de ses déplacements légaux.
		Un déplacement est légal si il ne met ou laisse pas le roi en échec.

		:param piece: La pièce concernée
		:param pseudolegal_moves: La liste de ses déplacements pseudo-légaux, cad sans tenir compte des échecs/clouages etc
		:return: La liste (éventuellement vide) des déplacements possible
		"""
		legal = []
		king = self.black_king if piece.color == NOIR else self.white_king
		ennemy_pieces = self.white_pieces.copy() if piece.color == NOIR else self.black_pieces.copy()
		# On retire la pièce de sa case actuelle, puisqu'elle va se déplacer
		self.board[piece.current_square[1]][piece.current_square[0]] = VIDE

		for position in pseudolegal_moves:
			(x, y) = position
			# On sauvegarde la pièce actuellement sur la case.
			current = self.board[y][x]
			# On y place une pièce temporaire de la couleur de la pièce se déplaçant.
			self.board[y][x] = Potential(piece.color, position)
			if current in ennemy_pieces:
				# On retire l'éventuelle pièce prise des pièces ennemies pour ne pas fausser l'évaluation.
				ennemy_pieces.remove(current)
			# Si le roi n'est pas en échec après le déplacement, il est légal
			if not self.is_in_check(king.current_square, piece.color, ennemy_pieces):
				legal.append(position)
			# On replace la pièce sauvegardée
			self.board[y][x] = current
			if current:  # Si current == piece.VIDE (0), on le rajoute pas
				ennemy_pieces.append(current)
		# Enfin, on replace la pièce déplacée
		self.board[piece.current_square[1]][piece.current_square[0]] = piece
		return legal

	def print_board(self):
		for line in self.board:
			print(line)

	def print_gamestate(self):
		print("Au tour des " + ("noirs" if self.gamestate >> 6 else "blancs"))
		if (self.gamestate >> 5) & 1:
			print("Les noirs sont en échec")
		elif (self.gamestate >> 4) & 1:
			print("Les blancs sont en échec")
		print("Les noirs peuvent roquer :" + " coté dame" * ((self.gamestate >> 3) & 1) +
		      " coté roi" * ((self.gamestate >> 2) & 1))
		print("Les blancs peuvent roquer :" + " coté dame" * ((self.gamestate >> 1) & 1) +
		      " coté roi" * (self.gamestate & 1))
		print(self.moves)
		print("Nombre de coups :", self.movecount)
		print("Evaluation de la position :", self.evaluation)

	def move_piece(self, piece: Piece, new_pos: tuple[int, int]) -> None:
		"""
		Déplace une pièce du plateau à une nouvelle position, en mettant à jour sa position interne

		:param piece: La pièce de l'échiquier à déplacer
		:param new_pos: Sa nouvelle position
		"""
		(oldx, oldy), (newx, newy) = piece.current_square, new_pos
		self.board[oldy][oldx] = VIDE
		self.board[newy][newx] = piece
		piece.current_square = (newx, newy)

	def calculate_evaluation(self) -> None:
		"""
		Calcule l'évaluation de la position en terme de matériel, sans prendre en compte l'activité des pièces
		"""
		self.white_material_count = sum(p.worth for p in self.white_pieces)
		self.black_material_count = sum(p.worth for p in self.black_pieces)
		self.evaluation = self.white_material_count - self.black_material_count if not self.stalemate else 0

	def is_stalemate(self, color: int) -> bool:
		"""
		Vérifie si le joueur donné est pat, c'est-à-dire s'il ne lui reste plus de mouvements légaux sans être en échec.

		:param color: Le joueur concerné
		:return: Si il y a pat
		"""
		# On part du principe que le roi n'est pas en échec.
		# On peut utiliser la même logique que dans la vérification d'échec et mat, mais sans que le roi soit en échec.
		return self.is_checkmate(color)

	def legal_king_moves(self, king: Piece, ennemy_pieces: list[Piece], pseudolegal_moves: list[tuple[int, int]]) -> \
			list[tuple[int, int]]:
		"""
		Génère la liste des déplacements légaux du roi (sans compter le roque), en enlevant les déplacements qui le mettraient en échec.

		:param king: Le roi concerné
		:param ennemy_pieces: La liste des pièces ennemies
		:param pseudolegal_moves: Les déplacements pseudo-légaux
		:return: La liste des déplacements légaux du roi
		"""
		# On retire le roi de sa case actuelle pour qu'il ne fausse pas l'évaluation des échecs
		x, y = king.current_square
		self.board[y][x] = VIDE
		# On enleve les cases où le roi est en échec
		legal_moves = list(
				filter(lambda position: (
						not self.is_in_check(position, king.color, ennemy_pieces)),
				       pseudolegal_moves))
		# On remet le roi
		self.board[y][x] = king

		# Si le roi peut roquer et qu'il n'est pas en échec
		if (king == self.white_king and (self.gamestate & 0b11) and not (self.gamestate & 0b0010000)) or \
				(king == self.black_king and ((self.gamestate >> 2) & 0b11) and not (self.gamestate & 0b0100000)):
			state = ((self.gamestate >> 2) & 0b11) if king == self.black_king else (
					self.gamestate & 0b11)
			queenside, kingside = king.can_castle(king.current_square,
			                                      self.board, state)
			kingx, kingy = king.current_square
			# On vérifie que le roi ne traverse pas d'échecs et que la destination n'est pas en échec
			if queenside:
				if (kingx - 1, kingy) in legal_moves and not self.is_in_check((kingx - 2, kingy),
				                                                              king.color,
				                                                              ennemy_pieces):
					legal_moves.append((kingx - 2, kingy))
			if kingside:
				if (kingx + 1, kingy) in legal_moves and not self.is_in_check((kingx + 2, kingy),
				                                                              king.color,
				                                                              ennemy_pieces):
					legal_moves.append((kingx + 2, kingy))
		return legal_moves

	def promote_pawn(self, pawn: Piece, gui_choice: bool = True, choice=Queen):
		x, y = pawn.current_square
		if (pawn.color == BLANC and y == 0) or (pawn.color == NOIR and y == 7):
			if gui_choice:
				new_piece = choicebox("What do you want to promote to ?",
				                      choices=["Queen", "Rook", "Bishop", "Knight"])
				if new_piece is None:  # Le joueur a cliqué "Cancel", donc par défaut on fait une dame
					promoted = Queen(pawn.color, (x, y), self.tilesize)
				else:
					promoted = Piece.new_piece(pawn.color, PIECES[new_piece], (x, y),
					                           self.tilesize)
			else:
				promoted = choice(pawn.color, (x, y), self.tilesize)
			self.pieces.remove(pawn)
			self.pieces.append(promoted)
			if promoted.color == BLANC:
				self.white_pieces.remove(pawn)
				self.white_pieces.append(promoted)
			else:
				self.black_pieces.remove(pawn)
				self.black_pieces.append(promoted)
			self.board[y][x] = promoted
			return promoted
		return None

	def handle_keys(self, event: pygame.event.Event):
		if event.key == pygame.K_q:
			self.print_board()
		elif event.key == pygame.K_g:
			self.print_gamestate()
		elif event.key == pygame.K_ESCAPE:
			self.running = False
		elif event.key == pygame.K_LEFT:
			if self.moves:
				# On change le joueur
				self.gamestate ^= (1 << 6)
				last_move = self.moves.pop()
				self.travelled_moves.append(last_move)

				piece = last_move.piece

				self.move_piece(piece, last_move.orig)
				if last_move.taken:
					x, y = last_move.to
					self.board[y][x] = last_move.taken
					self.pieces.append(last_move.taken)
					(self.black_pieces if piece.color == BLANC else self.white_pieces).append(last_move.taken)

				if last_move.promote:
					self.pieces.remove(last_move.promote)
					self.pieces.append(last_move.piece)
					(self.black_pieces if piece.color == NOIR else self.white_pieces).remove(last_move.promote)
					(self.black_pieces if piece.color == NOIR else self.white_pieces).append(piece)

				if last_move.castle is not None:
					x, y = last_move.to
					# Queenside
					if last_move.castle:
						self.move_piece(self.board[y][x + 1], (x - 2, y))
					else:
						self.move_piece(self.board[y][x - 1], (x + 1, y))

				self.temp_board = self.board_surface.copy()

				self.gamestate = last_move.old_gamestate

			# self.saved_gamestate = self.gamestate
			# self.saved_pieces = self.pieces.copy()
			# self.saved_board = [line.copy() for line in self.board]

		elif event.key == pygame.K_RIGHT:
			if self.travelled_moves:
				# 	self.gamestate = self.saved_gamestate
				# 	self.pieces = self.saved_pieces.copy()
				# 	self.board = [line.copy() for line in self.saved_board]
				# 	self.black_pieces = [piece for piece in self.pieces if piece.color == NOIR]
				# 	self.white_pieces = [piece for piece in self.pieces if piece.color == BLANC]

				self.gamestate ^= (1 << 6)
				last_move = self.travelled_moves.pop()
				piece = last_move.piece
				self.moves.append(last_move)

				self.move_piece(piece, last_move.to)

				if last_move.taken:
					self.pieces.remove(last_move.taken)
					(self.white_pieces if piece.color == NOIR else self.black_pieces).remove(last_move.taken)

				if last_move.promote:
					self.pieces.append(last_move.promote)
					self.pieces.remove(piece)
					(self.black_pieces if piece.color == NOIR else self.white_pieces).append(last_move.promote)
					(self.black_pieces if piece.color == NOIR else self.white_pieces).remove(piece)

				if last_move.castle is not None:
					x, y = last_move.to
					# Queenside
					if last_move.castle:
						self.move_piece(self.board[y][x - 2], (x + 1, y))
					else:
						self.move_piece(self.board[y][x + 1], (x - 1, y))

				self.gamestate = last_move.new_gamestate
