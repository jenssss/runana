from __future__ import print_function

from runana import analyse
from runana import analyse_w_panda
from runana import read_numbers

def run_analysis(workdir):
    print(workdir)
    
    dict_w_parameters = analyse.collect_from_all(workdir)

    analyse.dictdiff(dict_w_parameters)
    
    seqs = analyse.Seqs(dict_w_parameters)
    import pprint
    pprint.pprint(seqs)
            
    panda_data = analyse_w_panda.SeqsDataFrame()
    panda_data.import_from_seq(seqs)

    read_var = analyse.make_collector_function(workdir,read_numbers.read_number_from_file,
                                                fname='example.stdout',inumber=1)
    
    panda_var = panda_data.applymap(read_var)
    print(panda_var)

    # panda_conv = analyse_w_panda.calc_panda_convergence(panda_var)
    # print(panda_conv)


    param_panda = panda_data.applymap(analyse_w_panda.
                                      return_dict_element(dict_w_parameters))

    analyse_w_panda.plot(panda_var,'plot_test.pdf',
                             logy=False, param_panda=param_panda)

            

if (__name__ == "__main__"):
    with open('latest_run_dir.txt') as file_:
        workdir = file_.read()
    run_analysis(
        workdir = workdir
    )
