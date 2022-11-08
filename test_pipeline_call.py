
import high_level_reduction_accordion as pipeline
import ipdb; ipdb.set_trace()
# instantiate object that will contain the series of reduction steps
test_gen = pipeline.GenerateCalib(model_choice="abcdfghk")

# print configuration params to log file
step = pipeline.config_init(objective = "find_calib", module_name="module1")

# add step to procedure
test_gen.add_step(step)

# make all the directories
step = pipeline.make_dirs(objective = "find_calib")

# add step to procedure
test_gen.add_step(step)

# run the pipeline
test_gen.run()

'''
# compile the C spectral normalization script
pipeline.compile_normalization.compile_bkgrnd()

# take list of unnormalized empirical spectra, normalize them, and write out
pipeline.create_spec_realizations.create_spec_realizations_main(num = 1, noise_level=0.0, spec_file_type="ascii.no_header")

# run_robospect on normalized synthetic spectra
pipeline.run_robo.main()



# ------
module = pipeline.teff_retrieval.junkAccordionFcn_zap(module_name="module1")

test_gen.add_step(module)

module = pipeline.teff_retrieval.junkAccordionFcn_zap(module_name="module2")

test_gen.add_step(module)

test_gen.run()

import ipdb; ipdb.set_trace()
'''
