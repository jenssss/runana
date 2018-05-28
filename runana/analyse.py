#!/usr/bin/python
import os
from os import path
from functools import partial, wraps

import f90nml
from runana import read_numbers
from runana.run import cwd

try:
    basestring          # Python 2.x
except NameError:
    basestring = str    # Python 3.x

    
def string_or_iterable(args):
    """ Generator that assumes args is either a string or an iterable. """
    if isinstance(args, basestring):
        yield args
    else:
        for arg in args:
            yield arg

def num_str(s):
    """ Tries to convert input to integer, then tries float, then complex. 
If all these fails the string is returned unchanged"""
    try:
        return int(s)
    except ValueError:
        try:
            return float(s)
        except ValueError:
            try:
                return complex(s)
            except ValueError:
                return s

def read_upname_file(filename):
    """ Reads file in upname format

    In this format the names of variables are given on a line, with the values on the following line. Each variable/name should be seperated by at least two whitespaces or a tab. Each set of names/values lines should be seperated by at least one blank line
    """
    with open(filename,'r') as input_file_in:
        previous_line = []
        data={}
        for line in input_file_in:
            # Break line on tab or more than two consequtive whitespaces
            # line = split([r'\s{2,}'],line.rstrip())
            line = line.rstrip().replace('\t','  ').split('  ')
            line = [num_str(elem.strip()) for elem in line if elem]
            data.update(dict(zip(previous_line,line)))
            previous_line = line
    return data


def read_input_files_upname(patterns=['*.inp']):
    """ Read the all files matching `patterns` with :func:`read_upname_file`

    The data from all the files is supersetted and the resulting dict is returned"""
    from itertools import chain
    import glob
    filenames = list(chain(*(glob.glob(pattern)
                             for pattern in string_or_iterable(patterns))))
    dicts = dict((filename,read_upname_file(filename)) for filename in filenames)
    return superset(dicts)


def flat_iterator(nml):
    """Iterator that returns the adress of an element as a 2-tuple, 
    along with the element """
    for key, value in nml.items():
        for inner_key, inner_value in value.items():
            yield (key,inner_key), inner_value

def read_and_flatten_namelist(filename):
    namelist = f90nml.read(filename)
    return dict(flat_iterator(namelist))

def read_input_files_f90nml(patterns=['*.nml']):
    """ Read the all files matching `patterns` with :func:`f90nml.read`

    The namelists are flattened and supersetted, the resulting dict is returned"""
    from itertools import chain
    import glob
    filenames = list(chain(*(glob.glob(pattern)
                             for pattern in string_or_iterable(patterns))))
    dicts = dict((filename,read_and_flatten_namelist(filename)) for filename in filenames)
    return superset(dicts)

@read_numbers.ignore_error(TypeError,[])
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

def collect_from_all(workdir,read_func=read_input_files_f90nml):
    """ Recursively searches through all subdirectories of `workdir`. `read_func` is run in any directory containing a file named 'hostname.txt', and the result is stored in a dict, with the path in tuple-form as key. This dict is returned. 

    Subdirectories of a directory with a 'hostname.txt' file are not searched.
    """
    data={}
    for index,result in collecting_loop_recursive(workdir,read_func):
        data[index] = result
    return data

def make_collector_function(workdir,read_func,*args,**kwargs):
    """ Returns a function that runs `read_func(*args,**kwargs)` in the 
directory that is the join of `workdir` and the argument to the function"""
    return read_from_dir(roll_in_args(read_func,*args,**kwargs),workdir)

@read_numbers.ignore_error(TypeError)
def collect(dir_,read_func):
    """ Switches to `dir_` and runs `read_func`"""
    with cwd(dir_):
        return read_func()
    
def roll_in_args(read_func,*args,**kwargs):
    read_func_no_args = partial(read_func,*args,**kwargs)
    read_func_subdir = partial(collect,read_func=read_func_no_args)
    return read_func_subdir
def compose2(f, g):
    @wraps(f)
    def fg(*a, **kw): return f(g(*a, **kw))
    return fg

    
@read_numbers.ignore_error(TypeError)
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
    def __init__(self,param_dicts):
        for index,param_dict in param_dicts.items():
            indices_dict = {}
            for index_compare,param_dict_compare in param_dicts.items():
                for key,value,value_compare in get_index_for_all_but_one_changed(param_dict,param_dict_compare):
                    if not key in indices_dict:
                        indices_dict[key] = {value:index}
                    indices_dict[key][value_compare] = index_compare

            for key,indices in indices_dict.items():
                seqs_list = self.get(key,[])
                if all( not indices_eq(param_dicts,indices.values(),indices_seqs.values()) for indices_seqs in seqs_list):
                    self[key] = seqs_list + [indices]

    def iterator(self):
        for key in self:
            for indx,seq_list in enumerate(self[key]):
                yield key,indx,seq_list

    
def get_index_for_all_but_one_changed(nl1,nl2):
    for key, value in nl1.items(): 
        value2 = nl2[key]
        if value != value2:
            if namelists_eq(nl1,nl2,[key]): 
                yield key, value, value2

def namelists_eq(nl1,nl2,ignore_keys=[]):
    nl1_flat = copy_w_ignore_keys(nl1,ignore_keys)
    nl2_flat = copy_w_ignore_keys(nl2,ignore_keys)
    return nl1_flat == nl2_flat
def copy_w_ignore_keys(nl,ignore_keys=[]):
    return dict((key,value) for key, value in nl.items() if key not in ignore_keys)
            

def indices_eq(namelists,indices1,indices2):
    namelist_list1 = SetList(namelists[indx] for indx in indices1)
    namelist_list2 = SetList(namelists[indx] for indx in indices2)
    return namelist_list1.lset_eq(namelist_list2)


class SetList(list):
    """List with some set operations """
    def issubset(self,list2):
        # Checks if self is subset of list2
        list3 = []
        for elem in list2:
            if elem in self:
                list3.append(elem)
        return list2 == list3

    def lset_eq(self,list2):
        return self.issubset(list2) and list2.issubset(self)
    


# The following two functions were inspired by nmltab
def superset(alldicts):
    """ Returns dict containing all keys from the dicts contained in `alldicts`

    :param dict alldicts: a dictionary containing dictionaries"""
    superdict = {}
    for dict_ in alldicts.values():
        superdict.update(dict_)
    return superdict

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
