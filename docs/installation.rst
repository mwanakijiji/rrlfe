Installation
=================

We highly recommend that you create a compartmentalized software environment, inside of which
you can install ``rrlfe`` and all the right versions of packages that it relies on.

To create such an environment with ``conda``, follow the instructions `here <https://conda.io/projects/conda/en/latest/user-guide/tasks/manage-environments.html>`_. 
(Use Python version 3.8 at the step \'\'To create an environment with a specific version of Python.\'\')

Activate the environment:

.. code-block:: python

  conda activate rrlfe_env

Pip install ``rrlfe``:

.. code-block:: python

  pip install rrlfe

Make a directory (say, ``rrlfe_io/``) to contain the I/O of your reduction. ``cd`` to it, and grab some files directly from the repo which we
will need:

.. code-block:: python

  wget https://raw.githubusercontent.com/mwanakijiji/rrlfe/main/src.tar.gz
  tar -xvf src.tar.gz

Pip install the packages listed in the requirements file:

.. code-block:: python

  pip install -r requirements.txt

In the parent directory which contains ``rrlfe_io/``, clone the Python port of Robospect and install it
by following the instructions `here <https://github.com/czwa/robospect.py>`_.

Then make directory ``robospect.py/tmp/`` and copy the file ``ll`` to it from the ``rrlfe_io/`` directory. (This 
file tells Robospect where to look for absorption lines in the spectra.)

That's it! You're ready to roll. To try a test run in the ``rrlfe_io/`` directory, run the sample script which was contained in the tar file:

.. code-block:: python

  python example_calibration_application_min_working_example.py

If you would ever like to file an issue on the ``rrlfe`` Github repo, you can do so `here <https://github.com/mwanakijiji/rrlfe/issues>`_.

**Note:** The repository code contains a 3 Mb FITS file `deg_1-100_calib_solution_20230507.fits`, which contains the calibration solution corresponding to that in the paper 
`Spalding et al. 2023 MNRAS 527:828 <https://academic.oup.com/mnras/article/527/1/828/7326007>`_, except that it is a 1:100 undersampling of the posterior chain links. Using the 'degraded' version provided, however, produces 
[Fe/H] retrievals which differ negligibly from those using the full, 300 Mb calibration file. (The full calibration file is available on request.) 

Below is a plot showing how the answers differ between the full and 1:100 degraded calibration. 
The variation is negligible compared to typical [Fe/H] uncertainties of ~0.15.

.. image:: imgs/degraded_comparison.png
  :width: 600
  :align: center
  :alt: Retrieval comparison
