#!/usr/bin/env python
from sys import argv
import numpy as np
import f90nml

config = f90nml.read(argv[1])

npoints = config['nlIntegrate']['npoints']

x = np.linspace(0, 2, npoints)
y = x**2

I = np.trapz(y, x)

print('Integral of x**2 from 0 to 2: ', I)

import time
import random
wait = 0.1
time.sleep(wait+0.1*random.random())
