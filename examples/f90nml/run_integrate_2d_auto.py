#!/usr/bin/python
from __future__ import print_function
from os import path, getcwd

from runana import run

scratch_base = path.expanduser('~/test_run/runana/integrate_2d_test_auto')

nvar_values = 20
some_iters = {('nlIntegrate2', 'npointsx'): run.generate_list(
    start=10, incr=50, incr_func='add', nvalues=nvar_values),
              # ('nlGroup2', 'third_variable'): ['a','b','c']
}
some_iters[('nlIntegrate2', 'npointsy')] = run.generate_list(10, 50, nvalues=nvar_values)

product_iters = {}
chain_iters = some_iters
just_replace = {}

input_file = 'config.nml'

programs = ['integrate_2d_test.py',]
programs = [path.join(getcwd(), program) for program in programs]

print('Running in ', scratch_base)
from runana import read_numbers
from functools import partial
read_func = partial(read_numbers.read_last_number_from_file,
                    fname='integrate.stdout',pattern='Integral')
conv_crit = run.ConvCrit(read_func,eps=1e-3)

with run.print_time():
    run.auto_conv_rerun(run.auto_conv)(programs, input_file, scratch_base, conv_crit, chain_iters=chain_iters, product_iters=product_iters, just_replace=just_replace)
    
with open('latest_run_dir.txt','w') as file_:
    file_.write(scratch_base)
