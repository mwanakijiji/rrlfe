import high_level_reduction_accordion as pipeline

# instantiate object that will contain the series of reduction steps
test_gen = pipeline.GenerateCalib() ## ## need to let this set config file being read in (currently in __init__)

# print configuration params to log file
step = pipeline.ConfigInit(module_name="module1")

# add step to procedure
test_gen.add_step(step)

# make all the directories
step = pipeline.MakeDirs(module_name="module2")

# add step to procedure
test_gen.add_step(step)

# compile the C spectral normalization script
step = pipeline.compile_normalization.CompileBkgrnd(module_name="module3")

# add step to procedure
test_gen.add_step(step)

# take list of unnormalized empirical spectra, normalize them, and write out
step = pipeline.create_spec_realizations.CreateSpecRealizationsMain(
    module_name="module4",
    input_spec_list_read="./src/junk_test_synthetic_spectra.list",
    unnorm_spectra_dir_read="./src/model_spectra/rrmods_all/original_ascii_files/",
    unnorm_noise_churned_spectra_dir_read="./src/realizations_output/",
    bkgrnd_output_dir_write="./rrlfe_io_red/realizations_output/norm/",
    final_spec_dir_write="./rrlfe_io_red/realizations_output/norm/final/",
    noise_level=0.0,
    spec_file_type="ascii.no_header",
    number_specs=1,
    verb=False)

# add step to procedure
test_gen.add_step(step)
''' # skipping, because it takes too much time
# run_robospect on normalized synthetic spectra
step = pipeline.run_robo.Robo(
    module_name="module5",
    robo_dir_read="../robospect.py/",
    normzed_spec_dir_read="./rrlfe_io_red/realizations_output/norm/final/",
    robo_output_write="./rrlfe_io_red/robospect_output/smo_files/")

# add step to procedure
test_gen.add_step(step)
'''
# scrape_ew_from_robo and calculate EWs + err_EW
step = pipeline.scrape_ew_and_errew.Scraper(
    module_name="module6",
    robo_output_read="./rrlfe_io_red/robospect_output/smo_files/",
    file_scraped_write="./rrlfe_io_red/ew_products/all_ew_info.csv",
    input_spec_list_read="./src/junk_test_synthetic_spectra.list"
    )

# add step to procedure
test_gen.add_step(step)

# scrape_ew_from_robo and calculate EWs + err_EW
step = pipeline.scrape_ew_and_errew.QualityCheck(
    module_name="module7",
    file_scraped_all_read="./rrlfe_io_red/ew_products/all_ew_info.csv",
    file_scraped_good_write="./rrlfe_io_red/ew_products/ew_info_good_only.csv")

# add step to procedure
test_gen.add_step(step)

# transpose/stack all the data, where each row corresponds to a spectrum
step = pipeline.scrape_ew_and_errew.StackSpectra(
    module_name="module8",
    file_ew_data_read="./rrlfe_io_red/ew_products/ew_info_good_only.csv",
    file_restacked_write="./rrlfe_io_red/ew_products/restacked_ew_info_good_only.csv",
    input_spec_list_read="./src/junk_test_synthetic_spectra.list")

# add step to procedure
test_gen.add_step(step)

# make a net Balmer line from the H-delta and H-gamma lines
step = pipeline.scrape_ew_and_errew.GenerateNetBalmer(
    module_name="module9",
    file_restacked_read="./rrlfe_io_red/ew_products/restacked_ew_info_good_only.csv",
    file_ew_net_balmer_write="./rrlfe_io_red/ew_products/restacked_ew_info_good_only_w_net_balmer.csv")

# add step to procedure
test_gen.add_step(step)
'''
# add errors from noise-churning (obsolete)
step = pipeline.scrape_ew_and_errew.GenerateAddlEwErrors(module_name="module10")

# add step to procedure
test_gen.add_step(step)

# take meta-data from file names of synthetic spectra and add to table
step = pipeline.scrape_ew_and_errew.AddSyntheticMetaData(module_name="module11")

# add step to procedure
test_gen.add_step(step)

# scrape_ew_from_robo and calculate EWs + err_EW
step = pipeline.teff_retrieval.TempVsBalmer(module_name="module12")

# add step to procedure
test_gen.add_step(step)

# run_emcee
# coeff defs: K = a + bH + cF + dHF + f(H^2) + g(F^2) + h(H^2)F + kH(F^2) + m(H^3) + n(F^3)
# where K is CaII K EW; H is Balmer EW; F is [Fe/H]
step = pipeline.run_emcee.RunEmcee(module_name="module13")

# add step to procedure
test_gen.add_step(step)

step = pipeline.run_emcee.WriteSolnToFits(module_name="module14")

# add step to procedure
test_gen.add_step(step)

step = pipeline.run_emcee.CornerPlot(module_name="module15")

# add step to procedure
test_gen.add_step(step)
'''

test_gen.run()
