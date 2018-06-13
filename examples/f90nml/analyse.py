from __future__ import print_function

from runana import analyse
from runana import analyse_pandas
from runana import read_numbers


def run_analysis(workdir):
    print(workdir)

    dict_w_parameters = analyse.read_input_files(workdir)

    dict_w_parameters.diff()

    seqs = analyse.Seqs(dict_w_parameters)
    from pprint import pprint
    pprint(seqs)

    changedsparams = analyse.ChangedParams(dict_w_parameters)
    varvals, pairs = changedsparams.identify_pairs()
    # pprint(changedsparams)
    # pprint(dict(((tuple(varname[1] for varname in key), list_) for key, list_ in varvals.items())))
    # pprint(dict(((tuple(varname[1] for varname in key), list_) for key, list_ in pairs.items())))

    connected = analyse.find_connected_components(pairs)
    # pprint(dict(((tuple(varname[1] for varname in key), list_) for key, list_ in connected.items())))

    pprint(varvals)
    double_var = dict((key, list_) for key, list_ in connected.items() if len(key) == 2)
    pprint(double_var)
    print(analyse_pandas.import_from_double_var(double_var, varvals))

    raise SystemExit

    seqs_new = dict((key, list_) for key, list_ in connected.items() if len(key) == 1)
    pprint(seqs_new)

    panda_data_new = analyse_pandas.SeqsDataFrame().import_from_seq_new(seqs_new, varvals)
    print(panda_data_new)

    panda_data = analyse_pandas.SeqsDataFrame().import_from_seq(seqs)
    print(panda_data)

    read_var = analyse.make_collector_function(workdir,read_numbers.read_number_from_file,
                                                fname='example.stdout',inumber=1)

    panda_var = panda_data.applymap(read_var)
    print(panda_var)

    # panda_conv = analyse_pandas.calc_panda_convergence(panda_var)
    # print(panda_conv)

    param_panda = panda_data.applymap(analyse_pandas.
                                      return_dict_element(dict_w_parameters))

    panda_var.plot_('plot_test.pdf',
                             logy=False, param_panda=param_panda)


if (__name__ == "__main__"):
    with open('latest_run_dir.txt') as file_:
        workdir = file_.read()
    run_analysis(
        workdir=workdir
    )
