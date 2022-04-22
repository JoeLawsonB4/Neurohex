from __future__ import absolute_import
from __future__ import print_function
import sys
sys.path.append("..")
from inputFormat import state_string
from preprocess import preprocess
"""
Visual check that preprocessing stage is working correctly.
"""


pos = preprocess("../data/raw_games_small.dat", trim_final=False)

for p in pos:
	print(p)