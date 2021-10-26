# encoding=latin-1

from os import path

import pygame

# Constantes utilisées
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
		self.worth = 0
		if name is not None and tilesize is not None and piece_name is not None:
			self.image = pygame.transform.smoothscale(pygame.image.load(path.join("resources",
		                                                                      self.name)),
		                                          (tilesize, tilesize))

	@staticmethod
	def new_piece(color: int, piece_type: int, position: tuple[int, int], tilesize: int):
		"""
		Créée et renvoit une pièce du type passé.

		:param color: La couleur de la pièce
		:param piece_type: Le type de la pièce
		:param position: La case de l'échiquier
		:param tilesize: La taille en pixels des cases, pour mettre l'image de la pièce à l'échelle
		:return: La pièce appropriée
		"""
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
		"""
		Génère la liste des déplacements pseudolégaux pour la pièce.
		A implémenter dans les sous-classes.

		:param board: L'état actuel de l'échiquier
		:return: La liste des déplacements pseudolégaux pour la pièce
		"""
		pass

	@staticmethod
	def generate_moves_for_piece(color: int, position: tuple[int, int], board, only_captures: bool = False) -> list[tuple[int, int]]:
		"""
		Génère la liste des déplacements pseudolégaux pour une pièce de la couleur et à la position passée.
		A implémenter dans les sous-classes.

		:param color: La couleur de la pièce
		:param position: La case actuelle de la pièce
		:param board: L'état actuel de l'échiquier
		:param only_captures: Si il ne faut générer que des captures, utilisé pour la détection d'échecs
		:return: La liste des déplacements pseudolégaux pour la pièce
		"""
		pass
	
	def get_positional_score(self, x: int, y: int) -> int:
		pass


# On importe à la fin pour éviter les problèmes d'importation circulaire
from pieces.king import King
from pieces.queen import Queen
from pieces.rook import Rook
from pieces.bishop import Bishop
from pieces.knight import Knight
from pieces.pawn import Pawn
