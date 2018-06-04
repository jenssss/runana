from shutil import copy

try:
    basestring          # Python 2.x
except NameError:
    basestring = str    # Python 3.x


def filter_inp_file_f90nml(inp_file_in, inp_file_out, replace_with_these):
    """ Replaces elements in *inp_file_in* and places the result in *inp_file_out*

    replace_with_these is a dict with entries of the form
    {'Name of parameter':*value to replace with*}

    This version works on namelist files using the f90nml package
    """
    import f90nml
    patch = patch_from_tupled_dict(replace_with_these)
    if patch:
        f90nml.patch(inp_file_in, patch, inp_file_out)
    else:
        copy(inp_file_in, inp_file_out)


def patch_from_tupled_dict(tupled_dict):
    patch = {}
    for replace_this, replace_val in tupled_dict.items():
        group, field = replace_this
        gdict = patch.get(group, {})
        gdict.update({field: replace_val})
        patch[group] = gdict
    return patch


def filter_inp_file_upname(inp_file_in, inp_file_out, replace_with_these):
    """ Replaces elements in *inp_file_in* and places the result in *inp_file_out*

    replace_with_these is a dict with entries of the form
    {'Name of parameter':*value to replace with*}

    This version replaces entries that is one line below a string matching
    *Name of parameter*, in the same position as the string
    """
    with open(inp_file_in, 'r') as input_file_in:
        with open(inp_file_out, 'w') as input_file_out:
            index_replace = {}
            for line in input_file_in:
                if index_replace:
                    lin = line.split()
                    for replace_this in index_replace:
                        lin[index_replace[replace_this]] = str(replace_with_these[replace_this])
                    input_file_out.write('  '.join(lin)+'\n')
                    index_replace = {}
                else:
                    input_file_out.write(line)
                for replace_this in replace_with_these:
                    for index, word in enumerate(line.split()):
                        if replace_this == word:
                            index_replace[replace_this] = index


#: Available input file filter functions
INP_FILE_FILTERS = {'f90nml': filter_inp_file_f90nml,
                    'upname': filter_inp_file_upname}


def read_upname_file(filename):
    """ Reads file in upname format

    In this format the names of variables are given on a line, with the values
    on the following line. Each variable/name should be seperated by at least
    two whitespaces or a tab. Each set of names/values lines should be
    seperated by at least one blank line
    """
    with open(filename, 'r') as input_file_in:
        previous_line = []
        data = {}
        for line in input_file_in:
            # Break line on tab or more than two consequtive whitespaces
            line = line.rstrip().replace('\t', '  ').split('  ')
            line = [num_str(elem.strip()) for elem in line if elem]
            data.update(dict(zip(previous_line, line)))
            previous_line = line
    return data


def read_input_files_upname(patterns=['*.inp']):
    """ Read the all files matching `patterns` with :func:`read_upname_file`

    The data from all the files is supersetted and the resulting dict is
    returned
    """
    from itertools import chain
    import glob
    filenames = list(chain(*(glob.glob(pattern)
                             for pattern in string_or_iterable(patterns))))
    dicts = dict((filename, read_upname_file(filename))
                 for filename in filenames)
    return superset(dicts)


def flat_iterator(nml):
    """Iterator that returns the adress of an element as a 2-tuple,
    along with the element """
    for key, value in nml.items():
        for inner_key, inner_value in value.items():
            yield (key, inner_key), inner_value


def read_and_flatten_namelist(filename):
    import f90nml
    namelist = f90nml.read(filename)
    dict_ = dict(flat_iterator(namelist))
    return dict_


def read_input_files_f90nml(patterns=['*.nml']):
    """ Read the all files matching `patterns` with :func:`f90nml.read`

    The namelists are flattened and supersetted, the resulting dict is
    returned
    """
    from itertools import chain
    import glob
    filenames = list(chain(*(glob.glob(pattern)
                             for pattern in string_or_iterable(patterns))))
    dicts = dict((filename, read_and_flatten_namelist(filename))
                 for filename in filenames)
    return superset(dicts)


def string_or_iterable(args):
    """ Generator that assumes args is either a string or an iterable. """
    if isinstance(args, basestring):
        yield args
    else:
        for arg in args:
            yield arg


# This function was inspired by nmltab
def superset(alldicts):
    """ Returns dict containing all keys from the dicts contained in `alldicts`

    :param dict alldicts: a dictionary containing dictionaries"""
    superdict = {}
    for dict_ in alldicts.values():
        superdict.update(dict_)
    return superdict


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
