Tutorial: Generating a calibration
=================

The basic idea is that, first, we take synthetic spectra with known input parameters, normalize them, 
and measure the EWs of the absorption lines. Knowing the metallicities [Fe/H], we make a functional fit that 
is an extension of the one in Layden 1994. The raw solution is output as a FITS file containing the MCMC posteriors
and relevant information in the header. 'Raw' in this context signifies that no offset correction 
has been applied to the solution, to make it consistent with retrievals based on high-resoltion spectroscopy.

To find that offset correction, we retrieve [Fe/H] based on low-resolution spectroscopy from stars which already have known values based on 
high-resolution spectroscopy. By comparing the two [Fe/H] values for these stars, the parameters of this correction
are added into the FITS header of the raw calibration to produce a final calibration.

To put all this into practice, we call different classes from rrlfe and string them together into a pipeline.
The user gives each instantiated module a module_name, which allows it to be distinguished from other modules
when the pipeline is run.

To get started, let's import the machinery we need:

.. code-block:: python

    import high_level_application_accordion as pipeline

and make sure to define the absolute path of the repo. All I/O directories will be beneath this.

.. code-block:: python

    stem_abs = "/Users/bandari/Documents/git.repos/rrlfe/"

Now instantiate the object that will contain the series of reduction steps, and instantiate the object
to print configuration parameters to a log file. We need to add the latter to the former with the add_step command.

.. code-block:: python

    test_gen = pipeline.GenerateCalib()

    step = pipeline.ConfigInit(module_name="module1")

    test_gen.add_step(step)


Compile the C script to do the spectral normalization. Notice how the module_name strings are arbitrary. They 
just have to be different each time something is instantiated.

.. code-block:: python

    step = pipeline.compile_normalization.CompileBkgrnd(module_name="module3")

    test_gen.add_step(step)

Take a list of unnormalized empirical spectra, normalize them, and write out. Here, _read directories are those where
data already exists and is being read in, and _write is where the module writes something to. Make sure these 
directories already exist before running the pipeline.

.. code-block:: python

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

    test_gen.add_step(step)

Measure the EWs of the normalized (synthetic) spectra by running Robospect.

.. code-block:: python

    step = pipeline.run_robo.Robo(
        module_name="module5",
        robo_dir_read="../robospect.py/",
        normzed_spec_dir_read=stem_abs+"rrlfe_io_red/realizations_output/norm/final/",
        robo_output_write=stem_abs+"rrlfe_io_red/robospect_output/smo_files/")

    test_gen.add_step(step)

Scrape all the EWs from the raw Robospect output files.

.. code-block:: python

    step = pipeline.scrape_ew_and_errew.Scraper(
        module_name="module6",
        input_spec_list_read=stem_abs+"src/junk_test_synthetic_spectra.list",
        robo_output_read=stem_abs+"rrlfe_io_red/robospect_output/smo_files/",
        file_scraped_write=stem_abs+"rrlfe_io_red/ew_products/all_ew_info.csv")

    test_gen.add_step(step)

Do a quality check on the lines, based on Robospect quality flags. We don't want to base the 
calibration on spurious EWs.

.. code-block:: python

    step = pipeline.scrape_ew_and_errew.QualityCheck(
        module_name="module7",
        file_scraped_all_read=stem_abs+"rrlfe_io_red/ew_products/all_ew_info.csv",
        file_scraped_good_write=stem_abs+"rrlfe_io_red/ew_products/ew_info_good_only.csv")

    test_gen.add_step(step)

Transpose and stack all the data, so that each row corresponds to a spectrum and the columns represent 
different absorption lines.

.. code-block:: python

    step = pipeline.scrape_ew_and_errew.StackSpectra(
        module_name="module8",
        input_spec_list_read=stem_abs+"src/junk_test_synthetic_spectra.list",
        file_ew_data_read=stem_abs+"rrlfe_io_red/ew_products/ew_info_good_only.csv",
        file_restacked_write=stem_abs+"rrlfe_io_red/ew_products/restacked_ew_info_good_only.csv")

    test_gen.add_step(step)

Make a net Balmer line from the H-delta and H-gamma lines

.. code-block:: python

    step = pipeline.scrape_ew_and_errew.GenerateNetBalmer(
        module_name="module9",
        file_restacked_read=stem_abs+"rrlfe_io_red/ew_products/restacked_ew_info_good_only.csv",
        file_ew_net_balmer_write=stem_abs+"rrlfe_io_red/ew_products/restacked_ew_info_good_only_w_net_balmer.csv")

    test_gen.add_step(step)

Add errors from noise-churning (OBSOLETE? CAN THIS BE SKIPPED?)

.. code-block:: python

    step = pipeline.scrape_ew_and_errew.GenerateAddlEwErrors(
        module_name="module10",
        ew_data_restacked_read=stem_abs+"rrlfe_io_red/ew_products/restacked_ew_info_good_only_w_net_balmer.csv",
        ew_data_w_net_balmer_read=stem_abs+"rrlfe_io_red/ew_products/restacked_ew_info_good_only_w_net_balmer_errors.csv")

    test_gen.add_step(step)

Whether you want to *generate* a new calibration or *apply* one that already exists to a given set of spectra, the steps up 
until this point will be essentially the same: we take a bunch of spectra, normalize them, find the absorption line EWs, and put 
them into a big table. 

But now the steps diverge, beginning with the following step to take the known input parameters from synthetic spectra 
and adding them to the big table we have previously generated. Note this step requires a list of spectra we want to select:

.. code-block:: python

    step = pipeline.scrape_ew_and_errew.AddSyntheticMetaData(
        module_name="module11",
        input_spec_list_read=stem_abs+"src/junk_test_synthetic_spectra.list",
        ew_data_w_net_balmer_read=stem_abs+"rrlfe_io_red/ew_products/restacked_ew_info_good_only_w_net_balmer_errors.csv",
        file_w_meta_data_write=stem_abs+"rrlfe_io_red/ew_products/restacked_ew_w_metadata.csv")

    test_gen.add_step(step)

As an added bonus to our calibration, we also calculate a linear function for Teff based on Balmer line width:

.. code-block:: python

    step = pipeline.teff_retrieval.TempVsBalmer(
        module_name="module12",
        file_ew_poststack_read=stem_abs+"rrlfe_io_red/ew_products/restacked_ew_w_metadata.csv",
        file_ew_tefffit_write=stem_abs+"rrlfe_io_red/ew_products/all_data_input_mcmc.csv",
        plot_tefffit_write=stem_abs+"rrlfe_io_red/bin/teff_vs_balmer.png",
        data_tefffit_write=stem_abs+"rrlfe_io_red/bin/teff_vs_balmer_trend.txt")

    test_gen.add_step(step)

Now we actually run the MCMC to do the fit of [Fe/H] as a function of Balmer line width. This
step makes use of the package emcee.

.. code-block:: python

    # run_emcee
    # coeff defs: K = a + bH + cF + dHF + f(H^2) + g(F^2) + h(H^2)F + kH(F^2) + m(H^3) + n(F^3)
    # where K is CaII K EW; H is Balmer EW; F is [Fe/H]
    step = pipeline.run_emcee.RunEmcee(
        module_name="module13",
        file_name_scraped_ews_good_only_read=stem_abs+"rrlfe_io_red/ew_products/all_data_input_mcmc.csv",
        file_name_write_mcmc_text_write=stem_abs+"rrlfe_io_red/bin/mcmc_output.csv")

    test_gen.add_step(step)

Export the table to a FITS file:

.. code-block:: python

    step = pipeline.run_emcee.WriteSolnToFits(
        module_name="module14",
        file_name_mcmc_posterior_read=stem_abs+"rrlfe_io_red/bin/mcmc_output.csv",
        file_name_teff_data_read=stem_abs+"rrlfe_io_red/bin/teff_vs_balmer_trend.txt",
        soln_write_name=stem_abs+"rrlfe_io_red/bin/calib_solution.fits")

    test_gen.add_step(step)

This optional step is a wrapper for making a nice corner plot from the emcee package:

.. code-block:: python

    step = pipeline.run_emcee.CornerPlot(
        module_name="module15",
        file_name_mcmc_posterior_read=stem_abs+"rrlfe_io_red/bin/mcmc_output.csv",
        plot_corner_write=stem_abs+"rrlfe_io_red/bin/mcmc_corner.png")

    test_gen.add_step(step)

.. code-block:: python

    test_gen.run()

Once we have the raw calibration, there is just one piece missing: a final correction to remove any offset relative to [Fe/H] retrievals 
using high-resolution spectroscopy. To do that, skip to the next tutorial on applying a calibration, and apply the raw
calibration to a basis set of low-resolution spectra. (In Spalding+ 2023, we used spectra taken from McDonald Observatory.)

Once you have done so, run the following mini-pipeline: 

.. code-block:: python

    import high_level_application_accordion as pipeline
    stem_abs = "/Users/bandari/Documents/git.repos/rrlfe/"

    test_gen = pipeline.GenerateCalib()

    step = pipeline.ConfigInit(module_name="module1")

    test_gen.add_step(step)

    step = pipeline.final_corrxn.FindCorrxn(
        module_name="module16",
        file_name_mcd_lit_fehs="", # McD EW values
        soln_write_name=stem_abs+"rrlfe_io_red/bin/calib_solution.fits" # solution to which we will append corrxn to
    )

    test_gen.add_step(step)

And here's the step that executes the steps which have been strung together: 

.. code-block:: python
    
    test_gen.run()

Now you should have gotten a FITS file with the calibration, and containing correction parameters in the header.
