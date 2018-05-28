#!/usr/bin/python
from sys import argv
from runana.analyse import read_upname_file

config = read_upname_file(argv[1])

print(config['variable'])
print(config['other_variable'])

import time
import random
wait = 0.1
time.sleep(wait+0.1*random.random())
