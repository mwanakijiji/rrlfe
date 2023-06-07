# Applies a raw correction based on synthetic data to the McDonald dataset,
# and then generates the offset correction given overlapping stars in high-res
# spectroscopy literature

import high_level_application_accordion as pipeline

# absolute stem of repo; needed to make dirs if they don't exist
stem_abs = "/suphys/espa3021/Documents/git.repos/rrlfe/"
#stem_abs = "/Users/bandari/Documents/git.repos/rrlfe/"
#stem_abs = "/home/prunelle/rrlfe/"

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
step = pipeline.compile_normalization.CompileBkgrnd(
    module_name="module3", 
    cc_bkgrnd_dir=stem_abs+"src/")

# add step to procedure
test_gen.add_step(step)
'''
# take list of unnormalized empirical spectra, normalize them, and write out
step = pipeline.create_spec_realizations.CreateSpecRealizationsMain(
    module_name="module4",
    cc_bkgrnd_dir=stem_abs+"src/",
    input_spec_list_read=stem_abs+"src/mcd_final_phases_ascii_files_all.list",
    unnorm_spectra_dir_read=stem_abs+"src/mcdonald_spectra/",
    unnorm_noise_churned_spectra_dir_read=stem_abs+"rrlfe_io_20230510_mcd_raw/realizations_output/",
    bkgrnd_output_dir_write=stem_abs+"rrlfe_io_20230510_mcd_raw/realizations_output/norm/",
    final_spec_dir_write=stem_abs+"rrlfe_io_20230510_mcd_raw/realizations_output/norm/final/",
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
    normzed_spec_dir_read=stem_abs+"rrlfe_io_20230510_mcd_raw/realizations_output/norm/final/",
    robo_output_write=stem_abs+"rrlfe_io_20230510_mcd_raw/robospect_output/smo_files/")

# add step to procedure
test_gen.add_step(step)

# scrape_ew_from_robo and calculate EWs + err_EW
step = pipeline.scrape_ew_and_errew.Scraper(
    module_name="module6",
    input_spec_list_read=stem_abs+"src/mcd_final_phases_ascii_files_all.list",
    robo_output_read=stem_abs+"rrlfe_io_20230510_mcd_raw/robospect_output/smo_files/",
    file_scraped_write=stem_abs+"rrlfe_io_20230510_mcd_raw/ew_products/all_ew_info.csv")

# add step to procedure
test_gen.add_step(step)

# scrape_ew_from_robo and calculate EWs + err_EW
step = pipeline.scrape_ew_and_errew.QualityCheck(
    module_name="module7",
    file_scraped_all_read=stem_abs+"rrlfe_io_20230510_mcd_raw/ew_products/all_ew_info.csv",
    file_scraped_good_write=stem_abs+"rrlfe_io_20230510_mcd_raw/ew_products/ew_info_good_only.csv")

# add step to procedure
test_gen.add_step(step)

# transpose/stack all the data, where each row corresponds to a spectrum
step = pipeline.scrape_ew_and_errew.StackSpectra(
    module_name="module8",
    file_ew_data_read=stem_abs+"rrlfe_io_20230510_mcd_raw/ew_products/ew_info_good_only.csv",
    file_restacked_write=stem_abs+"rrlfe_io_20230510_mcd_raw/ew_products/restacked_ew_info_good_only.csv",
    input_spec_list_read=stem_abs+"src/mcd_final_phases_ascii_files_all.list")

# add step to procedure
test_gen.add_step(step)

# make a net Balmer line from the H-delta and H-gamma lines
step = pipeline.scrape_ew_and_errew.GenerateNetBalmer(
    module_name="module9",
    file_restacked_read=stem_abs+"rrlfe_io_20230510_mcd_raw/ew_products/restacked_ew_info_good_only.csv",
    file_ew_net_balmer_write=stem_abs+"rrlfe_io_20230510_mcd_raw/ew_products/restacked_ew_info_good_only_w_net_balmer.csv")

# add step to procedure
test_gen.add_step(step)

# add errors from noise-churning (obsolete)
step = pipeline.scrape_ew_and_errew.GenerateAddlEwErrors(
    module_name="module10",
    ew_data_restacked_read=stem_abs+"rrlfe_io_20230510_mcd_raw/ew_products/restacked_ew_info_good_only_w_net_balmer.csv",
    ew_data_w_net_balmer_read=stem_abs+"rrlfe_io_20230510_mcd_raw/ew_products/restacked_ew_info_good_only_w_net_balmer_errors.csv")


# add step to procedure
test_gen.add_step(step)

step = pipeline.find_feh.FehRetrieval(
    module_name="module11",
    file_good_ew_read=stem_abs+"rrlfe_io_20230510_mcd_raw/ew_products/restacked_ew_info_good_only_w_net_balmer_errors.csv",
    file_calib_read=stem_abs+"rrlfe_io_20230507_synthetic/bin/calib_solution_20230507.fits",
    dir_retrievals_write=stem_abs+"rrlfe_io_20230510_mcd_raw/bin/pickled_info/",
    file_retrievals_write=stem_abs+"rrlfe_io_20230510_mcd_raw/bin/retrieved_vals.csv")

# add step to procedure
test_gen.add_step(step)

'''
# apply the raw calibration to the McD star EW data, and find the correction based on them
# this requires a separate application script to have run on the McD data; it's too complicated to build it in here; TBD later
step = pipeline.final_corrxn.FindCorrxn(
    module_name="module16",
    file_name_basis_raw_retrieved_fehs=stem_abs+"rrlfe_io_20230510_mcd_raw/bin/retrieved_vals.csv", # retrieved McD Fe/H values based on raw rrlfe calibration
    file_name_basis_lit_fehs=stem_abs+"notebooks_for_development/mapped_program_fehs_20230402.csv", # mapped high-res literature Fe/H values for McD stars
    soln_write_name=stem_abs+"rrlfe_io_20230507_synthetic/bin/calib_solution_20230507.fits" # raw calibration which is applied, and to which corrxn is appended to
)

# add step to procedure
test_gen.add_step(step)

test_gen.run()
