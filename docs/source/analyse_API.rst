
Analyse API
===========

Get data
--------

Get parameters
""""""""""""""

.. autofunction:: runana.analyse.collect_from_all
		  
.. autoclass:: runana.analyse.Seqs

.. autofunction:: runana.input_file_handling.read_input_files_f90nml

.. autofunction:: runana.input_file_handling.read_input_files_upname

.. autofunction:: runana.input_file_handling.read_upname_file
		  
.. autofunction:: runana.analyse.unpack_list_values

Get other stuff
"""""""""""""""
	       
.. autofunction:: runana.analyse.make_collector_function

.. autofunction:: runana.analyse.prepend_dir

.. autofunction:: runana.analyse.read_from_dir

.. autofunction:: runana.analyse.dictdiff
		  
		  

Analyse with panda API
----------------------

This module requires the :py:mod:`pandas` package

.. autoclass:: runana.analyse_w_panda.SeqsDataFrame

.. automethod:: runana.analyse_w_panda.SeqsDataFrame.import_from_seq
	       
.. automethod:: runana.analyse_w_panda.SeqsDataFrame.calc_convergence

.. automethod:: runana.analyse_w_panda.SeqsDataFrame.plot_

.. autofunction:: runana.analyse_w_panda.return_dict_element

		  
		  
Read numbers API
----------------

.. autofunction:: runana.read_numbers.read_number_from_file
		  
.. autofunction:: runana.read_numbers.read_last_number_from_file
		  
.. autofunction:: runana.read_numbers.read_column_from_file

.. autofunction:: runana.read_numbers.read_file_one_block
		  
.. autofunction:: runana.read_numbers.read_file_sev_blocks

		  
		  
Matplotlib managers
-------------------

Context managers for using :mod:`matplotlib`. Use these together with pythons `with` statement

.. autoclass:: runana.matplotlib_managers.plot_manager

.. autoclass:: runana.matplotlib_managers.single_fig_manager

.. autoclass:: runana.matplotlib_managers.single_ax_manager

.. autofunction:: runana.matplotlib_managers.plot_ax_manager

	       
		  
		  
		  
