Installation
=================

You can clone the code for this package from the command line:

.. code-block:: python

  git clone https://github.com/mwanakijiji/rrlfe.git

(A ``pip install`` option will come in the future.)

As a next step, we highly recommend that you create a compartmentalized software environment, inside of which
you can install all the right versions of various software packages that ``rrlfe`` relies on, and without interfering
with other installations on your local system. We recommend you have ``conda`` installed to do this.
Here are two ways of creating such an environment with ``conda``:

1.  Run the following command in the ``rrlfe/`` home directory:

    .. code-block:: python

      make

    This will initialize Python version 3.8 environment called ``rrlfe_env`` and install pip inside of it. 

2. Follow the instructions `here <https://conda.io/projects/conda/en/latest/user-guide/tasks/manage-environments.html>`_.
  (Use Python version 3.8 at the step \'\'To create an environment with a specific version of Python.\'\')

Activate the environment with ``conda``:

.. code-block:: python

  conda activate rrlfe_env

And install the requirements for ``rrlfe`` with pip:

.. code-block:: python

  pip install -r requirements.txt

Now, install the Python port of Robospect. You can do this in one of two ways:

1.  In the directory ``rrlfe/``, run a script which clones Robospect into the parent directory one level higher, installs it, and copies an absorption line list into it:

  .. code-block:: python

    python install_robospect.py

2. Do this manually by following the instructions `here <https://github.com/czwa/robospect.py>`_.

  Make sure to clone the code into the same parent directory which contains the ``rrlfe/`` directory. 
  (Note that if there are any deprecation errors in the installation step, you may need 
  to file an issue in the Robospect.py `repo <https://github.com/czwa/robospect.py/issues>`_, which is maintained 
  independently of ``rrlfe``.) Then make directory ``robospect.py/tmp/`` and copy the file ``ll`` to it from the ``rrlfe/`` directory. (This 
  file tells Robospect where to look for absorption lines in the spectra.)

That's it! You're ready to roll. You can try a test run in the ``rrlfe/`` directory with the command

.. code-block:: python

  python example_application_min_working_example.py

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
