#!/usr/bin/python
from __future__ import print_function
from os import path, getcwd

from runana import run

scratch_base = path.expanduser('~/test_run/runana/test_upname')

nvar_values = 3
some_iters = {'variable': run.generate_list(
    start=1, incr=1, incr_func='add', nvalues=nvar_values),
              #  'third_variable': ['a','b','c']
}

product_iters = {}
chain_iters = some_iters
just_replace = {'other_variable': -3.0}
just_replace = {}

# chain_iters, just_replace = run.common_start(chain_iters, just_replace)

input_file = 'config.inp'

programs = ['example_program.py',]
programs = [path.join(getcwd(), program) for program in programs]

print('Running in ', scratch_base)

with run.print_time():
    run.execute(programs, input_file, scratch_base, chain_iters=chain_iters, product_iters=product_iters, just_replace=just_replace, filter_func='upname')

just_replace = {'other_variable': -3.0}
nvar_values = 4
some_iters = {'variable': run.generate_list(
    start=1, incr=1, incr_func='add', nvalues=nvar_values),}
chain_iters = some_iters
with run.print_time():
    run.execute(programs, input_file, scratch_base, chain_iters=chain_iters, product_iters=product_iters, just_replace=just_replace, filter_func='upname')

    
with open('latest_run_dir.txt','w') as file_:
    file_.write(scratch_base)

import analyse
analyse.run_analysis(scratch_base)
    
