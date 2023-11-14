import high_level_generation_accordion as pipeline

# absolute stem of repo; needed to make dirs if they don't exist
stem_abs = "/suphys/espa3021/Documents/git.repos/rrlfe/"
#stem_abs = "/Users/bandari/Documents/git.repos/rrlfe/"
#stem_abs = "/home/prunelle/rrlfe/"

# string for the upper level directory
stem_string = 'rrlfe_io_generation_test_20231112/'

# instantiate object that will contain the series of reduction steps
test_gen = pipeline.GenerateCalib()

# print configuration params to log file
step = pipeline.ConfigInit(module_name="module1")

'''
step = pipeline.run_emcee.WriteSolnToFits(
    module_name="module14",
    file_name_mcmc_posterior_read=stem_abs+stem_string+"bin/mcmc_output.csv",
    file_name_teff_data_read=stem_abs+stem_string+"bin/teff_vs_balmer_trend.txt",
    soln_write_name=stem_abs+stem_string+"bin/calib_solution.fits")
'''
# add step to procedure
test_gen.add_step(step)

step = pipeline.run_emcee.CornerPlot(
    module_name="module15",
    file_name_mcmc_posterior_read=stem_abs+stem_string+"bin/mcmc_output.csv",
    plot_corner_write=stem_abs+stem_string+"bin/mcmc_corner.png")

# add step to procedure
test_gen.add_step(step)

'''
# apply the final correction, as based on comparisons of [Fe/H] values from high-res spectroscopy
# and from low resolution spectra taken at McDonald Observatory 
step = pipeline.final_corrxn.ApplyCorrxn(
    module_name="module16",
    file_name_mcd_lit_fehs="", # McD EW values
    soln_write_name=stem_abs+"rrlfe_io_red/bin/calib_solution.fits" # solution to which we will append corrxn to
)


# add step to procedure
test_gen.add_step(step)
'''

'''
        module_name (str): module name
        file_name_basis_raw_retrieved_fehs (str): file name of raw retrieved Fe/Hs
        soln_fits_name (str): file name containing the raw calibration as a binary table,
            and the correction in the header
        file_name_corrected_retrieved_fehs_write (str): file name of the Fe/Hs with col
            of corrected Fe/Hs
'''
test_gen.run()
