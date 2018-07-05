#!/usr/bin/python
from sys import argv
import numpy as np
import f90nml

config = f90nml.read(argv[1])

npointsx = config['nlIntegrate2']['npointsx']
npointsy = config['nlIntegrate2']['npointsy']
powerx = float(config['nlIntegrate2']['powerx'])

x = np.linspace(0,2,npointsx)
y = np.linspace(0,2,npointsy)

X,Y = np.meshgrid(x,y)

f = np.sin(X**powerx+Y**3)+X-Y

I = np.trapz(np.trapz(f,Y,axis=0),x)

print('Integral of sin(x**5+y**3)+x-y from 0 to 2: ',I)

