# Generates a raw calibration, based on synthetic spectra
# (raw here means 'no offset correction is applied at the very end')

import high_level_reduction_accordion as pipeline

# absolute stem of repo; needed to make dirs if they don't exist
stem_abs = "/suphys/espa3021/rrlfe/"
#stem_abs = "/Users/bandari/Documents/git.repos/rrlfe/"

# file name of list containing basenames of spectra to reduce
#spectra_basenames = "junk_test_synthetic_spectra_without_feh_m30.list"
spectra_basenames = "synthetic_spectra_without_feh_m30.list"

# instantiate object that will contain the series of reduction steps
test_gen = pipeline.GenerateCalib() ## ## need to let this set config file being read in (currently in __init__)

# print configuration params to log file
step = pipeline.ConfigInit(module_name="module1")

# add step to procedure
test_gen.add_step(step)

# compile the C spectral normalization script
step = pipeline.compile_normalization.CompileBkgrnd(
    module_name="module3", 
    cc_bkgrnd_dir=stem_abs+"src/")

# add step to procedure
test_gen.add_step(step)

# take list of unnormalized empirical spectra, normalize them, and write out
step = pipeline.create_spec_realizations.CreateSpecRealizationsMain(
    module_name="module4",
    cc_bkgrnd_dir=stem_abs+"src/",
    input_spec_list_read=stem_abs+"src/"+spectra_basenames,
    unnorm_spectra_dir_read=stem_abs+"src/model_spectra/rrmods_all/original_ascii_files/",
    unnorm_noise_churned_spectra_dir_read=stem_abs+"src/realizations_output_20230507_synthetic/",
    bkgrnd_output_dir_write=stem_abs+"rrlfe_io_20230415_synthetic/realizations_output_20230507_synthetic/norm/",
    final_spec_dir_write=stem_abs+"rrlfe_io_20230415_synthetic/realizations_output_20230507_synthetic/norm/final/",
    noise_level=0.0,
    spec_file_type="ascii.no_header",
    number_specs=1,
    verb=False)

# add step to procedure
test_gen.add_step(step)
'''
# skipping, because it takes too much time
# run_robospect on normalized synthetic spectra

step1 = pipeline.run_robo.Robo(
    module_name="module5",
    robo_dir_read="../robospect.py/",
    normzed_spec_dir_read=stem_abs+"rrlfe_io_20230415_synthetic/realizations_output_20230507_synthetic/norm/final/",
    robo_output_write=stem_abs+"rrlfe_io_20230415_synthetic/robospect_output/smo_files/")

# add step to procedure
test_gen.add_step(step1)
'''
# scrape_ew_from_robo and calculate EWs + err_EW
step = pipeline.scrape_ew_and_errew.Scraper(
    module_name="module6",
    input_spec_list_read=stem_abs+"src/"+spectra_basenames,
    robo_output_read=stem_abs+"rrlfe_io_20230415_synthetic/robospect_output/smo_files/",
    file_scraped_write=stem_abs+"rrlfe_io_20230415_synthetic/ew_products/all_ew_info.csv")

# add step to procedure
test_gen.add_step(step)

# scrape_ew_from_robo and calculate EWs + err_EW
step = pipeline.scrape_ew_and_errew.QualityCheck(
    module_name="module7",
    file_scraped_all_read=stem_abs+"rrlfe_io_20230415_synthetic/ew_products/all_ew_info.csv",
    file_scraped_good_write=stem_abs+"rrlfe_io_20230415_synthetic/ew_products/ew_info_good_only.csv")

# add step to procedure
test_gen.add_step(step)

# transpose/stack all the data, where each row corresponds to a spectrum
step = pipeline.scrape_ew_and_errew.StackSpectra(
    module_name="module8",
    input_spec_list_read=stem_abs+"src/"+spectra_basenames,
    file_ew_data_read=stem_abs+"rrlfe_io_20230415_synthetic/ew_products/ew_info_good_only.csv",
    file_restacked_write=stem_abs+"rrlfe_io_20230415_synthetic/ew_products/restacked_ew_info_good_only.csv")

# add step to procedure
test_gen.add_step(step)

# make a net Balmer line from the H-delta and H-gamma lines
step = pipeline.scrape_ew_and_errew.GenerateNetBalmer(
    module_name="module9",
    file_restacked_read=stem_abs+"rrlfe_io_20230415_synthetic/ew_products/restacked_ew_info_good_only.csv",
    file_ew_net_balmer_write=stem_abs+"rrlfe_io_20230415_synthetic/ew_products/restacked_ew_info_good_only_w_net_balmer.csv")

# add step to procedure
test_gen.add_step(step)

# take meta-data from file names of synthetic spectra and add to table
step = pipeline.scrape_ew_and_errew.AddSyntheticMetaData(
    module_name="module11",
    input_spec_list_read=stem_abs+"src/"+spectra_basenames,
    ew_data_w_net_balmer_read=stem_abs+"rrlfe_io_20230415_synthetic/ew_products/restacked_ew_info_good_only_w_net_balmer.csv",
    file_w_meta_data_write=stem_abs+"rrlfe_io_20230415_synthetic/ew_products/restacked_ew_w_metadata.csv")

# add step to procedure
test_gen.add_step(step)
'''
# add errors from other methods: noise-churning, teff-feh groups, etc.
step = pipeline.scrape_ew_and_errew.GenerateAddlEwErrors(
    module_name="module10",
    ew_data_restacked_read=stem_abs+"rrlfe_io_20230415_synthetic/ew_products/restacked_ew_w_metadata.csv",
    ew_data_w_net_balmer_read=stem_abs+"rrlfe_io_20230415_synthetic/ew_products/restacked_ew_info_good_only_w_metadata_and_net_balmer_errors.csv")

# add step to procedure
test_gen.add_step(step)

## EVERYTHING SHOULD WORK UP TO HERE

# scrape_ew_from_robo and calculate EWs + err_EW
step = pipeline.teff_retrieval.TempVsBalmer(
    module_name="module12",
    file_ew_poststack_read=stem_abs+"rrlfe_io_20230415_synthetic/ew_products/restacked_ew_info_good_only_w_metadata_and_net_balmer_errors.csv",
    file_ew_tefffit_write=stem_abs+"rrlfe_io_20230415_synthetic/ew_products/all_data_input_mcmc.csv",
    plot_tefffit_write=stem_abs+"rrlfe_io_20230415_synthetic/bin/teff_vs_balmer.png",
    data_tefffit_write=stem_abs+"rrlfe_io_20230415_synthetic/bin/teff_vs_balmer_trend.txt")

# add step to procedure
test_gen.add_step(step)

# skipping, because it takes too much time
# run_emcee
# coeff defs: K = a + bH + cF + dHF + f(H^2) + g(F^2) + h(H^2)F + kH(F^2) + m(H^3) + n(F^3)
# where K is CaII K EW; H is Balmer EW; F is [Fe/H]
step = pipeline.run_emcee.RunEmcee(
    module_name="module13",
    file_name_scraped_ews_good_only_read=stem_abs+"rrlfe_io_20230415_synthetic/ew_products/all_data_input_mcmc.csv",
    file_name_write_mcmc_text_write=stem_abs+"rrlfe_io_20230415_synthetic/bin/mcmc_output.csv")

# add step to procedure
test_gen.add_step(step)


step = pipeline.run_emcee.WriteSolnToFits(
    module_name="module14",
    file_name_mcmc_posterior_read=stem_abs+"rrlfe_io_20230415_synthetic/bin/mcmc_output.csv",
    file_name_teff_data_read=stem_abs+"rrlfe_io_20230415_synthetic/bin/teff_vs_balmer_trend.txt",
    soln_write_name=stem_abs+"rrlfe_io_20230415_synthetic/bin/calib_solution_20230415.fits")

# add step to procedure
test_gen.add_step(step)

step = pipeline.run_emcee.CornerPlot(
    module_name="module15",
    file_name_mcmc_posterior_read=stem_abs+"rrlfe_io_20230415_synthetic/bin/mcmc_output.csv",
    plot_corner_write=stem_abs+"rrlfe_io_20230415_synthetic/bin/mcmc_corner.png")

# add step to procedure
test_gen.add_step(step)


# apply the raw calibration to the McD star EW data, and find the correction based on them
# this requires a separate application script to have run on the McD data; it's too complicated to build it in here; TBD later
step = pipeline.final_corrxn.FindCorrxn(
    module_name="module16",
    file_name_basis_raw_retrieved_fehs="",
    file_name_basis_lit_fehs=stem_abs+"notebooks_for_development/mapped_program_fehs_20230402.csv",
    soln_write_name=stem_abs+"rrlfe_io_20230415_synthetic/bin/calib_solution_20230415.fits" # solution to which we will append corrxn to
)
'''
test_gen.run()