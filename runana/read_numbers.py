from os import path;  pjoin = path.join
from functools import wraps

def ignore_error(error=IOError, return_=None):
    def ignore(func):
        @wraps(func)
        def wrapper(*args,**kwargs):
            try:
                return func(*args,**kwargs)
            except error:
                return return_
        return wrapper
    return ignore

ignore_missing_file = ignore_error()

@ignore_missing_file
def read_last_number_from_file(fname,pattern=''):
    number = None
    with open(fname) as stdout_file:
        for number in numbers_in_file_iterator(stdout_file,pattern=pattern):
            pass
    return number

@ignore_missing_file
def read_number_from_file(fname,inumber,pattern=''):
    with open(fname) as stdout_file:
        for indx,number in enumerate(numbers_in_file_iterator(stdout_file,pattern=pattern)):
            if indx==inumber-1:
                return number
    number = 'Not enough numbers in file'
    return number

@ignore_missing_file
def read_column_from_file(fname,icolumn,pattern=''):
    with open(fname) as stdout_file:
        for line in lines_in_file_iterator(stdout_file,pattern=pattern):
            for indx,word in enumerate(line.split()):
                if indx==icolumn-1:
                    return word
    return None


def lines_in_file_iterator(file_handle,pattern=''):
    for line in file_handle:
        if pattern in line:
            yield line

def words_in_file_iterator(file_handle,pattern=''):
    for line in lines_in_file_iterator(file_handle,pattern=''):
        for word in line.split():
            yield word

def numbers_in_file_iterator(file_handle,pattern=''):
    for word in words_in_file_iterator(file_handle,pattern=''):
        try:
            number=float(word)
            yield number
        except ValueError:
            pass

def split(delimiters, string, maxsplit=0):
    import re
    regexPattern = '|'.join(map(re.escape, delimiters))
    return re.split(regexPattern, string, maxsplit)

def read_file_sev_blocks(filename):
    try:
        with open(filename,'r') as fil:
            blocks = [[[float(element) for element in line.split()]
                       for line in block.split('\n')]
                      for block in split(['\n \n','\n\n'],fil.read())[:-1]]
    except IOError:
        blocks = None
    return blocks

    
def numpy_file_read(fname):
    import numpy as np
    try:
        a = np.loadtxt(fname)
    except IOError:
        a = None
    return a


def read_file_sev_blocks_c(filename):
    try:
        with open(filename,'r') as fil:
            blocks = [[[num_c(element) for element in line.split()]
                       for line in block.split('\n')]
                      for block in split(['\n \n','\n\n'],fil.read())[:-1]]
            print(blocks)
    except IOError:
        blocks = None
    return blocks

def num_c(s):
    try:
        return int(s)
    except ValueError:
        try:
            return float(s)
        except ValueError:
            return complex(s)


def num(s):
    try:
        return int(s)
    except ValueError:
        return float(s)
    
def read_file_one_block(filename):
    with open(filename,'r') as fil:
        block = [[num(element) for element in line.split()]
                 for line in fil.read().split('\n')[:-1]]
    return block


def read_file_one_block_c(filename):
    with open(filename,'r') as fil:
        block = [[num_c(element) for element in line.split()]
                 for line in fil.read().split('\n')[:-1]]
    return block


def read_file_one_block_numpy(filename):
    import numpy as np
    block = read_file_one_block(filename)
    return np.asarray(block)
