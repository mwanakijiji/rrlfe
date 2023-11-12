Tutorial: Applying a calibration
=================

This tutorial shows you how to take a ready-made calibration and apply it to low-resolution stellar 
spectra to find their corresponding metallicities. These steps are all in the script 
``example_application_min_working_example.py``, and the repo contains all the test spectra required to run it.

first series of steps is presented without 
commentary, as they are the same as for generating a calibration, up to and including the section
'Make a net Balmer line.' Commentary resumes below when the steps diverge.

.. code-block:: python

    import high_level_application_accordion as pipeline

.. code-block:: python

    # absolute stem of rrlfe repo
    stem_abs = "/Users/myname/directory1/directory2/rrlfe/"

    # string for the next-level directory which will contain all the I/O
    stem_string = 'rrlfe_io_test/'

    # calibration solution to use (this corresponds to that in Spalding+ 2023 MNRAS)
    calib_soln = 'deg_1-100_calib_solution_20230507.fits'   

.. code-block:: python

    # instantiate object that will contain the series of reduction steps
    test_gen = pipeline.ApplyCalib() ## ## need to let this set config file being read in (currently in __init__)

    # print configuration params to log file
    step = pipeline.ConfigInit(module_name="module1")

    # add step to procedure
    test_gen.add_step(step)

In the above first step which we formally add to the pipeline, the 'module_name' string is arbitrary. We just have to 
define different strings for each module we add to the pipeline, so that they can be kept in order. We may as well
have used ``parakeet`` instead of ``module1``, just as long as we give a different name at each step.

.. code-block:: python

    # compile the C spectral normalization script and define directory in which to place the binary
    step = pipeline.compile_normalization.CompileBkgrnd(
        module_name="module3",
        cc_bkgrnd_dir=stem_abs+"src/")

    # add step to procedure
    test_gen.add_step(step)

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

.. code-block:: python

    # run_robospect on normalized synthetic spectra
    step = pipeline.run_robo.Robo(
        module_name="module5",
        robo_dir_read="../robospect.py/",
        normzed_spec_dir_read=stem_abs+stem_string+"realizations_output/norm/final/",
        robo_output_write=stem_abs+stem_string+"robospect_output/smo_files/")

    # add step to procedure
    test_gen.add_step(step)

.. code-block:: python

    # scrape_ew_from_robo and calculate EWs + err_EW
    step = pipeline.scrape_ew_and_errew.Scraper(
        module_name="module6",
        input_spec_list_read=stem_abs+"src/trunc_sdss_list_single_epoch_3911_to_4950.list",
        robo_output_read=stem_abs+stem_string+"robospect_output/smo_files/",
        file_scraped_write=stem_abs+stem_string+"ew_products/all_ew_info.csv")

    # add step to procedure
    test_gen.add_step(step)

.. code-block:: python

    # scrape_ew_from_robo and calculate EWs + err_EW
    step = pipeline.scrape_ew_and_errew.QualityCheck(
        module_name="module7",
        file_scraped_all_read=stem_abs+stem_string+"ew_products/all_ew_info.csv",
        file_scraped_good_write=stem_abs+stem_string+"ew_products/ew_info_good_only.csv")

    # add step to procedure
    test_gen.add_step(step)

.. code-block:: python

    # transpose/stack all the data, where each row corresponds to a spectrum
    step = pipeline.scrape_ew_and_errew.StackSpectra(
        module_name="module8",
        file_ew_data_read=stem_abs+stem_string+"ew_products/ew_info_good_only.csv",
        file_restacked_write=stem_abs+stem_string+"ew_products/restacked_ew_info_good_only.csv",
        input_spec_list_read=stem_abs+"src/trunc_sdss_list_single_epoch_3911_to_4950.list")

    # add step to procedure
    test_gen.add_step(step)

.. code-block:: python

    # make a net Balmer line from the H-delta and H-gamma lines
    step = pipeline.scrape_ew_and_errew.GenerateNetBalmer(
        module_name="module9",
        file_restacked_read=stem_abs+stem_string+"ew_products/restacked_ew_info_good_only.csv",
        file_ew_net_balmer_write=stem_abs+stem_string+"ew_products/restacked_ew_info_good_only_w_net_balmer.csv")

    # add step to procedure
    test_gen.add_step(step)

.. code-block:: python

    # add errors from noise-churning
    step = pipeline.scrape_ew_and_errew.GenerateAddlEwErrors(
        module_name="module10",
        ew_data_restacked_read=stem_abs+stem_string+"ew_products/restacked_ew_info_good_only_w_net_balmer.csv",
        ew_data_w_net_balmer_read=stem_abs+stem_string+"ew_products/restacked_ew_info_good_only_w_net_balmer_errors.csv")

    # add step to procedure
    test_gen.add_step(step)

The above steps will provide us a table of EWs. Now apply a pre-existing [Fe/H] calibration contained in a FITS file. This will
initially generate 'raw' [Fe/H] values.

.. code-block:: python

    step = pipeline.find_feh.FehRetrieval(
        module_name="module11",
        file_good_ew_read=stem_abs+stem_string+"ew_products/restacked_ew_info_good_only_w_net_balmer_errors.csv",
        file_calib_read=stem_abs+"rrlfe_io_20230507_synthetic/bin/"+calib_soln,
        dir_retrievals_write=stem_abs+stem_string+"bin/pickled_info/",
        file_retrievals_write=stem_abs+stem_string+"bin/retrieved_vals.csv")

    # add step to procedure
    test_gen.add_step(step)

Don't forget to apply the final correction to make the results consistent with high-resolution [Fe/H] studies. 

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