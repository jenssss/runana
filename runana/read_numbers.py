from contextlib import contextmanager
try:
    @contextmanager
    def whatever():
        yield

    @whatever()
    def whateever():
        pass
except TypeError:
    from contextlib2 import contextmanager


@contextmanager
def ignored(*exceptions):
    try:
        yield
    except exceptions:
        pass


# ignored = contextmanager(ignored)

# def ignore_error(error=IOError, return_=None):
#     def ignore(func):
#         @wraps(func)
#         def wrapper(*args, **kwargs):
#             try:
#                 return func(*args, **kwargs)
#             except error:
#                 return return_
#         return wrapper
#     return ignore


ignore_missing_file = ignored(IOError)


@ignore_missing_file
def read_last_number_from_file(fname, pattern=''):
    number = None
    with open(fname) as stdout_file:
        for number in numbers_in_file_iterator(stdout_file, pattern=pattern):
            pass
    return number


@ignore_missing_file
def read_smallest_number_from_file(fname, pattern=''):
    with open(fname) as stdout_file:
        smallest = 100000
        for number in numbers_in_file_iterator(stdout_file, pattern=pattern):
            if number < smallest:
                smallest = number
    return smallest


@ignore_missing_file
def read_number_from_file(fname, inumber, pattern=''):
    with open(fname) as stdout_file:
        for indx, number in enumerate(numbers_in_file_iterator(stdout_file, pattern=pattern)):
            if indx == inumber-1:
                return number
    number = 'Not enough numbers in file'
    return number


@ignore_missing_file
def read_column_from_file(fname, icolumn, pattern=''):
    with open(fname) as stdout_file:
        for line in lines_in_file_iterator(stdout_file, pattern=pattern):
            for indx, word in enumerate(line.split()):
                if indx == icolumn-1:
                    return word


def lines_in_file_iterator(file_handle, pattern=''):
    for line in file_handle:
        if pattern in line:
            yield line


def words_in_file_iterator(file_handle, pattern=''):
    for line in lines_in_file_iterator(file_handle, pattern=pattern):
        for word in line.split():
            yield word


def numbers_in_file_iterator(file_handle, pattern=''):
    for word in words_in_file_iterator(file_handle, pattern=pattern):
        try:
            number = float(word)
            yield number
        except ValueError:
            pass


def split(delimiters, string, maxsplit=0):
    import re
    regexPattern = '|'.join(map(re.escape, delimiters))
    return re.split(regexPattern, string, maxsplit)


@ignore_missing_file
def read_file_sev_blocks(filename):
    with open(filename, 'r') as fil:
        blocks = [[[float(element) for element in line.split()]
                   for line in block.split('\n') if len(line) > 0]
                  for block in split(['\n \n', '\n\n'], fil.read())
                  if len(block) > 0]
    return blocks


def numpy_file_read(fname):
    import numpy as np
    try:
        a = np.loadtxt(fname)
    except IOError:
        a = None
    return a


@ignore_missing_file
def read_file_sev_blocks_c(filename):
    with open(filename, 'r') as fil:
        blocks = [[[num_c(element) for element in line.split()]
                   for line in block.split('\n') if len(line) > 0]
                  for block in split(['\n \n', '\n\n'], fil.read())
                  if len(block) > 0]
    return blocks


@ignore_missing_file
def read_file_super_blocks(filename):
    with open(filename, 'r') as fil:
        blocks = [[[[num_c(element) for element in line.split()]
                    for line in block.split('\n') if len(line) > 0]
                   for block in split(['\n \n', '\n\n'], super_block) if len(block) > 0]
                  for super_block in split(['\n \n \n', '\n\n\n'], fil.read()) if len(super_block) > 0]
    return blocks


@ignore_missing_file
def read_file_sev_blocks_new(filename):
    with open(filename, 'r') as fil:
        lines = [[num_c(element) for element in line.split()]
                 for line in fil.read().split('\n')]
    return split_list(lines)
    # return split_list(split_list(lines))
    # from pprint import pprint
    # pprint(lines)
    # len_lines = list(map(len, lines))
    # pprint(list(len_lines))
    # zero_idx = [i for i, x in enumerate(len_lines) if x == 0]
    # # zero_idx_ends = [0] + zero_idx
    # zero_idx_ends = zero_idx + [len(lines)]
    # pprint(zero_idx)
    # pprint(list(zip(zero_idx_ends, zero_idx_ends[1:])))
    # pprint([(i, i+1) for i in zero_idx])
    # ranges = [(i+1, j) for i, j in zip(zero_idx_ends, zero_idx_ends[1:])]
    # from itertools import chain
    # zero_idx_ranges = [(0, zero_idx[0])] + list(chain(*list(zip([(i, i+1) for i in zero_idx], ranges))))
    # # zero_idx_ranges = list(chain(*list(ranges, zip([(i, i+1) for i in zero_idx])))) + [(zero_idx[-1]+1, len(lines))]
    # pprint(list(zero_idx_ranges))
    # blocks = [lines[i:j] for i, j in zero_idx_ranges]
    # return blocks


from itertools import chain
def split_list(list_):
    print(list_)
    len_lines = list(map(len, list_))
    # print(len_lines)
    zero_idx = [i for i, x in enumerate(len_lines) if x == 0]
    if len(zero_idx) == 0:
        return list_
    else:
        # zero_idx_ends = zero_idx + [len(list_)]
        # ranges = [(i+1, j) for i, j in zip(zero_idx_ends, zero_idx_ends[1:])] # if i+1 != j]
        rangez = []
        if len(list_)-1 != zero_idx[-1]:
            zero_idx = zero_idx + [len(list_)]
        for i, j in zip(zero_idx, zero_idx[1:]):
            # if i+1 != j:
            #     rangez.append((i+1, i+1))
            rangez.append((i+1, j))
        if zero_idx[0] != 0:
            rangez = [(0, zero_idx[0])] + rangez
        # print(rangez)
        # zero_ranges = list([(i, i) for i in zero_idx])
        # print(ranges)
        # print(zero_ranges)
        # print(zero_idx)
        # zero_idx_ranges = [(0, zero_idx[0])] + list(chain(*zip(zero_ranges, ranges)))
        # print(zero_idx_ranges)
        # new_list  = [list_[i:j] for i, j in zero_idx_ranges]
        new_list  = [list_[i:j] for i, j in rangez]
        # print(new_list)
        # return new_list
        splitted_list = split_list(new_list)
        # print(splitted_list)
        return splitted_list



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
        try:
            return float(s)
        except ValueError:
            return s


@ignore_missing_file
def read_file_one_block(filename):
    with open(filename, 'r') as fil:
        block = [[num(element) for element in line.split()]
                 for line in fil.read().split('\n') if len(line) > 0]
    return block


@ignore_missing_file
def read_file_one_block_c(filename):
    with open(filename, 'r') as fil:
        block = [[num_c(element) for element in line.split()]
                 for line in fil.read().split('\n') if len(line) > 0]
    return block


@ignore_missing_file
def read_file_one_block_numpy(filename):
    import numpy as np
    block = read_file_one_block(filename)
    return np.asarray(block)
