from runana.write_numbers import write_file_sev_blocks
from runana.read_numbers import read_file_sev_blocks_new


def test_write_array():
    array = [[1, 2, 5], [3, 4]]
    array = [array, array, array]
    array = [array, array]
    # array = [3, 4]
    filename = "write_numbers.dat"
    write_file_sev_blocks(filename, array)
    read_array = read_file_sev_blocks_new(filename)
    assert array == read_array
