Prerequisites
=================

Once you have installed the software, you also need

**1. A batch of reduced spectra** that will be fed into the pipeline. The spectra are in the same format, whether you are 
intending on generating a calibration from them, or applying a calibration to them. Each file consists of whitespace-delimited
columns (no headers) containing wavelength (in angstroms), flux (arbitrary), and noise (same units as flux), like as follows:

3911.2 21154720.0 4599.426051150295
3912.6 20747450.0 4554.936882109345
3914.0 20456280.0 4522.861925816441
3915.4 20701740.0 4549.916482749985

We recommend that you restrict the wavelength range from 3911 to 4950 angstroms. (We found that this resulted in the best 
normalization, especially given the denser lines at the Ca II K end.)

**2. A list of those spectrum file names.**

If you are applying a metallicity calibration to spectra, the format 
of the spectrum files includes the original spectrum file name, and additional
quantities: subtype, phase, literature [Fe/H], etc. If you don't know the quantities 
other than the original spectrum file name, just leave them blank, like here:

orig_spec_file_name,subtype,phase,feh,err_feh
AR_Per_01.dat,,,,
AR_Per_02.dat,,,,
AR_Per_03.dat,,,,
AR_Per_04.dat,,,,

If you are generating a new calibration based on synthetic spectra, the list 
of input spectra also needs to include the parameters used to generate those 
spectra, like [Fe/H], Teff, etc:

orig_spec_file_name,subtype,phase,feh,err_feh,teff,logg,alpha
575020m05.smo,,,-0.5,0.15,5750,2.0,0.4
575020m10.smo,,,-1.0,0.15,5750,2.0,0.4
575020m15.smo,,,-1.5,0.15,5750,2.0,0.4
575020m20.smo,,,-2.0,0.15,5750,2.0,0.4