#!/usr/bin/python
from sys import argv
import numpy as np
import f90nml

config = f90nml.read(argv[1])

npointsx = config['nlIntegrate2']['npointsx']
npointsy = config['nlIntegrate2']['npointsy']

x = np.linspace(0,2,npointsx)
y = np.linspace(0,2,npointsy)

X,Y = np.meshgrid(x,y)

f = np.sin(X**5+Y**3)+X-Y

I = np.trapz(np.trapz(f,Y,axis=0),x)

print('Integral of x**2+y**2 from 0 to 2: ',I)

