Tutorial: Generating a calibration
=================

The basic idea is that, first, we take synthetic spectra with known input parameters, normalize them, 
and measure the EWs of the absorption lines. Knowing the metallicities [Fe/H], we make a functional fit that 
is an extension of the one in Layden 1994. The solution is a FITS file with the MCMC posteriors.

Then, we retrieve [Fe/H] from stars which already have known values based on high-resolution spectroscopy.
This lets us find a final correction to the raw calibration we have made, and the parameters of this correction
are added into the FITS header of the raw calibration. 'Raw' in the context here signifies that no offset correction 
is applied at the very end.'

In the highest level of the rrlfe repo, let's import what we need:

.. code-block:: python

    import high_level_application_accordion as pipeline

.. code-block:: python

    # absolute stem of repo; needed to make dirs if they don't exist
    stem_abs = "/Users/bandari/Documents/git.repos/rrlfe/"

.. code-block:: python

    # instantiate object that will contain the series of reduction steps
    test_gen = pipeline.GenerateCalib() ## ## need to let this set config file being read in (currently in __init__)

    # print configuration params to log file
    step = pipeline.ConfigInit(module_name="module1")

    # add step to procedure
    test_gen.add_step(step)

.. code-block:: python

    # compile the C spectral normalization script
    step = pipeline.compile_normalization.CompileBkgrnd(module_name="module3")

    # add step to procedure
    test_gen.add_step(step)


    # take list of unnormalized empirical spectra, normalize them, and write out
    step = pipeline.create_spec_realizations.CreateSpecRealizationsMain(
        module_name="module4",
        input_spec_list_read=stem_abs+"src/sdss_test_20221213.list",
        unnorm_spectra_dir_read=stem_abs+"src/sdss_20221213_cosmic_rays_removed_automated_3900_to_5299_angstr/",
        unnorm_noise_churned_spectra_dir_read=stem_abs+"src/realizations_output/",
        bkgrnd_output_dir_write=stem_abs+"rrlfe_io_20221220_sdss_test_2/realizations_output/norm/",
        final_spec_dir_write=stem_abs+"rrlfe_io_20221220_sdss_test_2/realizations_output/norm/final/",
        noise_level=0.0,
        spec_file_type="ascii.no_header",
        number_specs=1,
        verb=False)

.. code-block:: python

    # add step to procedure
    test_gen.add_step(step)
    #'''# skipping, because it takes too much time
    # run_robospect on normalized synthetic spectra
    step = pipeline.run_robo.Robo(
        module_name="module5",
        robo_dir_read="../robospect.py/",
        normzed_spec_dir_read=stem_abs+"rrlfe_io_red/realizations_output/norm/final/",
        robo_output_write=stem_abs+"rrlfe_io_red/robospect_output/smo_files/")

    # add step to procedure
    test_gen.add_step(step)

.. code-block:: python

    # scrape_ew_from_robo and calculate EWs + err_EW
    step = pipeline.scrape_ew_and_errew.Scraper(
        module_name="module6",
        input_spec_list_read=stem_abs+"src/junk_test_synthetic_spectra.list",
        robo_output_read=stem_abs+"rrlfe_io_red/robospect_output/smo_files/",
        file_scraped_write=stem_abs+"rrlfe_io_red/ew_products/all_ew_info.csv")

    # add step to procedure
    test_gen.add_step(step)

.. code-block:: python

    # scrape_ew_from_robo and calculate EWs + err_EW
    step = pipeline.scrape_ew_and_errew.QualityCheck(
        module_name="module7",
        file_scraped_all_read=stem_abs+"rrlfe_io_red/ew_products/all_ew_info.csv",
        file_scraped_good_write=stem_abs+"rrlfe_io_red/ew_products/ew_info_good_only.csv")

    # add step to procedure
    test_gen.add_step(step)

.. code-block:: python

    # transpose/stack all the data, where each row corresponds to a spectrum
    step = pipeline.scrape_ew_and_errew.StackSpectra(
        module_name="module8",
        input_spec_list_read=stem_abs+"src/junk_test_synthetic_spectra.list",
        file_ew_data_read=stem_abs+"rrlfe_io_red/ew_products/ew_info_good_only.csv",
        file_restacked_write=stem_abs+"rrlfe_io_red/ew_products/restacked_ew_info_good_only.csv")

    # add step to procedure
    test_gen.add_step(step)

.. code-block:: python

    # make a net Balmer line from the H-delta and H-gamma lines
    step = pipeline.scrape_ew_and_errew.GenerateNetBalmer(
        module_name="module9",
        file_restacked_read=stem_abs+"rrlfe_io_red/ew_products/restacked_ew_info_good_only.csv",
        file_ew_net_balmer_write=stem_abs+"rrlfe_io_red/ew_products/restacked_ew_info_good_only_w_net_balmer.csv")

    # add step to procedure
    test_gen.add_step(step)

.. code-block:: python

    # add errors from noise-churning (obsolete)
    step = pipeline.scrape_ew_and_errew.GenerateAddlEwErrors(
        module_name="module10",
        ew_data_restacked_read=stem_abs+"rrlfe_io_red/ew_products/restacked_ew_info_good_only_w_net_balmer.csv",
        ew_data_w_net_balmer_read=stem_abs+"rrlfe_io_red/ew_products/restacked_ew_info_good_only_w_net_balmer_errors.csv")

    # add step to procedure
    test_gen.add_step(step)

.. code-block:: python

    # take meta-data from file names of synthetic spectra and add to table
    step = pipeline.scrape_ew_and_errew.AddSyntheticMetaData(
        module_name="module11",
        input_spec_list_read=stem_abs+"src/junk_test_synthetic_spectra.list",
        ew_data_w_net_balmer_read=stem_abs+"rrlfe_io_red/ew_products/restacked_ew_info_good_only_w_net_balmer_errors.csv",
        file_w_meta_data_write=stem_abs+"rrlfe_io_red/ew_products/restacked_ew_w_metadata.csv")

    # add step to procedure
    test_gen.add_step(step)

.. code-block:: python

    # scrape_ew_from_robo and calculate EWs + err_EW
    step = pipeline.teff_retrieval.TempVsBalmer(
        module_name="module12",
        file_ew_poststack_read=stem_abs+"rrlfe_io_red/ew_products/restacked_ew_w_metadata.csv",
        file_ew_tefffit_write=stem_abs+"rrlfe_io_red/ew_products/all_data_input_mcmc.csv",
        plot_tefffit_write=stem_abs+"rrlfe_io_red/bin/teff_vs_balmer.png",
        data_tefffit_write=stem_abs+"rrlfe_io_red/bin/teff_vs_balmer_trend.txt")

    # add step to procedure
    test_gen.add_step(step)

.. code-block:: python

    # run_emcee
    # coeff defs: K = a + bH + cF + dHF + f(H^2) + g(F^2) + h(H^2)F + kH(F^2) + m(H^3) + n(F^3)
    # where K is CaII K EW; H is Balmer EW; F is [Fe/H]
    step = pipeline.run_emcee.RunEmcee(
        module_name="module13",
        file_name_scraped_ews_good_only_read=stem_abs+"rrlfe_io_red/ew_products/all_data_input_mcmc.csv",
        file_name_write_mcmc_text_write=stem_abs+"rrlfe_io_red/bin/mcmc_output.csv")

    # add step to procedure
    test_gen.add_step(step)

.. code-block:: python

    step = pipeline.run_emcee.WriteSolnToFits(
        module_name="module14",
        file_name_mcmc_posterior_read=stem_abs+"rrlfe_io_red/bin/mcmc_output.csv",
        file_name_teff_data_read=stem_abs+"rrlfe_io_red/bin/teff_vs_balmer_trend.txt",
        soln_write_name=stem_abs+"rrlfe_io_red/bin/calib_solution.fits")

    # add step to procedure
    test_gen.add_step(step)

.. code-block:: python

    step = pipeline.run_emcee.CornerPlot(
        module_name="module15",
        file_name_mcmc_posterior_read=stem_abs+"rrlfe_io_red/bin/mcmc_output.csv",
        plot_corner_write=stem_abs+"rrlfe_io_red/bin/mcmc_corner.png")

    # add step to procedure
    test_gen.add_step(step)

.. code-block:: python

    # apply the raw calibration to the McD star EW data, and find the correction based on them
    # this requires a separate application script to have run on the McD data; it's too complicated to build it in here; TBD later
    step = pipeline.final_corrxn.FindCorrxn(
        module_name="module16",
        file_name_mcd_lit_fehs="", # McD EW values
        soln_write_name=stem_abs+"rrlfe_io_red/bin/calib_solution.fits" # solution to which we will append corrxn to
    )

.. code-block:: python

    test_gen.run()



