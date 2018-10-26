#!/usr/bin/python
from __future__ import print_function
from os import path, getcwd

from runana import run


def main():
    input_file = 'config.nml'

    scratch_base = path.expanduser('~/test_run/runana/test')

    just_replace, product_iters, chain_iters, co_iters = setup_replacers()

    programs = setup_programs()

    print('Running in ', scratch_base)

    with run.print_time():
        run.execute(programs, input_file, scratch_base,
                    chain_iters=chain_iters, product_iters=product_iters,
                    co_iters=co_iters, just_replace=just_replace)


def setup_programs():
    programs = ['example_program.py', ]
    programs = [path.join(getcwd(), program) for program in programs]
    return programs


def setup_replacers():
    nvar_values = 3
    some_iters = {('nlGroup', 'var'): run.generate_list(
        start=1, incr=1, incr_func='add', nvalues=nvar_values),
                  ('nlGroup2', 'varb'): [-3.0, -5, -10]
                  # ('nlGroup2', 'third_variable'): ['a','b','c']
    }

    product_iters = {}
    chain_iters = {}
    co_iters = {}
    # chain_iters = some_iters
    co_iters = some_iters
    just_replace = {('nlGroup2', 'varb'): -3.0}
    just_replace = {}
    from pprint import pprint
    pprint(some_iters)
    # chain_iters, just_replace = run.common_start(chain_iters, just_replace)
    return just_replace, product_iters, chain_iters, co_iters


if __name__ == "__main__":
    main()

# just_replace = {('nlGroup2', 'varb'): -3.0}
# nvar_values = 4
# some_iters = {('nlGroup', 'var'): run.generate_list(
#     start=1, incr=1, incr_func='add', nvalues=nvar_values),}
# chain_iters = some_iters
# with run.print_time():
#     run.execute(programs, input_file, scratch_base, chain_iters=chain_iters, product_iters=product_iters, just_replace=just_replace)
    
# with open('latest_run_dir.txt', 'w') as file_:
#     file_.write(scratch_base)

# import analyse
# analyse.run_analysis(scratch_base)
