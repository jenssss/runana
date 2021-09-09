===============================================
Runana - Run programs and analyse their results
===============================================

Utility library for running programs and analysing their results.

Useful for convergence testing. Integrates well with Fortran programs.

Documentation: http://runana.readthedocs.org/en/latest/

Installation
============

``runana`` can be installed from pypi::

   $ pip install runana

The latest version of ``runana`` can be installed from source::

   $ git clone https://github.com/jenssss/runana.git
   $ cd runana
   $ python setup.py install

Users without install privileges can append the ``--user`` flag to
``setup.py``::

   $ python setup.py install --user


Example usage
=============

A number of examples are included in the ``examples`` directory of the
source code. The subfolder ``f90nml`` uses configuration files in the
fortran namelist format, while ``upname`` uses a configuration name format
in which the names and values of variables are given on consequtive
lines with entries seperated by white space.

Here follows one of the examples from the ``f90nml`` folder. A simple
program for performing a numerical integration is given in
``examples/f90nml/integrate_test.py``. The main content of this file is::

  #!/usr/bin/env python
  from sys import argv
  import numpy as np
  import f90nml

  config = f90nml.read(argv[1])

  npoints = config['nlIntegrate']['npoints']

  x = np.linspace(0, 2, npoints)
  y = 10*x**2

  I = np.trapz(y, x)

  print('Integral of 10*x**2 from 0 to 2: ', I)

The program can be configured through a namelist configuration, which
should be given as the first argument when calling the program
``./intergrate_test.py config.nml``. An example of such a configuration
is located at ``examples/f90nml/config.nml`` and contains entries of the
form::

  &nlGroup
    var = 1
  &end

  &nlIntegrate
    npoints = 10
  &end

We want to run this program for a number of different values of the
``npoints`` parameter, and compare the results. For this we can use
``runana``. The file ``examples/f90nml/run_integrate.py`` contains a
script showing how this can be run::

  from os import path, getcwd
  from runana.run import execute, print_time, generate_list
  
  def setup_programs():
      programs = ['integrate_test.py',]
      programs = [path.join(getcwd(), program) for program in programs]
      return programs
 
  def setup_replacers():
      nvar_values = 10
      chain_iters = {('nlIntegrate', 'npoints'): generate_list(
          start=10, incr=10, incr_func='add', nvalues=nvar_values),
      }
      return chain_iters
  
  input_file = 'config.nml'
      
  chain_iters = setup_replacers()
      
  scratch_base = path.expanduser('~/test_run/runana/integrate_test')
      
  programs = setup_programs()
  
  print('Running in ', scratch_base)
  
  with print_time():
      execute(programs, input_file, scratch_base,
              chain_iters=chain_iters)
  
Running this script will run the integration program with 10 values of
the ``npoints`` parameter in increments of 10 starting from 10. The
results of the calculations will be stored in
``~/test_run/runana/integrate_test``, specified in the ``scratch_base``
variable. For each parameter, a seperate run of the program will be
performed, and the results stored in separate subdirectories of
``~/test_run/runana/integrate_test``. This script can be run by running
``python run_integrate.py`` in the ``examples/f90nml/`` directory.

Finally, the results can be analyzed using the script in
``examples/f90nml/analyse_integrate.py``, which contains::

  from os import path
  from runana import analyse
  from runana import analyse_pandas
  from runana import read_numbers

  workdir = path.expanduser('~/test_run/runana/integrate_test')

  params_to_dirs = analyse.read_input_files(workdir)

  params_to_dirs.diff()

  panda_data = analyse_pandas.make_a_seq_panda(params_to_dirs)

  read_var = analyse.make_collector_function(
        workdir,
        read_numbers.read_last_number_from_file,
        fname="integrate_test.py.stdout",
        pattern="Integral",
    )
  panda_var = panda_data.applymap(read_var)
  print("Values of integral")
  print(panda_var)

  panda_conv = panda_var.calc_convergence()
  print("Estimated difference between current and fully converged value")
  print(panda_conv)
  param_panda = panda_data.applymap(
        analyse_pandas.return_dict_element(params_to_dirs)
	)
  panda_var.plot_("plot_test_integral_var.pdf", param_panda=param_panda)
  panda_conv.plot_("plot_test_integral_conv.pdf", logy=True, param_panda=param_panda)

Running this script should print out::

  Values of integral:
                                0
  NumParam NumParamValue           
  npoints  10.0           26.831276
           20.0           26.703601
           30.0           26.682521
           40.0           26.675433
           50.0           26.672220
           60.0           26.670497
           70.0           26.669467
           80.0           26.668803
           90.0           26.668350
           100.0          26.668027

  Estimated difference between current and fully converged value:
                            0_conv
  NumParam NumParamValue          
  npoints  10.0                NaN
           20.0           0.009562
           30.0           0.002370
           40.0           0.001063
           50.0           0.000602
           60.0           0.000388
           70.0           0.000270
           80.0           0.000199
           90.0           0.000153
           100.0          0.000121
  
The script collects the values calculated by the integration program and
puts them into a pandas ``DataFrame``, indexed by the value of the
varying numerical parameter. It also calculates an estimate for how well
converged the calculation is. Finally the script plots these values to the files
``plot_test_integral_var.pdf`` and ``plot_test_integral_conv.pdf``.


Similar software
================

https://github.com/ioam/lancet

   
