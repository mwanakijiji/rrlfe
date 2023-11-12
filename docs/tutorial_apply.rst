Tutorial: Applying a calibration
=================

This tutorial shows you how to take a ready-made calibration and apply it to low-resolution stellar 
spectra to find their corresponding metallicities. These steps are all in the script 
``example_application_min_working_example.py``, and the repo contains all the test spectra required to run it.

Let's get started!

Normalize a given set of spectra
----

This section can be applied to any given input spectra, be they synthetic or empirical, and for the purpose of either generating 
a calibration from them, or applying a calibration to them. This tutorial is specifically about applying a calibration,
so the various choices of directories will be to that end.

Start by importing the machinery we need:

.. code-block:: python

    import high_level_application_accordion as pipeline

We define the absolute path of the repo, and the I/O directory which will be located beneath that. 
In addition we define a handy string or two. 

.. code-block:: python

    # absolute stem of rrlfe repo
    stem_abs = "/Users/myname/directory1/directory2/rrlfe/"

    # string for the next-level directory which will contain all the I/O
    stem_string = 'rrlfe_io_test/'

    # calibration solution to use (this corresponds to that in Spalding+ 2023 MNRAS)
    calib_soln = 'deg_1-100_calib_solution_20230507.fits'   

Now instantiate the object that will contain the series of reduction steps, and instantiate the object
to print configuration parameters to a log file. We need to add the latter to the former with the add_step command.

.. code-block:: python

    # instantiate object that will contain the series of steps of the pipeline
    test_gen = pipeline.ApplyCalib()

    # print configuration params to log file
    step = pipeline.ConfigInit(module_name="module1")

    # add step to procedure
    test_gen.add_step(step)

In the above first step which we formally add to the pipeline, the 'module_name' string is arbitrary. We just have to 
define different strings for each module we add to the pipeline, so that they can be kept in order. We may as well
have used ``parakeet`` instead of ``module1``, just as long as we give a different name at each step.

Now we compile the C script to do the spectral normalization. Notice how the module_name strings are arbitrary. They 
just have to be different each time something is instantiated.

.. code-block:: python

    # compile the C spectral normalization script and define directory in which to place the binary
    step = pipeline.compile_normalization.CompileBkgrnd(
        module_name="module3",
        cc_bkgrnd_dir=stem_abs+"src/")

    # add step to procedure
    test_gen.add_step(step)

Take a list of unnormalized empirical spectra, normalize them, and write out. Here, _read directories are those where
data already exists and is being read in, and _write is where the module writes something to. New directories will be 
made as needed. 

Note that the `list <https://raw.githubusercontent.com/mwanakijiji/rrlfe/main/src/trunc_sdss_list_single_epoch_3911_to_4950.list>`_ 
of input spectra includes file basenames under a column `orig_spec_file_name`, and a few empty columns which do not come into play
here (they define some metadata for *generating* a new calibration).

:download:`Here <https://raw.githubusercontent.com/mwanakijiji/rrlfe/main/src/sdss_single_epoch_chopped_3911_to_4950/spec-0266-51630-0197g001.dat>`_ is also an example of 
a spectrum input file from that list. It includes formatting which the pipeline is looking for: three 
whitespace-delimited columns of wavelength (in anglstroms), flux (arbitrary) and flux noise.

.. code-block:: python

    # take list of unnormalized empirical spectra, normalize them, and write out
    step = pipeline.create_spec_realizations.CreateSpecRealizationsMain(
        module_name="module4",
        cc_bkgrnd_dir=stem_abs+"src/",
        input_spec_list_read=stem_abs+"src/trunc_sdss_list_single_epoch_3911_to_4950.list",
        unnorm_spectra_dir_read=stem_abs+"src/sdss_single_epoch_chopped_3911_to_4950/",
        unnorm_noise_churned_spectra_dir_read=stem_abs+stem_string+"realizations_output/",
        bkgrnd_output_dir_write=stem_abs+stem_string+"realizations_output/norm/",
        final_spec_dir_write=stem_abs+stem_string+"realizations_output/norm/final/",
        noise_level=0.0,
        spec_file_type="ascii.no_header",
        number_specs=1,
        verb=False)

    # add step to procedure
    test_gen.add_step(step)

Measure EWs of absorption lines
----

Run `Robospect <https://home.ifa.hawaii.edu/users/watersc1/robospect/>`_ on the spectra to measure and write out the EWs.

.. code-block:: python

    # run_robospect on normalized synthetic spectra
    step = pipeline.run_robo.Robo(
        module_name="module5",
        robo_dir_read="../robospect.py/",
        normzed_spec_dir_read=stem_abs+stem_string+"realizations_output/norm/final/",
        robo_output_write=stem_abs+stem_string+"robospect_output/smo_files/")

    # add step to procedure
    test_gen.add_step(step)

Scrape all the EWs from the raw Robospect output files.

.. code-block:: python

    # scrape_ew_from_robo and calculate EWs + err_EW
    step = pipeline.scrape_ew_and_errew.Scraper(
        module_name="module6",
        input_spec_list_read=stem_abs+"src/trunc_sdss_list_single_epoch_3911_to_4950.list",
        robo_output_read=stem_abs+stem_string+"robospect_output/smo_files/",
        file_scraped_write=stem_abs+stem_string+"ew_products/all_ew_info.csv")

    # add step to procedure
    test_gen.add_step(step)

Do a quality check on the lines, based on Robospect quality flags. We don't want to base the 
calibration on spurious EWs.

.. code-block:: python

    # scrape_ew_from_robo and calculate EWs + err_EW
    step = pipeline.scrape_ew_and_errew.QualityCheck(
        module_name="module7",
        file_scraped_all_read=stem_abs+stem_string+"ew_products/all_ew_info.csv",
        file_scraped_good_write=stem_abs+stem_string+"ew_products/ew_info_good_only.csv")

    # add step to procedure
    test_gen.add_step(step)

Transpose and stack all the data, so that each row corresponds to a spectrum and the columns represent 
different absorption lines.

.. code-block:: python

    # transpose/stack all the data, where each row corresponds to a spectrum
    step = pipeline.scrape_ew_and_errew.StackSpectra(
        module_name="module8",
        file_ew_data_read=stem_abs+stem_string+"ew_products/ew_info_good_only.csv",
        file_restacked_write=stem_abs+stem_string+"ew_products/restacked_ew_info_good_only.csv",
        input_spec_list_read=stem_abs+"src/trunc_sdss_list_single_epoch_3911_to_4950.list")

    # add step to procedure
    test_gen.add_step(step)

Make a net Balmer line
------

We combine the the H-delta and H-gamma lines to make a 'net' Balmer absorption line

.. code-block:: python

    # make a net Balmer line from the H-delta and H-gamma lines
    step = pipeline.scrape_ew_and_errew.GenerateNetBalmer(
        module_name="module9",
        file_restacked_read=stem_abs+stem_string+"ew_products/restacked_ew_info_good_only.csv",
        file_ew_net_balmer_write=stem_abs+stem_string+"ew_products/restacked_ew_info_good_only_w_net_balmer.csv")

    # add step to procedure
    test_gen.add_step(step)

Add EW errors for the net Balmer lines

.. code-block:: python

    # add errors
    step = pipeline.scrape_ew_and_errew.GenerateAddlEwErrors(
        module_name="module10",
        ew_data_restacked_read=stem_abs+stem_string+"ew_products/restacked_ew_info_good_only_w_net_balmer.csv",
        ew_data_w_net_balmer_read=stem_abs+stem_string+"ew_products/restacked_ew_info_good_only_w_net_balmer_errors.csv")

    # add step to procedure
    test_gen.add_step(step)

The above steps will provide us a table of EWs. Whether you want to *apply* a calibration to spectra to get [Fe/H] values or 
*generate* a new calibration, the steps up until this point will be essentially the same: we take a bunch of spectra, 
normalize them, find the absorption line EWs, generate net Balmer lines, and put all the info into a big table. 

Now the steps between *applying* and *generating* a calibration diverge. Below we apply our pre-existing [Fe/H] 
calibration contained in a FITS file. This will initially generate 'raw' [Fe/H] values.

.. code-block:: python

    step = pipeline.find_feh.FehRetrieval(
        module_name="module11",
        file_good_ew_read=stem_abs+stem_string+"ew_products/restacked_ew_info_good_only_w_net_balmer_errors.csv",
        file_calib_read=stem_abs+"rrlfe_io_20230507_synthetic/bin/"+calib_soln,
        dir_retrievals_write=stem_abs+stem_string+"bin/pickled_info/",
        file_retrievals_write=stem_abs+stem_string+"bin/retrieved_vals.csv")

    # add step to procedure
    test_gen.add_step(step)

These 'raw' values still have to be corrected for an offset to make them consistent with 
high-res spectroscopic studies. Below we apply that final correction.

.. code-block:: python

    # apply final correction
    step = pipeline.final_corrxn.ApplyCorrxn(
        module_name="module16",
        file_name_basis_raw_retrieved_fehs=stem_abs+stem_string+"bin/retrieved_vals.csv", # retrieved McD Fe/H values based on raw rrlfe calibration
        soln_fits_name=stem_abs+"rrlfe_io_20230507_synthetic/bin/"+calib_soln, # calibration file which includes correction info in the header
        file_name_corrected_retrieved_fehs_write=stem_abs+stem_string+"bin/retrieved_vals_corrected.csv" # mapped high-res literature Fe/H values for McD stars
    )

    # add step to procedure
    test_gen.add_step(step)

Here's the final line of code that executes the above steps which have been strung together: 

.. code-block:: python

    test_gen.run()

That's it! You should have final [Fe/H] values in the file `retrieved_vals_corrected.csv`, whose absolute path is printed 
to screen and to the log. That file contains various intermediatary data as well, but the columns you are likely most
interested in are 

`orig_spec_file_name`: the original file name of the spectrum
`feh_corrected`: [Fe/H], after having applied the last correction above
`err_feh_retrieved`: random error in [Fe/H]
`teff_retrieved`: a coarse measure of the Teff of the spectum, based on the strong correlation between some Balmer lines and Teff
