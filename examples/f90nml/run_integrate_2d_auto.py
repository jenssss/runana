#!/usr/bin/python
from __future__ import print_function
from os import path, getcwd
from functools import partial

from runana import run
from runana import read_numbers

read_func = partial(read_numbers.read_last_number_from_file,
                    fname='integrate.stdout',pattern='Integral')
conv_crit = run.ConvCrit(read_func,eps=1e-3)

scratch_base = path.expanduser('~/test_run/runana/integrate_2d_test_auto')

nvar_values = 20
some_iters = {('nlIntegrate2', 'npointsx'): run.generate_list(
    start=10, incr=30, incr_func='add', nvalues=nvar_values),
}
some_iters[('nlIntegrate2', 'npointsy')] = run.generate_list(10, 30, nvalues=nvar_values)

chain_iters = some_iters

input_file = 'config.nml'

programs = ['integrate_2d_test.py',]
programs = [path.join(getcwd(), program) for program in programs]

print('Running in ', scratch_base)

with run.print_time():
    run.auto_conv_rerun(run.auto_conv)(programs, input_file, scratch_base, conv_crit, chain_iters=chain_iters)
    
with open('latest_run_dir.txt','w') as file_:
    file_.write(scratch_base)


import analyse_integrate
analyse_integrate.run_analysis(scratch_base)
    
