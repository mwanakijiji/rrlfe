Tutorial: Generating a calibration
=================

The basic idea is as follows:

1. We take synthetic spectra with known input parameters, normalize them, 
and measure the EWs of the absorption lines. Knowing the metallicities [Fe/H], we make a functional fit that 
is an extension of the one in Layden 1994. The raw solution is output as a FITS file containing the MCMC posteriors
and relevant information in the header. 'Raw' in this context signifies that no offset correction 
has been applied to the solution to make it consistent with retrievals based on high-resolution spectroscopy. 
`Here <https://raw.githubusercontent.com/mwanakijiji/rrlfe/main/example_calibration_generation_raw_min_working_example.py>`_
is an example script that does through all these steps, and we step through them below.


2. To find the offset correction between the [Fe/H] values based on the raw and high-res studies, we retrieve 
[Fe/H] based on empirical low-resolution spectroscopy from stars which already have known values based on 
high-resolution spectroscopy. By comparing the two [Fe/H] values for these stars, the parameters of this correction
are added into the FITS header of the raw calibration to produce a 'final' calibration.

To put all this into practice, we call different classes from ``rrlfe`` and string them together into a pipeline.
The user gives each instantiated module a ``module_name``, which allows it to be distinguished from other modules
when the pipeline is run.

Note the first series of steps---normalizing spectra, measuring the EWs of their absorption lines, 
and packaging the results into large data tables---is virtually the same as for applying a ready-made calibration
to a given set of spectra. (See `Tutorial: Applying a Calibration`.) This tutorial is specifically about generating a calibration,
so the choices of directory names will be to that end. If you are already familiar with how to normalize spectra 
and measure their EWs, you can probably skip down to the section `Add known meta-data and run MCMC`. 

Normalize a given set of synthetic spectra
----

Start by importing the machinery we need:

.. code-block:: python

    from rrlfe import high_level_generation_accordion as pipeline

We define the absolute path of the repo, and the I/O directory which will be located beneath that. 
In addition we define a handy string or two. 

.. code-block:: python

    # absolute stem of rrlfe repo
    stem_abs = "/Users/myname/directory1/directory2/rrlfe/"

    # string for the next-level directory which will contain all the I/O
    stem_string = 'rrlfe_io_test/'

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

Note that the `list <https://raw.githubusercontent.com/mwanakijiji/rrlfe/main/src/synthetic_spectra.list>`_ 
of input spectra includes file basenames under a column `orig_spec_file_name` (see the `Prerequisites` page), and a few columns which 
contain metadata for *generating* a new calibration.

`Here <https://raw.githubusercontent.com/mwanakijiji/rrlfe/main/src/sdss_single_epoch_chopped_3911_to_4950/spec-0266-51630-0197g001.dat>`_ 
is an example spectrum input file. It includes formatting which the pipeline is looking for: three 
whitespace-delimited columns of wavelength (in angstroms), flux (arbitrary) and flux noise.

.. code-block:: python

    # take list of unnormalized empirical spectra, normalize them, and write out
    step = pipeline.create_spec_realizations.CreateSpecRealizationsMain(
        module_name="module4",
        cc_bkgrnd_dir=stem_abs+"src/",
        input_spec_list_read=stem_abs+"src/synthetic_spectra.list",
        unnorm_spectra_dir_read=stem_abs+"src/synthetic_spectra/",
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
        input_spec_list_read=stem_abs+"src/synthetic_spectra.list",
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
        input_spec_list_read=stem_abs+"src/synthetic_spectra.list")

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

Whether you want to *generate* a new calibration or *apply* one that already exists to a given set of spectra, the steps up 
until this point will be essentially the same: we take a bunch of spectra, normalize them, find the absorption line EWs, and put 
them into a big table. 

But now the steps diverge, beginning with the following step to take the known input parameters from synthetic spectra 
and adding them to the big table we have previously generated. 

Add known meta-data and run MCMC
------

Note this step requires a list of spectra we want to select

.. code-block:: python

    step = pipeline.scrape_ew_and_errew.AddSyntheticMetaData(
        module_name="module11",
        input_spec_list_read=stem_abs+"src/synthetic_spectra.list",
        ew_data_w_net_balmer_read=stem_abs+stem_string+"/ew_products/restacked_ew_info_good_only_w_net_balmer_errors.csv",
        file_w_meta_data_write=stem_abs+stem_string+"/ew_products/restacked_ew_w_metadata.csv")

    test_gen.add_step(step)

As an added bonus to our calibration, we also calculate a linear function for Teff based on Balmer line width:

.. code-block:: python

    step = pipeline.teff_retrieval.TempVsBalmer(
        module_name="module12",
        file_ew_poststack_read=stem_abs+stem_string+"ew_products/restacked_ew_w_metadata.csv",
        file_ew_tefffit_write=stem_abs+stem_string+"ew_products/all_data_input_mcmc.csv",
        plot_tefffit_write=stem_abs+stem_string+"bin/teff_vs_balmer.png",
        data_tefffit_write=stem_abs+stem_string+"bin/teff_vs_balmer_trend.txt")

    test_gen.add_step(step)

Now we actually run the MCMC to do the fit of [Fe/H] as a function of Balmer line width. This
step makes use of the package emcee.

.. code-block:: python

    # run_emcee
    # coeff defs: K = a + bH + cF + dHF + f(H^2) + g(F^2) + h(H^2)F + kH(F^2) + m(H^3) + n(F^3)
    # where K is CaII K EW; H is Balmer EW; F is [Fe/H]
    step = pipeline.run_emcee.RunEmcee(
        module_name="module13",
        file_name_scraped_ews_good_only_read=stem_abs+stem_string+"ew_products/all_data_input_mcmc.csv",
        file_name_write_mcmc_text_write=stem_abs+stem_string+"bin/mcmc_output.csv")

    test_gen.add_step(step)

Export the raw calibration
------

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
using high-resolution spectroscopy. 

Add final correction to the raw calibration
------

To do that, skip to the next tutorial on applying a calibration, and apply the raw
calibration you just made to a basis set of low-resolution spectra. 
In Spalding et al. 2024, we used spectra taken from McDonald Observatory.

Once you have done so and have retrieved [Fe/H] values from a basis set of empirical spectra, you can 
run the following mini-pipeline: 

.. code-block:: python

    import high_level_application_accordion as pipeline

    stem_abs = "/Users/myname/directory1/directory2/rrlfe/"
    stem_string = 'rrlfe_io_test/'

    test_gen = pipeline.GenerateCalib()

    step = pipeline.ConfigInit(module_name="module1")

    test_gen.add_step(step)

    step = pipeline.final_corrxn.FindCorrxn(
        module_name="module16",
        file_name_basis_raw_retrieved_fehs=stem_abs+stem_string+"bin/retrieved_vals.csv", # retrieved McD Fe/H values based on raw rrlfe calibration
        file_name_basis_lit_fehs=stem_abs+"src/mapped_program_fehs_20230402.csv", # file name with composite literature [Fe/H] values of McD stars based on high-res spectroscopy
        soln_write_name=stem_abs+stem_string+"bin/calib_solution_test_20231119.fits" # mapped high-res literature Fe/H values for McD stars
    )

    test_gen.add_step(step)

And here's the step that executes the steps which have been strung together: 

.. code-block:: python
    
    test_gen.run()

To see the longer version of the above step---which includes the normalization of McDonald spectra, measurement
of their EWs, and determination of the final offset correction---check out out the example script 
`here <https://raw.githubusercontent.com/mwanakijiji/rrlfe/main/example_calibration_correction_generation_min_working_example.py>`_.
(This script is also in the repo and the tarball src.tar.gz.)

Done! Now you should have a FITS file with the raw calibration in the table data, and with correction parameters in the header.
Now, when you apply this calibration to other spectra, run the same steps as above to generate 'raw' [Fe/H] values (i.e., up to the point 
`Add final correction to the raw calibration`, though you can shortcut steps because you already have written out the MCMC
posteriors), and add in the following last step to the pipeline, which reads in the 
FITS file calibration and extracts and applies the corrective offset to the raw [Fe/H] values:

.. code-block:: python
    
    step = pipeline.final_corrxn.ApplyCorrxn(
        module_name="module16",
        file_name_basis_raw_retrieved_fehs="", # McD EW values
        soln_fits_name="",
        file_name_corrected_retrieved_fehs_write=""
    )

    test_gen.add_step(step)
