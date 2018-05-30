#!/usr/bin/python
import os
from os import path
from functools import partial, wraps

from runana.read_numbers import ignore_error
from runana.run import cwd
from runana.input_file_handling import read_input_files_f90nml, string_or_iterable, superset

try:
    basestring          # Python 2.x
except NameError:
    basestring = str    # Python 3.x
    
@ignore_error(TypeError,[])
def get_subdirs(a_dir):
    return [name for name in os.listdir(a_dir)
            if os.path.isdir(os.path.join(a_dir, name))]

def collecting_loop_recursive(dir_,read_func):
    subdirs = get_subdirs(dir_)
    for subdir in subdirs:
        asubdir = os.path.join(dir_,subdir)
        if os.path.exists(os.path.join(asubdir,'hostname.txt')):
            with cwd(asubdir):
                value = read_func()
            yield (subdir,),value
        else:
            for dirs,vals in collecting_loop_recursive(os.path.join(dir_,subdir),
                                                       read_func):
                yield (subdir,)+dirs,vals

def read_input_files(workdir,read_func=read_input_files_f90nml):
    """ Recursively searches through all subdirectories of `workdir`. `read_func` is run in any directory containing a file named 'hostname.txt', and the result is stored in a :class:`ParamDict`, with the path in tuple-form as key. This :class:`ParamDict` is returned. 

    Subdirectories of a directory with a 'hostname.txt' file are not searched.
    """
    paramdict = ParamDict()
    paramdict.read(workdir,read_func=read_func)
    return paramdict
                
class ParamDict(dict):
    """ Dictionary that holds dictionaries of parameters """
    def read(self,workdir,read_func=read_input_files_f90nml):
        for index,result in collecting_loop_recursive(workdir,read_func):
            self[index] = result

    def diff(self):
        """ Call :func:`dictdiff` on `ParamDict` object """
        dictdiff(self)

    def unpack_list_values(self):
        """ Takes any numerical parameter value in `ParamDict` object that is a list and
        packs it into individual slots with name numparam_name + idx

        Works in-place
        """
        for key,param_dict in self.items():
            spread_out_lists(param_dict)

def spread_out_lists(dict_):
    newdict = {}
    delete_keys = []
    for key,val in dict_.items():
        if isinstance(val,list):
            delete_keys += [key]
            for idx,elem in enumerate(val):
                if isinstance(key,tuple):
                    newkey = (key[0],str(key[1])+'_'+str(idx+1))
                else:
                    newkey = str(key)+'_'+str(idx+1)
                newdict[newkey] = elem
    dict_.update(newdict)
    for key in delete_keys:
        del dict_[key]
        
def make_collector_function(workdir,read_func,*args,**kwargs):
    """ Returns a function that runs `read_func(*args,**kwargs)` in the 
directory that is the join of `workdir` and the argument to the function"""
    return read_from_dir(roll_in_args(read_func,*args,**kwargs),workdir)

@ignore_error(TypeError)
def collect(dir_,read_func):
    """ Switches to `dir_` and runs `read_func`"""
    with cwd(dir_):
        return read_func()
    
def roll_in_args(read_func,*args,**kwargs):
    read_func_no_args = partial(read_func,*args,**kwargs)
    read_func_subdir = partial(collect,read_func=read_func_no_args)
    return read_func_subdir
def compose2(f, g):
    # @wraps(f)
    def fg(*a, **kw): return f(g(*a, **kw))
    return fg

    
@ignore_error(TypeError)
def join_dirs(subdirs,workdir):
    dir_ = os.path.join(workdir,
                        *tuple(string_or_iterable(subdirs)))
    return dir_
    
def prepend_dir(workdir):
    """ Returns a function that takes a tuple of directories and returns the 
combination of those into a path, with `workdir` prepended """
    return partial(join_dirs,workdir=workdir)

def read_from_dir(read_func,workdir):
    """ Composes `read_func` with :func:`prepend_dir(workdir)<prepend_dir>` """
    return compose2(read_func,prepend_dir(workdir))

    
class Seqs(dict):
    """ Seqeunces of related runs
    
    :param dict param_dicts: Dictionary containing dictionaries of parameters, in the form returned from e.g. :func:`collect_from_all`
    """
    def __init__(self,param_dicts,*args,**kwargs):
        super(Seqs, self).__init__(*args,**kwargs)
        keys = list(param_dicts.keys())
        for index in list(keys):
            del keys[0]
            for key,indices in get_indices_dict(index,param_dicts,keys).items():
                seqs_list = self.get(key,[])
                if all( not indices_sub(param_dicts,indices.values(),indices_seqs.values())
                        for indices_seqs in seqs_list):
                    self[key] = seqs_list + [indices]
                    
    def iterator(self):
        for key in self:
            for indx,seq_list in enumerate(self[key]):
                yield key,indx,seq_list

def catch_list_values(value,index):
    try:
        ret = {value:index}
    except TypeError:
        ret = {tuple(value):index}
    return ret

                
def get_indices_dict(index,param_dicts,keys):
    indices_dict = {}
    for index_compare in keys:
        for key,value,value_compare in get_index_for_all_but_one_changed(param_dicts[index],param_dicts[index_compare]):
            if key not in indices_dict:
                indices_dict[key] = catch_list_values(value,index)
            indices_dict[key].update(catch_list_values(value_compare,index_compare))
    return indices_dict
   
def get_index_for_all_but_one_changed(nl1,nl2):
    for key, value in nl1.items():
        try:
            value2 = nl2[key]
            if value != value2:
                if dict_eq_ignore(nl1,nl2,[key]): 
                    yield key, value, value2
        except KeyError:
            pass

def dict_eq_ignore(dict1,dict2,ignore_keys=[]):
    dict1_flat = copy_w_ignore_keys(dict1,ignore_keys)
    dict2_flat = copy_w_ignore_keys(dict2,ignore_keys)
    return dict1_flat == dict2_flat
def copy_w_ignore_keys(dict_,ignore_keys=[]):
    return dict((key,value) for key, value in dict_.items() if key not in ignore_keys)

def indices_sub(dicts,indices1,indices2):
    dict_list1 = list(dicts[indx] for indx in indices1)
    dict_list2 = list(dicts[indx] for indx in indices2)
    return issubset(dict_list2,dict_list1)

def issubset(list1,list2):
    """ Checks if list1 is subset of list2 """
    list3 = []
    for elem in list2:
        if elem in list1:
            list3.append(elem)
    return list2 == list3


# This function was inspired by nmltab
def dictdiff(alldicts):
    """ In-place removes all key:value pairs that are shared across all dicts 

    :param dict alldicts: a dictionary containing dictionaries"""
    superdict = superset(alldicts)
    for key in superdict:
        all_dicts_have_key = all((key in dict_) for dict_ in alldicts.values())
        if all_dicts_have_key:
            value_is_same = all((superdict[key] == dict_[key])
                                for dict_ in alldicts.values())
            if value_is_same:
                for dict_ in alldicts.values():
                    del dict_[key]
