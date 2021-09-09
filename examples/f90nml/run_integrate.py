#!/usr/bin/env python
from __future__ import print_function
from os import path, getcwd

from runana.run import execute, print_time, generate_list


def main():
    input_file = 'config.nml'
    
    chain_iters = setup_replacers()
    
    scratch_base = path.expanduser('~/test_run/runana/integrate_test')
    
    programs = setup_programs()

    print('Running in ', scratch_base)

    with print_time():
        execute(programs, input_file, scratch_base,
                    chain_iters=chain_iters)

    with open('latest_run_dir.txt','w') as file_:
        file_.write(scratch_base)


def setup_programs():
    programs = ['integrate_test.py',]
    programs = [path.join(getcwd(), program) for program in programs]
    return programs


def setup_replacers():
    nvar_values = 10
    chain_iters = {('nlIntegrate', 'npoints'): generate_list(
        start=10, incr=10, incr_func='add', nvalues=nvar_values),
                  # ('nlGroup2', 'third_variable'): ['a','b','c']
    }
    return chain_iters


if __name__ == "__main__":
    main()
