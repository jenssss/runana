#!/usr/bin/env python
from __future__ import print_function

from runana import analyse
from runana import analyse_pandas
from runana import read_numbers


def run_analysis(workdir):
    print(workdir)

    dict_w_parameters = analyse.read_input_files(workdir)

    dict_w_parameters.diff()
    analyse_co_iterating_vars(dict_w_parameters)


def analyse_co_iterating_vars(dict_w_parameters):
    panda_data = analyse_pandas.make_a_seq_panda(dict_w_parameters)
    print(panda_data)
    
    changedsparams = analyse.ChangedParams(dict_w_parameters)
    from pprint import pprint
    pprint(changedsparams)
    varvals, pairs = changedsparams.groupby_varname()
    print("pairs")
    pprint(pairs)
    connected = analyse.find_connected_components(pairs)
    print("connected")
    pprint(connected)
    # pprint(varvals)
    double_var = dict((key, list_) for key, list_ in connected.items() if len(key) == 2)
    print("double_var")
    pprint(double_var)

    double_pandas = analyse_pandas.import_from_double_var(double_var, varvals)
    double_var_vectors = analyse_pandas.double_var_vectors(double_var, varvals)
    from runana import matplotlib_managers as mplm
    pattern = 'Integral'
    read_var = analyse.make_collector_function(workdir, read_numbers.
                                               read_last_number_from_file,
                                               fname='integrate_test.py.stdout',
                                               pattern=pattern)
    for namevals, double_panda  in analyse_pandas.double_var_iter(double_pandas):
        print(double_panda)
        print(double_panda.applymap(read_var))

    with mplm.plot_manager('double_var_test.pdf') as pp:
        for namevals, (x, y, dirs) in analyse_pandas.double_var_iter(double_var_vectors):
            with mplm.single_ax_manager(pp) as ax:
                z = list(map(read_var,dirs))
                ax.tripcolor(x, y, z)
                # ax[1].tricontourf(x,y,z, 20)
                ax.plot(x, y, 'ko ')
                ax.set_xlabel(namevals[0][1])
                ax.set_ylabel(namevals[1][1])


if __name__ == "__main__":
    with open('latest_run_dir.txt') as file_:
        workdir = file_.read()
    run_analysis(workdir=workdir)
