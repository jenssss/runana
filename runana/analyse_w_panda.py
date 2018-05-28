#!/usr/bin/python
import pandas as pd

from runana.run import is_it_tuple
from runana.read_numbers import ignore_error


class SeqsDataFrame(pd.DataFrame):
    numparam = 'NumParam'
    numparamval = 'NumParamValue'
    @property
    def _constructor(self):
        return SeqsDataFrame

    def iterator(self):
        for numparam,data in self.iterator_outer():
            for column in data:
                dat = data[column]
                yield (numparam,column),dat

    def iterator_outer(self):
        for numparam in self.index.levels[0]:
            data = self.loc[(numparam)]
            data.sort_index(inplace=True)
            yield numparam,data
                
    def iterator_drop(self):
        for (numparam,column),dat in self.iterator():
            dat = dat.dropna()
            if not dat.empty:
                yield (numparam,column),dat

    def import_from_seq(self,seqs):
        """Converts the seqs object into a SeqsDataFrame"""
        multiindx = pd.MultiIndex(levels = [[], []],labels = [[], []],
                                  names = [self.numparam,self.numparamval])
        self.set_index(multiindx,inplace=True)
        for key,indx,seq_list in seqs.iterator():
            for numparamval in sorted(seq_list,key=try_to_float):
                run_index = seq_list[numparamval]
                numparam = is_it_tuple(key)
                self.loc[(numparam,numparamval),indx] = 0.1
                self.loc[(numparam,numparamval),indx] = run_index


def extract_interesting_vars(param_series,numparam):
    for column in param_series:
        paramdicts = param_series[column].dropna()
        if not paramdicts.empty:
            paramdict = paramdicts.iloc[0]
            for param_str in write_paramdict(paramdict,numparam):
                yield ''.join((str(column),': ',param_str))

def write_paramdict(paramdict,ignore=None, connector='='):
    for field in paramdict:
        if field!=ignore:
            yield ''.join((str(is_it_tuple(field)),connector,str(paramdict[field])))

                
def return_dict_element(dict_, error=KeyError):
    """ Returns a function that returns `dict_[arg]`, while ignoring `error`"""
    @ignore_error(error)
    def return_element(el):
        return dict_[el]
    return return_element
                
def try_to_float(str_):
    try:
        return float(str_)
    except ValueError:
        return str_
                
                    
def plot(plotdata, outfile, logx=False, logy=False, param_panda=None):
    """ Requires :mod:`numpy` and :mod:`matplotlib`"""
    from runana import matplotlib_managers as mplm
    import numpy as np
    with mplm.plot_manager(outfile=outfile) as pp:
        for numparam,data in plotdata.iterator_outer():
            with mplm.single_ax_manager(pp=pp) as ax:
                data.plot(ax=ax,alpha=0.8,marker='o')
                ax.set_xlabel(numparam)
                ax.legend(loc='best')
                if logx:
                    ax.set_xscale('log')
                if logy:
                    ax.set_yscale('log')
                    # ymin,ymax = ax.get_ylim()
                    ymin = np.nanmin(data.values)
                    ymax = np.nanmax(data.values)
                    ymin = np.power(10,np.floor(np.log10(ymin)))
                    ymax = np.power(10,np.ceil(np.log10(ymax)))
                    ax.set_ylim([ymin,ymax])

                if param_panda is not None:
                    param_series = param_panda.loc[(numparam)]
                    string = ' '.join(extract_interesting_vars(param_series,numparam))
                    ax.text(-0.1, 1.05, string, transform=ax.transAxes)

def calc_convergence(data_in):
    import numpy as np
    data_out = data_in.copy()
    columns = list(data_in.columns)
    data_out = data_out.drop(columns=columns)
    for (numparam,column),data in data_in.iterator():
        data = data.reset_index(level=data_in.numparamval)
        relDiff = data.diff()/data
        RelErrorEstimate = relDiff[column]/relDiff[data_in.numparamval]
        RelErrorEstimate = RelErrorEstimate.apply(np.abs)
        RelErrorEstimate = pd.Series(RelErrorEstimate.values,data[data_in.numparamval])
        for numparamval in data[data_in.numparamval]:
            data_out.loc[(numparam,numparamval),str(column)+'reldiff'] = RelErrorEstimate[numparamval]
    return data_out


