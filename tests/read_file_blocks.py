from runana.read_numbers import read_file_sev_blocks_new
# import sys
# sys.setrecursionlimit(50)
from pprint import pprint
blocks = read_file_sev_blocks_new('test3.dat')
print('')
pprint(blocks)

import numpy as np
nparray = np.asarray(blocks)
print( nparray)
print( nparray.shape)
