import high_level_reduction_accordion as pipeline

# instantiate object that will contain the series of reduction steps
test_gen = pipeline.GenerateCalib(model_choice="abcdfghk") ## ## need to let this set config file being read in (currently in __init__)

# print configuration params to log file
step = pipeline.configInit(module_name="module1")

# add step to procedure
test_gen.add_step(step)

# make all the directories
step = pipeline.makeDirs(module_name="module2")

# add step to procedure
test_gen.add_step(step)

# compile the C spectral normalization script
step = pipeline.compile_normalization.compileBkgrnd(module_name="module3")

# add step to procedure
test_gen.add_step(step)


# take list of unnormalized empirical spectra, normalize them, and write out
step = pipeline.create_spec_realizations.create_spec_realizations_main(module_name="module4", num = 1, noise_level=0.0, spec_file_type="ascii.no_header")

# add step to procedure
test_gen.add_step(step)

# run_robospect on normalized synthetic spectra
step = pipeline.run_robo.Robo(module_name="module5")

# add step to procedure
test_gen.add_step(step)
test_gen.run()
'''
# scrape_ew_from_robo and calculate EWs + err_EW
step = pipeline.scrape_ew_and_errew.Scraper(module_name="module6")

# add step to procedure
test_gen.add_step(step)

# run the pipeline
test_gen.run()
'''
