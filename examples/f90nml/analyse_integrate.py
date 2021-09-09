#!/usr/bin/env python
from __future__ import print_function

from runana import analyse
from runana import analyse_pandas
from runana import read_numbers


def run_analysis(workdir):
    print(workdir)

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
    print("Values of integral:")
    print(panda_var)

    panda_conv = panda_var.calc_convergence()
    print()
    print("Estimated difference between current and fully converged value:")
    print(panda_conv)
    param_panda = panda_data.applymap(
        analyse_pandas.return_dict_element(params_to_dirs)
    )
    panda_var.plot_("plot_test_integral_var.pdf", param_panda=param_panda)
    panda_conv.plot_("plot_test_integral_conv.pdf", logy=True, param_panda=param_panda)


if __name__ == "__main__":
    with open("latest_run_dir.txt") as file_:
        workdir = file_.read()
    run_analysis(workdir=workdir)
