#!/usr/bin/python
from sys import argv
import f90nml

config = f90nml.read(argv[1])

print(config['nlGroup']['variable'])
print(config['nlGroup2']['other_variable'])

import time
import random
wait = 0.1
time.sleep(wait+0.1*random.random())
