from os import path

import pygame

BLANC = 0
NOIR = 1
ROI = 1 << 5
REINE = 1 << 4
TOUR = 1 << 3
FOU = 1 << 2
CAVALIER = 1 << 1
PION = 1
VIDE = 0

PIECES = {
		"P": PION,
		"Pawn": PION,
		"N": CAVALIER,
		"Knight": CAVALIER,
		"B": FOU,
		"Bishop": FOU,
		"R": TOUR,
		"Rook": TOUR,
		"Q": REINE,
		"Queen": REINE,
		"K": ROI,
		"King": ROI
}


class Piece(pygame.sprite.Sprite):
	def __init__(self, tilesize: int = None, name: str = None, piece_name: str = None):
		super(Piece, self).__init__()
		self.current_square: tuple[int, int] = (-1, -1)
		self.name = name
		self.piece_name = piece_name
		if name is not None and tilesize is not None and piece_name is not None:
			self.image = pygame.transform.smoothscale(pygame.image.load(path.join("resources",
		                                                                      self.name)),
		                                          (tilesize, tilesize))
			self.rect = self.image.get_rect()

	@staticmethod
	def new_piece(color: int, piece_type: int, position: tuple[int, int], tilesize: int):
		if piece_type == ROI:
			return King(color, position, tilesize)
		if piece_type == REINE:
			return Queen(color, position, tilesize)
		if piece_type == TOUR:
			return Rook(color, position, tilesize)
		if piece_type == CAVALIER:
			return Knight(color, position, tilesize)
		if piece_type == FOU:
			return Bishop(color, position, tilesize)
		if piece_type == PION:
			return Pawn(color, position, tilesize)

	def __repr__(self):
		return f"{self.piece_name} at {self.current_square}"

	def generate_all_moves(self, board) -> list[tuple[int, int]]:
		# A override par les subclass
		pass

	@staticmethod
	def generate_moves_for_piece(color: int, position: tuple[int, int], board, only_captures: bool = False) -> list[tuple[int, int]]:
		pass


# On importe � la fin pour �viter les probl�mes d'importation circulaire
from pieces.king import King
from pieces.queen import Queen
from pieces.rook import Rook
from pieces.bishop import Bishop
from pieces.knight import Knight
from pieces.pawn import Pawn
from pieces.potential import Potential
