from rrlfe import high_level_application_accordion as pipeline

# absolute stem of repo; needed to make dirs if they don't exist
#stem_abs = "/suphys/espa3021/Desktop/sandbox/"
stem_abs = "/Users/myname/directory1/directory2/rrlfe/"

# string for the upper level directory
stem_string = 'rrlfe_io/'

# calibration solution to use
calib_soln = 'deg_1-100_calib_solution_20230507.fits'

# instantiate object that will contain the series of reduction steps
test_gen = pipeline.ApplyCalib()

# print configuration params to log file
step = pipeline.ConfigInit(module_name="module1")

# add step to procedure
test_gen.add_step(step)

# compile the C spectral normalization script and define directory in which to place the binary
step = pipeline.compile_normalization.CompileBkgrnd(
    module_name="module3",
    cc_bkgrnd_dir=stem_abs+"src/")

# add step to procedure
test_gen.add_step(step)

# take list of unnormalized empirical spectra, normalize them, and write out
step = pipeline.create_spec_realizations.CreateSpecRealizationsMain(
    module_name="module4",
    cc_bkgrnd_dir=stem_abs+"src/",
    input_spec_list_read=stem_abs+"src/original_ascii_files.list",
    unnorm_spectra_dir_read=stem_abs+"src/original_ascii_files/",
    unnorm_noise_churned_spectra_dir_read=stem_abs+stem_string+"realizations_output/",
    bkgrnd_output_dir_write=stem_abs+stem_string+"realizations_output/norm/",
    final_spec_dir_write=stem_abs+stem_string+"realizations_output/norm/final/",
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
    normzed_spec_dir_read=stem_abs+stem_string+"realizations_output/norm/final/",
    robo_output_write=stem_abs+stem_string+"robospect_output/smo_files/")

# add step to procedure
test_gen.add_step(step)

# scrape_ew_from_robo and calculate EWs + err_EW
step = pipeline.scrape_ew_and_errew.Scraper(
    module_name="module6",
    input_spec_list_read=stem_abs+"src/original_ascii_files.list",
    robo_output_read=stem_abs+stem_string+"robospect_output/smo_files/",
    file_scraped_write=stem_abs+stem_string+"ew_products/all_ew_info.csv")

# add step to procedure
test_gen.add_step(step)

# scrape_ew_from_robo and calculate EWs + err_EW
step = pipeline.scrape_ew_and_errew.QualityCheck(
    module_name="module7",
    file_scraped_all_read=stem_abs+stem_string+"ew_products/all_ew_info.csv",
    file_scraped_good_write=stem_abs+stem_string+"ew_products/ew_info_good_only.csv")

# add step to procedure
test_gen.add_step(step)

# transpose/stack all the data, where each row corresponds to a spectrum
step = pipeline.scrape_ew_and_errew.StackSpectra(
    module_name="module8",
    file_ew_data_read=stem_abs+stem_string+"ew_products/ew_info_good_only.csv",
    file_restacked_write=stem_abs+stem_string+"ew_products/restacked_ew_info_good_only.csv",
    input_spec_list_read=stem_abs+"src/original_ascii_files.list")

# add step to procedure
test_gen.add_step(step)

# make a net Balmer line from the H-delta and H-gamma lines
step = pipeline.scrape_ew_and_errew.GenerateNetBalmer(
    module_name="module9",
    file_restacked_read=stem_abs+stem_string+"ew_products/restacked_ew_info_good_only.csv",
    file_ew_net_balmer_write=stem_abs+stem_string+"ew_products/restacked_ew_info_good_only_w_net_balmer.csv")

# add step to procedure
test_gen.add_step(step)

# add errors from noise-churning
step = pipeline.scrape_ew_and_errew.GenerateAddlEwErrors(
    module_name="module10",
    ew_data_restacked_read=stem_abs+stem_string+"ew_products/restacked_ew_info_good_only_w_net_balmer.csv",
    ew_data_w_net_balmer_read=stem_abs+stem_string+"ew_products/restacked_ew_info_good_only_w_net_balmer_errors.csv")


# add step to procedure
test_gen.add_step(step)

step = pipeline.find_feh.FehRetrieval(
    module_name="module11",
    file_good_ew_read=stem_abs+stem_string+"ew_products/restacked_ew_info_good_only_w_net_balmer_errors.csv",
    file_calib_read=stem_abs+"src/"+calib_soln,
    dir_retrievals_write=stem_abs+stem_string+"bin/pickled_info/",
    file_retrievals_write=stem_abs+stem_string+"bin/retrieved_vals.csv")

# add step to procedure
test_gen.add_step(step)

# apply final correction
step = pipeline.final_corrxn.ApplyCorrxn(
    module_name="module16",
    file_name_basis_raw_retrieved_fehs=stem_abs+stem_string+"bin/retrieved_vals.csv", # retrieved McD Fe/H values based on raw rrlfe calibration
    soln_fits_name=stem_abs+"src/"+calib_soln, # calibration file which includes correction info in the header
    file_name_corrected_retrieved_fehs_write=stem_abs+stem_string+"bin/retrieved_vals_corrected.csv" # mapped high-res literature Fe/H values for McD stars
)

# add step to procedure
test_gen.add_step(step)

test_gen.run()
