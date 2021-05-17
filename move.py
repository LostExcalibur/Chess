from dataclasses import dataclass
from piece import Piece
from pieces.pawn import Pawn


@dataclass(frozen=True, repr=False)
class Move:
    to: tuple[int, int]
    orig: tuple[int, int]
    piece: Piece
    old_gamestate: int
    new_gamestate: int
    taken: Piece = None
    # Castle = 0 si kingsidee, 1 si queenside, None sinon
    castle: int = None
    promote: Piece = None
    check: bool = False

    def __repr__(self):
        if self.castle is not None:
            return "O - O - O" if self.castle else "O - O"

        toret = ""
        if not isinstance(self.piece, Pawn):
            toret += self.piece.letter
        elif self.taken:
            toret += chr(ord('a') + self.orig[0])
            toret += str(8 - self.orig[1])

        toret += 'x' if self.taken else ''

        toret += chr(ord('a') + self.to[0])
        toret += str(8 - self.to[1])

        toret += "=" + self.promote.__repr__()[6] if self.promote else ''

        toret += '+' if self.check else ''

        return toret
