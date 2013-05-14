__author__ = 'mactep'

# 0x68, 0x56, 0xF2
# 0x97, 0x59, 0xFC
# 0xB4, 0x5D, 0xE5
# 0xF2, 0x4C, 0xC4
# 0xEB, 0x5B, 0xFC

# 0x6B, 0x19, 0xFC
# 0x37, 0xDB, 0xC5
# 0x6F, 0x33, 0xA0
# 0x94, 0x36, 0xAB
# 0xDA, 0x4D, 0xDE

# 0x64, 0x48, 0xA4
# 0xD3, 0xD0, 0x6A
# 0xD4, 0x91, 0x61
# 0xD3, 0x6A, 0x88
# 0xA4, 0x98, 0xDE

# 0x8F, 0xB9, 0xD3
# 0x67, 0xD3, 0xDE
# 0xC7, 0xAE, 0xAB
# 0xF5, 0x7E, 0x9B
# 0x00, 0xCC, 0xF5
from PyQt4.QtGui import QColor

AMINO_COLORS = {}

class AAColors(object):
    def __init__(self):
        self.light_green = QColor(0x77, 0xdd, 0x88)
        self.green       = QColor(0x99, 0xee, 0x66)
        self.dark_green  = QColor(0x55, 0xbb, 0x33)
        self.blue        = QColor(0x66, 0xbb, 0xff)
        self.lilac       = QColor(0x99, 0x99, 0xff)
        self.dark_blue   = QColor(0x55, 0x55, 0xff)
        self.orange      = QColor(0xff, 0xcc, 0x77)
        self.pink        = QColor(0xee, 0xaa, 0xaa)
        self.red         = QColor(0xff, 0x44, 0x55)

ac = AAColors()

AMINO_COLORS["A"] = ac.light_green
AMINO_COLORS["G"] = ac.light_green

AMINO_COLORS["C"] = ac.green

AMINO_COLORS["D"] = ac.dark_green
AMINO_COLORS["E"] = ac.dark_green
AMINO_COLORS["N"] = ac.dark_green
AMINO_COLORS["Q"] = ac.dark_green

AMINO_COLORS["I"] = ac.blue
AMINO_COLORS["L"] = ac.blue
AMINO_COLORS["M"] = ac.blue
AMINO_COLORS["V"] = ac.blue

AMINO_COLORS["F"] = ac.lilac
AMINO_COLORS["W"] = ac.lilac
AMINO_COLORS["Y"] = ac.lilac

AMINO_COLORS["H"] = ac.dark_blue

AMINO_COLORS["K"] = ac.orange
AMINO_COLORS["R"] = ac.orange

AMINO_COLORS["P"] = ac.pink

AMINO_COLORS["S"] = ac.red
AMINO_COLORS["T"] = ac.red


