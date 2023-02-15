import numpy as np
import pandas as pd
import logging
import matplotlib.pyplot as plt
from astropy.io import fits


class FindCorrxn:
    """
    Applies raw calibration to an empirical dataset and generates a correction

    Parameters:
        module_name (str): module name
        file_name_basis_raw_retrieved_fehs (str): file name of retrieved Fe/Hs
        file_name_basis_lit_fehs (str): file name of literature values based on high-res specs
        soln_write_name (str): file name containing empirical [Fe/H] values for stars
        
    Returns:
        writes correction to FITS file solution
    """

    def __init__(self, 
                module_name, 
                file_name_basis_raw_retrieved_fehs, 
                file_name_basis_lit_fehs,
                soln_write_name):

        self.name = module_name
        self.file_name_basis_raw_retrieved_fehs = file_name_basis_raw_retrieved_fehs
        self.file_name_basis_lit_fehs = file_name_basis_lit_fehs
        self.soln_write_name = soln_write_name

    def run_step(self, attribs = None):
        '''
        Finds residual between rrlfe and SSPP values
        
        INPUTS:
        vals_sspp: basis (probably mapped McDonald) [Fe/H] values (x); these are the ones we want to map onto
        vals_rrlfe: rrlfe [Fe/H] values (y)
        
        RETURNS:
        values of rrlfe [Fe/H] mapped onto SSPP
        '''

        df_raw_retrieved = pd.read_csv(self.file_name_basis_raw_retrieved_fehs) # raw values retrieved with rrlfe
        df_basis = pd.read_csv(self.file_name_basis_lit_fehs) # based on high-res spectroscopy from the literature

        # average the high-res values for each 

        ## make matching
        df_raw_retrieved['name_match'] = df_raw_retrieved['orig_spec_file_name'].str[:6].str.rstrip('_')
        df_raw_retrieved['name_match'].loc[df_raw_retrieved['name_match'] == 'V445_O'] = 'V445_Oph' # to make the name matching for this star to work right

        df_merged = df_raw_retrieved[['name_match','feh_retrieved']].merge(df_basis[['name_match','feh']], on='name_match', how='inner')
        df_merged.rename(columns={'feh': 'feh_lit'}, inplace=True) # rename for clarity
        ##

        vals_basis = df_merged['feh_lit'].values
        vals_rrlfe = df_merged['feh_retrieved'].values

        # initial best fit between rrlfe vs. SSPP
        m_b, b_b = np.polyfit(vals_basis,vals_rrlfe,1) # _b: best-fit
        
        # find residual best-fit line
        resids = (m_b-1)*vals_basis + b_b

        # read in raw FITS calibration
        hdul = fits.open(self.soln_write_name)
        #hdu = hdul[0].header
        #hdul.set('CORRXN_SLOPE_M','CORRXN_YINT_B')
        hdul[1].header["CO_SLP_M"] = (m_b, "Slope of raw rrlfe Fe/H vs. high-res spc")
        hdul[1].header["CO_YIN_B"] = (b_b, "Y-intercept of raw rrlfe Fe/H vs. high-res spc")
        hdul.writeto(self.soln_write_name, overwrite=True)

        logging.info("Appended final calibration correction to " + self.soln_write_name)

        '''
        plt.scatter(vals_sspp,vals_rrlfe)
        plt.plot([-2.8,0.3],[-2.8,0.3],linestyle=":")
        plt.plot(vals_sspp, m_b*vals_sspp + b_b,linestyle="--")
        plt.scatter(vals_sspp, rrlfe_corrected(vals_sspp, vals_rrlfe),linestyle="--", color="red")
        plt.show()
        '''
        
        ## ## CONTINUE HERE; need to append coeffs to FITS file, rather than just returning resids (except for testing) ## ##
        # return the empirical values with the residuals-to-1-to-1-line subtracted out
        return vals_rrlfe - resids