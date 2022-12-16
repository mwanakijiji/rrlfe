Documentation for rrlfe
=================================

This software package applies a metallicity calibration to low-resolution spectra of RR Lyrae variable stars.
The calibration is in the style of Layden 94, but with significant updates.

This software is for either

#. Determining and updating a metallicity calibration
#. Applying a calibration to low-resolution (R ~2000) spectroscopy

See paper `[TBD] <https://uknowledge.uky.edu/physastron_etds/22/>`_ for details about how the calibration was made, and for further scientific information.
If you do use this calibration or software, please cite the paper `[TBD] (2023)`.

The BibTeX entry is::

    @misc{rrlfe,
      author = {{Spalding}, E., R. Wilhelm, N. de Lee, and K. Carrell},
      title = {rrlfe},
      keywords = {Software},
      howpublished = {Astrophysics Source Code Library},
      year = 2023,
      archivePrefix = "ascl",
      eprint = {xxx.xxx},
      adsurl = {https://ui.adsabs.harvard.edu/abs/xxxxxxx},
      adsnote = {Provided by the SAO/NASA Astrophysics Data System}
    }

Logo art by Anna McElhannon

.. automodule:: modules.create_spec_realizations
    :members:

.. automodule:: modules.compile_normalization
    :members:

.. automodule:: modules.run_robo
    :members:

.. automodule:: modules.scrape_ew_and_errew
    :members:

.. automodule:: modules.teff_retrieval
    :members:

.. automodule:: modules.run_emcee
    :members:

.. toctree::
    :hidden:
    :glob:

    *
