import string
import numpy as np
import random, math
from numpy.linalg import solve as slv
from pylatex import (Document, NoEscape, SmallText, LargeText, MediumText, NewPage, Tabular, Alignat, Figure,
                     MultiColumn, MultiRow)
from pylatex.utils import bold
from random import *
from sympy import *
from sympy.plotting import plot
from skripteTests.skripte.funktionen import *
from skripteTests.skripte.plotten import *


a, b, c, d, e, f, g, h, x, y, z = symbols('a b c d e f g h x y z')
liste_teilaufg = list(string.ascii_lowercase)
nr_aufgabe = 0

