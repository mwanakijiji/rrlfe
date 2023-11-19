Prerequisites
=================

Once you have installed the software, you also need

**1. A batch of spectra** 

The spectra, which do not have to be normalized, are ascii files, each of which consists 
of whitespace-delimited columns (no headers) containing wavelength (in angstroms), flux (arbitrary), and noise 
(same units as flux), like as follows. `Here <https://raw.githubusercontent.com/mwanakijiji/rrlfe/main/src/trunc_sdss_list_single_epoch_3911_to_4950.list>`
is an example.

These files have the same format whether you are intending on generating a calibration from them, or applying a calibration to them. 
If your files are of empirical spectra (and not synthetic), we recommend that you restrict the wavelength range from 3911 to 4950 
angstroms. (We found that this resulted in the best normalization, especially given the denser lines at the Ca II K end.)

**2. A list of those spectrum file names.**

This is a comma-delimited ascii file. If you are applying a metallicity calibration to spectra, the format 
of the spectrum files includes the original spectrum file name, and additional
quantities: subtype, phase, literature [Fe/H], etc. If you don't know the quantities 
other than the original spectrum file name, just leave them blank, like in the example
 `here <https://raw.githubusercontent.com/mwanakijiji/rrlfe/main/src/mcd_final_phases_ascii_files_all_pub_20230606.list>`.

If you are generating a new calibration based on synthetic spectra, the list 
of input spectra also needs to include the parameters used to generate those 
spectra, like [Fe/H], Teff, etc. `Here <https://raw.githubusercontent.com/mwanakijiji/rrlfe/main/src/synthetic_spectra.list>` 
is an example.

**3. If a new calibration is being generated: a list of [Fe/H] values based on high-resolution spectroscopy, and low-resolution
spectra of the same stars.** 

This will enable the removal of a systematic offset in 'retrieved' vs. 'true' [Fe/H] values. 
Here `<https://raw.githubusercontent.com/mwanakijiji/rrlfe/main/src/mapped_program_fehs_20230402.csv>`  
is an example of a list of [Fe/H] values of a basis set of RR Lyrae stars, which are composite values from 
several literature high-resolution spectroscopic studies.