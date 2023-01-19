import high_level_application_accordion as pipeline

# absolute stem of repo; needed to make dirs if they don't exist
stem_abs = "/Users/bandari/Documents/git.repos/rrlfe/"

# instantiate object that will contain the series of reduction steps
test_gen = pipeline.ApplyCalib() ## ## need to let this set config file being read in (currently in __init__)

# print configuration params to log file
step = pipeline.ConfigInit(module_name="module1")

# add step to procedure
test_gen.add_step(step)

'''
# make all the directories
step = pipeline.MakeDirsConfig(module_name="module2")

# add step to procedure
test_gen.add_step(step)
'''
# compile the C spectral normalization script
step = pipeline.compile_normalization.CompileBkgrnd(module_name="module3")

# add step to procedure
test_gen.add_step(step)

'''
# take list of unnormalized empirical spectra, normalize them, and write out
step = pipeline.create_spec_realizations.CreateSpecRealizationsMain(
    module_name="module4",
    input_spec_list_read=stem_abs+"src/lamost_test_20230105.list",
    unnorm_spectra_dir_read=stem_abs+"src/lamost_spectra/",
    unnorm_noise_churned_spectra_dir_read=stem_abs+"rrlfe_io_20230105_lamost_test/realizations_output/",
    bkgrnd_output_dir_write=stem_abs+"rrlfe_io_20230105_lamost_test/realizations_output/norm/",
    final_spec_dir_write=stem_abs+"rrlfe_io_20230105_lamost_test/realizations_output/norm/final/",
    noise_level=0.0,
    spec_file_type="ascii.no_header",
    number_specs=1,
    verb=False)

# add step to procedure
test_gen.add_step(step)

# run_robospect on normalized synthetic spectra
step = pipeline.run_robo.Robo(
    module_name="module5",
    robo_dir_read="../robospect.py/",
    normzed_spec_dir_read=stem_abs+"src/lamost_20230105_normalized_rays_removed_3911_to_4950_angstr/",
    robo_output_write=stem_abs+"rrlfe_io_20230105_lamost_test/robospect_output/smo_files/")

# add step to procedure
test_gen.add_step(step)
'''
# scrape_ew_from_robo and calculate EWs + err_EW
step = pipeline.scrape_ew_and_errew.Scraper(
    module_name="module6",
    input_spec_list_read=stem_abs+"src/lamost_test_20230105.list",
    robo_output_read=stem_abs+"rrlfe_io_20230105_lamost_test/robospect_output/smo_files/",
    file_scraped_write=stem_abs+"rrlfe_io_20230105_lamost_test/ew_products/all_ew_info.csv")

# add step to procedure
test_gen.add_step(step)

# scrape_ew_from_robo and calculate EWs + err_EW
step = pipeline.scrape_ew_and_errew.QualityCheck(
    module_name="module7",
    file_scraped_all_read=stem_abs+"rrlfe_io_20230105_lamost_test/ew_products/all_ew_info.csv",
    file_scraped_good_write=stem_abs+"rrlfe_io_20230105_lamost_test/ew_products/ew_info_good_only.csv")

# add step to procedure
test_gen.add_step(step)

# transpose/stack all the data, where each row corresponds to a spectrum
step = pipeline.scrape_ew_and_errew.StackSpectra(
    module_name="module8",
    file_ew_data_read=stem_abs+"rrlfe_io_20230105_lamost_test/ew_products/ew_info_good_only.csv",
    file_restacked_write=stem_abs+"rrlfe_io_20230105_lamost_test/ew_products/restacked_ew_info_good_only.csv",
    input_spec_list_read=stem_abs+"src/lamost_test_20230105.list")

# add step to procedure
test_gen.add_step(step)

# make a net Balmer line from the H-delta and H-gamma lines
step = pipeline.scrape_ew_and_errew.GenerateNetBalmer(
    module_name="module9",
    file_restacked_read=stem_abs+"rrlfe_io_20230105_lamost_test/ew_products/restacked_ew_info_good_only.csv",
    file_ew_net_balmer_write=stem_abs+"rrlfe_io_20230105_lamost_test/ew_products/restacked_ew_info_good_only_w_net_balmer.csv")

# add step to procedure
test_gen.add_step(step)

# add errors from noise-churning (obsolete)
step = pipeline.scrape_ew_and_errew.GenerateAddlEwErrors(
    module_name="module10",
    ew_data_restacked_read=stem_abs+"rrlfe_io_20230105_lamost_test/ew_products/restacked_ew_info_good_only_w_net_balmer.csv",
    ew_data_w_net_balmer_read=stem_abs+"rrlfe_io_20230105_lamost_test/ew_products/restacked_ew_info_good_only_w_net_balmer_errors.csv")


# add step to procedure
test_gen.add_step(step)

step = pipeline.find_feh.FehRetrieval(
    module_name="module11",
    file_good_ew_read=stem_abs+"rrlfe_io_20230105_lamost_test/ew_products/restacked_ew_info_good_only_w_net_balmer_errors.csv",
    file_calib_read=stem_abs+"src/calib_solution_20220623_1.fits",
    dir_retrievals_write=stem_abs+"rrlfe_io_20230105_lamost_test/bin/pickled_info/",
    file_retrievals_write=stem_abs+"rrlfe_io_20230105_lamost_test/bin/retrieved_vals.csv")

# add step to procedure
test_gen.add_step(step)

test_gen.run()
