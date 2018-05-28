#!/usr/bin/python
from __future__ import print_function
from os import path, getcwd

from runana import run

scratch_base = path.expanduser('~/test_run/runana/integrate_test')

nvar_values = 10
some_iters = {('nlIntegrate', 'npoints'): run.generate_list(
    start=10, incr=10, incr_func='add', nvalues=nvar_values),
              # ('nlGroup2', 'third_variable'): ['a','b','c']
}

chain_iters = some_iters

input_file = 'config.nml'

programs = ['integrate_test.py',]
programs = [path.join(getcwd(), program) for program in programs]

print('Running in ', scratch_base)

with run.print_time():
    run.execute(programs, input_file, scratch_base, chain_iters=chain_iters)
    
with open('latest_run_dir.txt','w') as file_:
    file_.write(scratch_base)

import analyse_integrate
analyse_integrate.run_analysis(scratch_base)

    
