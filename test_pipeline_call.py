
import high_level_reduction_accordion as pipeline

# instantiate object that will contain the series of reduction steps
test_gen = pipeline.GenerateCalib(model_choice="abcdfghk")

# print configuration params to log file
step = pipeline.configInit(module_name="module1", objective = "find_calib")

# add step to procedure
test_gen.add_step(step)

# make all the directories
step = pipeline.makeDirs(module_name="module2", objective = "find_calib")

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

# run the pipeline
test_gen.run()

'''










# ------
module = pipeline.teff_retrieval.junkAccordionFcn_zap(module_name="module1")

test_gen.add_step(module)

module = pipeline.teff_retrieval.junkAccordionFcn_zap(module_name="module2")

test_gen.add_step(module)

test_gen.run()

import ipdb; ipdb.set_trace()
'''
