from __future__ import print_function

from runana import analyse
from runana import analyse_pandas
from runana import read_numbers
from runana import input_file_handling

def run_analysis(workdir):
    print(workdir)
    
    dict_w_parameters = analyse.read_input_files(workdir, read_func=input_file_handling.read_input_files_upname)

    dict_w_parameters.diff()
    
    seqs = analyse.Seqs(dict_w_parameters)
            
    panda_data = analyse_pandas.SeqsDataFrame().import_from_seq(seqs)

    read_var = analyse.make_collector_function(workdir,
                                               read_numbers.read_number_from_file,
                                               fname='example.stdout',inumber=1)
    
    panda_var = panda_data.applymap(read_var)
    print(panda_var)

    # panda_conv = analyse_pandas.calc_convergence(panda_var)
    # print(panda_conv)


    param_panda = panda_data.applymap(analyse_pandas.
                                      return_dict_element(dict_w_parameters))

    panda_var.plot_('plot_test.pdf',
                             logy=False, param_panda=param_panda)


            

if (__name__ == "__main__"):
    with open('latest_run_dir.txt') as file_:
        workdir = file_.read()
    run_analysis(
        workdir = workdir
    )
