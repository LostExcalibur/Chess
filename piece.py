import pygame
from os import path


BLANC = 0
NOIR = 1
ROI = 1 << 5
REINE = 1 << 4
TOUR = 1 << 3
FOU = 1 << 2
CAVALIER = 1 << 1
PION = 1

PIECES = {
		"P": PION,
		"N": CAVALIER,
		"B": FOU,
		"R": TOUR,
		"Q": REINE,
		"K": ROI
}


class Piece(pygame.sprite.Sprite):
	def __init__(self, piece_type: int, color: int, tilesize: int, position: tuple[int, int] = None):
		"""
		7 bits
		0 - 5 dans l'ordre : pion cavalier fou tour dame roi
		6 : couleur, noir = 1 / blanc = 0
		"""
		super(Piece, self).__init__()
		self.info = color << 6 | piece_type
		self.name = ""
		self.build_name()
		self.image = pygame.transform.smoothscale(pygame.image.load(path.join("resources",
		                                                                      self.name)),
		                                          (tilesize, tilesize))
		self.rect = self.image.get_rect()
		self.current_square = position if position else (4, 7)

	def build_name(self):
		color = self.info >> 6
		piece_type = self.info & 0b111111
		self.name = "w" * (color == 0) + "b" * (color == 1)
		self.name += "P" * (piece_type == PION) + "N" * (piece_type == CAVALIER)
		self.name += "B" * (piece_type == FOU) + "R" * (piece_type == TOUR)
		self.name += "Q" * (piece_type == REINE) + "K" * (piece_type == ROI)
		self.name += ".png"
