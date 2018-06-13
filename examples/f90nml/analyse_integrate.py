from __future__ import print_function

from runana import analyse
from runana import analyse_pandas
from runana import read_numbers


def run_analysis(workdir):
    print(workdir)

    dict_w_parameters = analyse.read_input_files(workdir)

    dict_w_parameters.diff()

    changedsparams = analyse.ChangedParams(dict_w_parameters)
    varvals, pairs = changedsparams.identify_pairs()
    connected = analyse.find_connected_components(pairs)
    # pprint(varvals)
    double_var = dict((key, list_) for key, list_ in connected.items() if len(key) == 2)
    from pprint import pprint
    pprint(double_var)

    double_pandas = analyse_pandas.import_from_double_var(double_var, varvals)
    double_var_vectors = analyse_pandas.double_var_vectors(double_var, varvals)
    from runana import matplotlib_managers as mplm
    pattern = 'Integral'
    read_var = analyse.make_collector_function(workdir, read_numbers.
                                               read_last_number_from_file,
                                               fname='integrate.stdout',
                                               pattern=pattern)
    for namevals, double_panda  in analyse_pandas.double_var_iter(double_pandas):
        print(double_panda.applymap(read_var))

    with mplm.plot_manager('double_var_test.pdf') as pp:
        for namevals, (x, y, dirs) in analyse_pandas.double_var_iter(double_var_vectors):
            with mplm.single_ax_manager(pp) as ax:
                z = list(map(read_var,dirs))
                ax.tripcolor(x, y, z)
                # ax[1].tricontourf(x,y,z, 20) # choose 20 contour levels, just to show how good its interpolation is
                ax.plot(x, y, 'ko ')
                ax.set_xlabel(namevals[0][1])
                ax.set_ylabel(namevals[1][1])

    # raise SystemExit

    seqs = analyse.Seqs(dict_w_parameters)

    panda_data = analyse_pandas.SeqsDataFrame().import_from_seq(seqs)
    print(panda_data)

    for pattern in ['Integral']:
        panda_var = panda_data.applymap(read_var)
        print(panda_var)

        panda_conv = panda_var.calc_convergence()
        # print(panda_conv)
        param_panda = panda_data.applymap(analyse_pandas.
                                          return_dict_element(dict_w_parameters))
        # panda_var.plot(,'plot_test_'+pattern+'.pdf',
        #                      logy=False, param_panda=param_panda)
        panda_conv.plot_('plot_test_'+pattern+'.pdf',
                         logy=True, param_panda=param_panda)


if (__name__ == "__main__"):
    with open('latest_run_dir.txt') as file_:
        workdir = file_.read()
    run_analysis(
        workdir=workdir
    )
