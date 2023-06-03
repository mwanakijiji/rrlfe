#!/usr/bin/env python
# coding: utf-8

# This makes a plot in the style of Fig. 1 in Pancino+ 2015, to
# give readers a sense of the phase coverage of our program stars.

# created 2019 July 1 by E.S.

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec

# all program stars

cases = ["RW Ari", "X Ari", "UY Cam",
         "RR Cet", "SV Eri", "VX Her",
         "RR Leo", "TT Lyn", "TV Lyn",
         "TW Lyn", "RR Lyr", "V535 Mon",
         "V445 Oph", "AV Peg", "BH Peg",
         "AR Per", "RU Psc", "T Sex",
         "TU UMa", "All RRabs", "All RRcs"]

bad_phase_region = [0.90,0.05]
greyness_alpha = 0.3

cols = 3
rows = 7

# set the spacing between axes

#gs1 = gridspec.GridSpec(rows, cols)
#gs1.update(wspace=0.0, hspace=0.05)

# define a normalization function

def normalize_curve(df_unnorm_photom, df_unnorm_spline, mag=True, nospline=False):
    '''
    Takes unnormalized light curves and normalizes them. This is done both for
    photometry and the spline fit, by using the spline's specs.

    INPUTS:
    df_unnorm_photom: dataframe containing empirical photometry
    df_unnorm_spline: dataframe containing spline
    mag: if true, input data is in magnitude space (as opposed to flux)
    nospline: if true, there is no spline data at all (and second input is just a dummy)
    '''

    if nospline:
        # if there is no spline data (input data will be in mags, presumably, since this is from AAVSO)

        # subtract offset from zero
        y_photom_mag_unnorm_offset = np.subtract(df_unnorm_photom["Mag"],np.min(df_unnorm_photom["Mag"]))

        df_unnorm_photom["y_photom_norm"] = np.divide(y_photom_mag_unnorm_offset,np.max(y_photom_mag_unnorm_offset))

        df_join = df_unnorm_photom.copy(deep=True)

        # normalize
        #df_unnorm_photom["y_photom_norm"] = np.divide(y_photom_mag_unnorm_offset,np.max(y_spline_mag_unnorm_offset))


    elif nospline==False:
        # if there is spline data

        if not mag:
            # if input is in flux
            df_unnorm_photom["Mag"] = -2.5*np.log10(np.divide(df_unnorm_photom["Flux"],np.min(df_unnorm_spline["Flux"])))
            df_unnorm_spline["Mag"] = -2.5*np.log10(np.divide(df_unnorm_spline["Flux"],np.min(df_unnorm_spline["Flux"])))

        # subtract offset from zero
        y_photom_mag_unnorm_offset = np.subtract(df_unnorm_photom["Mag"],np.min(df_unnorm_spline["Mag"]))
        y_spline_mag_unnorm_offset = np.subtract(df_unnorm_spline["Mag"],np.min(df_unnorm_spline["Mag"]))

        # normalize
        df_unnorm_photom["y_photom_norm"] = np.divide(y_photom_mag_unnorm_offset,np.max(y_spline_mag_unnorm_offset))
        df_unnorm_spline["Phase"] = df_unnorm_spline["#Phase"] # kludge
        df_unnorm_spline["y_spline_norm"] = np.divide(y_spline_mag_unnorm_offset,np.max(y_spline_mag_unnorm_offset))
        df_photom_new = df_unnorm_photom[['Phase', 'y_photom_norm']].copy()
        df_spline_new = df_unnorm_spline[['Phase', 'y_spline_norm']].copy()

        # join
        df_join = df_photom_new.set_index("Phase").join(df_spline_new.set_index("Phase"), on="Phase", how="outer")
        df_join.reset_index(inplace=True) # (otherwise phase is a key)

    # return table with photometric table, with spline added in
    return df_join

# read in data
df_phases = pd.read_csv("./data/phases_all_master_no_repeat_fits.csv")

# read in lightcurves
stem_phased_curves = "/Users/bandari/Documents/git.repos/rrlfe/notebooks_for_development/data/"

df_rw_ari = pd.read_csv(stem_phased_curves + "ndl_phased_curves_20220609/TESS_Phased_Curves/LC_RW_Ari.cur_0.sp.phase",
                        delim_whitespace=True)
df_rw_ari_spline = pd.read_csv(stem_phased_curves + "phase_folded_curves/LC_RW_Ari.cur_0.spl")

df_bh_peg = pd.read_csv("./data/phase_folded_curves/Phased_BH_Peg_aavso.dat",
                        delimiter=",")
df_bh_peg_spline = pd.read_csv(stem_phased_curves + "ndl_phased_curves_20220609/AAVSO_Phased_Curves/bh_peg_aavso_polished_truncated_ingest.txt_0.spl",
                        delimiter=",")
df_vx_her = pd.read_csv(stem_phased_curves + "ndl_phased_curves_20220609/AAVSO_Phased_Curves/vx_her_aavso_polished_ingest.fixed.txt_0.sp.phase",
                        delim_whitespace=True)
df_vx_her_spline = pd.read_csv(stem_phased_curves + "ndl_phased_curves_20220609/AAVSO_Phased_Curves/vx_her_aavso_polished_ingest.fixed.txt_0.spl",
                        delimiter=",")
df_rr_cet = pd.read_csv(stem_phased_curves + "ndl_phased_curves_20220609/TESS_Phased_Curves/LC_RR_Cet.cur_0.sp.phase",
                        delim_whitespace=True)
df_rr_cet_spline = pd.read_csv(stem_phased_curves + "phase_folded_curves/LC_RR_Cet.cur_0.spl")

df_sv_eri = pd.read_csv(stem_phased_curves + "ndl_phased_curves_20220609/TESS_Phased_Curves/LC_SV_Eri.cur_0.sp.phase",
                        delim_whitespace=True)
df_sv_eri_spline = pd.read_csv(stem_phased_curves + "phase_folded_curves/LC_SV_Eri.cur_0.spl")

df_x_ari = pd.read_csv(stem_phased_curves + "ndl_phased_curves_20220609/TESS_Phased_Curves/LC_X_Ari.cur_0.sp.phase",
                       delim_whitespace=True)
df_x_ari_spline = pd.read_csv(stem_phased_curves + "phase_folded_curves/LC_X_Ari.cur_0.spl")

df_t_sex = pd.read_csv(stem_phased_curves + "ndl_phased_curves_20220609/TESS_Phased_Curves/LC_T_Sex.cur_0.sp.phase",
                       delim_whitespace=True)
df_t_sex_spline = pd.read_csv(stem_phased_curves + "phase_folded_curves/LC_T_Sex.cur_0.spl")

df_uy_cam = pd.read_csv(stem_phased_curves + "ndl_phased_curves_20220609/TESS_Phased_Curves/LC_UY_Cam.cur_0.sp.phase",
                        delim_whitespace=True)
df_uy_cam_spline = pd.read_csv(stem_phased_curves + "phase_folded_curves/LC_UY_Cam.cur_0.spl")

df_v535_mon = pd.read_csv(stem_phased_curves + "ndl_phased_curves_20220715/KELT_Phased_Curves/V535_Mon_W_small.cur_0.sp.phase",
                          delim_whitespace=True)
df_v535_mon_spline = pd.read_csv(stem_phased_curves + "phase_folded_curves/V535_Mon_W_small.cur_0.spl")

df_tt_lyn = pd.read_csv(stem_phased_curves + "ndl_phased_curves_20220609/TESS_Phased_Curves/LC_TT_Lyn.cur_0.sp.phase",
                          delim_whitespace=True)
df_tt_lyn_spline = pd.read_csv(stem_phased_curves + "phase_folded_curves/LC_TT_Lyn.cur_0.spl")

df_tv_lyn = pd.read_csv(stem_phased_curves + "ndl_phased_curves_20220609/TESS_Phased_Curves/LC_TV_Lyn.cur_0.sp.phase",
                          delim_whitespace=True)
df_tv_lyn_spline = pd.read_csv(stem_phased_curves + "phase_folded_curves/LC_TV_Lyn.cur_0.spl")

df_rr_leo = pd.read_csv(stem_phased_curves + "ndl_phased_curves_20220609/TESS_Phased_Curves/LC_RR_Leo.cur_0.sp.phase",
                          delim_whitespace=True)
df_rr_leo_spline = pd.read_csv(stem_phased_curves + "phase_folded_curves/LC_RR_Leo.cur_0.spl")

df_rr_lyr = pd.read_csv(stem_phased_curves + "ndl_phased_curves_20220609/TESS_Phased_Curves/LC_RR_Lyr.cur_0.sp.phase",
                          delim_whitespace=True)
df_rr_lyr_spline = pd.read_csv(stem_phased_curves + "phase_folded_curves/LC_RR_Lyr.cur_0.spl")

df_tw_lyn = pd.read_csv(stem_phased_curves + "ndl_phased_curves_20220609/TESS_Phased_Curves/LC_TW_Lyn.cur_0.sp.phase",
                          delim_whitespace=True)
df_tw_lyn_spline = pd.read_csv(stem_phased_curves + "phase_folded_curves/LC_TW_Lyn.cur_0.spl")

df_tu_uma = pd.read_csv(stem_phased_curves + "ndl_phased_curves_20220609/TESS_Phased_Curves/LC_TU_UMa.cur_0.sp.phase",
                          delim_whitespace=True)
df_tu_uma_spline = pd.read_csv(stem_phased_curves + "phase_folded_curves/LC_TU_UMa.cur_0.spl")

df_v445_oph = pd.read_csv(stem_phased_curves + "ndl_phased_curves_20220609/KELT_Phased_Curves/V445_Oph_E.cur_0.sp.phase",
                        delim_whitespace=True)
df_v445_oph_spline = pd.read_csv(stem_phased_curves + "phase_folded_curves/V445_Oph_E.cur_1.spl")

df_av_peg = pd.read_csv(stem_phased_curves + "ndl_phased_curves_20220609/KELT_Phased_Curves/AV_Peg_E.cur_0.sp.phase",
                        delim_whitespace=True)
df_av_peg_spline = pd.read_csv(stem_phased_curves + "phase_folded_curves/AV_Peg_E.cur_1.spl")

df_ar_per = pd.read_csv(stem_phased_curves + "ndl_phased_curves_20220609/KELT_Phased_Curves/AR_Per_E.cur_0.sp.phase",
                        delim_whitespace=True)
df_ar_per_spline = pd.read_csv(stem_phased_curves + "phase_folded_curves/AR_Per_E.cur_1.spl")

df_ru_psc = pd.read_csv(stem_phased_curves + "ndl_phased_curves_20220609/KELT_Phased_Curves/RU_Psc_E_small.cur_0.sp.phase",
                        delim_whitespace=True)
df_ru_psc_spline = pd.read_csv(stem_phased_curves + "phase_folded_curves/RU_Psc_E_small.cur_0.spl")


idx_rw_ari = df_phases["star_match"] == "RW Ari"
idx_rr_cet = df_phases["star_match"] == "RR Cet"
idx_sv_eri = df_phases["star_match"] == "SV Eri"
idx_x_ari = df_phases["star_match"] == "X Ari"
idx_t_sex = df_phases["star_match"] == "T Sex"
idx_uy_cam = df_phases["star_match"] == "UY Cam"
idx_v535_mon = df_phases["star_match"] == "V 535"
idx_tt_lyn = df_phases["star_match"] == "TT Lyn"
idx_tv_lyn = df_phases["star_match"] == "TV Lyn"
idx_rr_leo = df_phases["star_match"] == "RR Leo"
idx_rr_lyr = df_phases["star_match"] == "RR Lyr"
idx_tw_lyn = df_phases["star_match"] == "TW Lyn"
idx_tu_uma = df_phases["star_match"] == "TU UMa"
idx_ru_psc = df_phases["star_match"] == "RU Psc"
idx_v445_oph = df_phases["star_match"] == "V445 O"
idx_av_peg = df_phases["star_match"] == "AV Peg"
idx_ar_per = df_phases["star_match"] == "AR Per"
idx_bh_peg = df_phases["star_match"] == "BH Peg"
idx_vx_her = df_phases["star_match"] == "VX Her"


# normalize
df_rw_ari_spline["Flux"] = df_rw_ari_spline["Mag"] # kludge because of mislabeling in input file
df_rw_ari = normalize_curve(df_rw_ari, df_rw_ari_spline, mag=False)

df_rr_cet_spline["Flux"] = df_rr_cet_spline["Mag"]
df_rr_cet = normalize_curve(df_rr_cet, df_rr_cet_spline, mag=False)

df_sv_eri_spline["Flux"] = df_sv_eri_spline["Mag"]
df_sv_eri = normalize_curve(df_sv_eri, df_sv_eri_spline, mag=False)

df_x_ari_spline["Flux"] = df_x_ari_spline["Mag"]
df_x_ari = normalize_curve(df_x_ari, df_x_ari_spline, mag=False)

df_t_sex_spline["Flux"] = df_t_sex_spline["Mag"]
df_t_sex = normalize_curve(df_t_sex, df_t_sex_spline, mag=False)

df_uy_cam_spline["Flux"] = df_uy_cam_spline["Mag"]
df_uy_cam = normalize_curve(df_uy_cam, df_uy_cam_spline, mag=False)

df_v535_mon_spline["Flux"] = df_v535_mon_spline["Mag"]
df_v535_mon = normalize_curve(df_v535_mon, df_v535_mon_spline, mag=True)

df_tv_lyn_spline["Flux"] = df_tv_lyn_spline["Mag"]
df_tv_lyn = normalize_curve(df_tv_lyn, df_tv_lyn_spline, mag=False)

df_tt_lyn_spline["Flux"] = df_tt_lyn_spline["Mag"]
df_tt_lyn = normalize_curve(df_tt_lyn, df_tt_lyn_spline, mag=False)

df_rr_leo_spline["Flux"] = df_rr_leo_spline["Mag"]
df_rr_leo = normalize_curve(df_rr_leo, df_rr_leo_spline, mag=False)

df_rr_lyr_spline["Flux"] = df_rr_lyr_spline["Mag"]
df_rr_lyr = normalize_curve(df_rr_lyr, df_rr_lyr_spline, mag=False)

df_tw_lyn_spline["Flux"] = df_tw_lyn_spline["Mag"]
df_tw_lyn = normalize_curve(df_tw_lyn, df_tw_lyn_spline, mag=False)

df_tu_uma_spline["Flux"] = df_tu_uma_spline["Mag"]
df_tu_uma = normalize_curve(df_tu_uma, df_tu_uma_spline, mag=False)

df_v445_oph = normalize_curve(df_v445_oph, df_v445_oph_spline)

df_av_peg = normalize_curve(df_av_peg, df_av_peg_spline)

df_ar_per = normalize_curve(df_ar_per, df_ar_per_spline)

df_ru_psc = normalize_curve(df_ru_psc, df_ru_psc_spline)

df_bh_peg["Mag"] = df_bh_peg["mag"] # kludge
df_bh_peg["Phase"] = df_bh_peg["phase"]
df_bh_peg = normalize_curve(df_bh_peg, df_bh_peg_spline)

#df_vx_her_spline["Mag"] = df_vx_her_spline[""]

#df_vx_her["phase"] = df_vx_her["#Phase"] # kludge
df_vx_her = normalize_curve(df_vx_her, df_vx_her_spline, mag=True)

# fake data
example_phase_phases_star_1 = [0.1,0.45,0.77,0.98]
x = np.linspace(0,1.,num=50)
y = np.sin(x)


# used some code from
# https://matplotlib.org/3.1.0/gallery/subplots_axes_and_figures/subplots_demo.html
fig, axs = plt.subplots(rows, cols, figsize = (10, 15), sharex=True, sharey=True)

font_size_subtitles = 15
font_size_source = 13

# RW Ari

axs[0, 0].set_title(cases[0] + " (c)", fontsize=font_size_subtitles)
axs[0, 0].annotate("TESS", xy=(0.1,0.9), xytext=(0.1, 0.9), bbox=dict(boxstyle='round,pad=0.3', fc='white', alpha=1), fontsize=font_size_source)
[axs[0, 0].axvline(i) for i in df_phases["my_phase"][idx_rw_ari].values]
axs[0, 0].scatter(df_rw_ari["Phase"],df_rw_ari["y_photom_norm"], color="k", s=2,zorder=3)
axs[0, 0].plot(df_rw_ari["Phase"],df_rw_ari["y_spline_norm"], color="r", zorder=5)
axs[0, 0].set_xlim([0,1.0])
axs[0, 0].set_ylim([0,1.0])
#axs[0, 0].axvspan(0, bad_phase_region[1], color="k", alpha=greyness_alpha)
#axs[0, 0].axvspan(bad_phase_region[0], 1, color="k", alpha=greyness_alpha)

# X Ari
axs[0, 1].set_title(cases[1] + " (ab)", fontsize=font_size_subtitles)
axs[0, 1].annotate("TESS", xy=(0.1,0.9), xytext=(0.1, 0.9), bbox=dict(boxstyle='round,pad=0.3', fc='white', alpha=1), fontsize=font_size_source)
[axs[0, 1].axvline(i) for i in df_phases["my_phase"][idx_x_ari].values]
axs[0, 1].scatter(df_x_ari["Phase"],df_x_ari["y_photom_norm"], color="k", s=2,zorder=3)
axs[0, 1].plot(df_x_ari["Phase"],df_x_ari["y_spline_norm"], color="r", zorder=5)
axs[0, 1].set_xlim([0,1.0])
axs[0, 1].set_ylim([0,1.0])
#axs[0, 1].axvspan(0, bad_phase_region[1], color="k", alpha=greyness_alpha)
#axs[0, 1].axvspan(bad_phase_region[0], 1, color="k", alpha=greyness_alpha)

# UY Cam
axs[0, 2].set_title(cases[2] + " (c)", fontsize=font_size_subtitles)
axs[0, 2].annotate("TESS", xy=(0.1,0.9), xytext=(0.1, 0.9), bbox=dict(boxstyle='round,pad=0.3', fc='white', alpha=1), fontsize=font_size_source)
[axs[0, 2].axvline(i) for i in df_phases["my_phase"][idx_uy_cam].values]
axs[0, 2].scatter(df_uy_cam["Phase"], df_uy_cam["y_photom_norm"], color="k", s=2,zorder=3)
axs[0, 2].plot(df_uy_cam["Phase"],df_uy_cam["y_spline_norm"], color="r", zorder=5)
axs[0, 2].set_xlim([0,1.0])
axs[0, 2].set_ylim([0,1.0])
#axs[0, 2].axvspan(0, bad_phase_region[1], color="k", alpha=greyness_alpha)
#axs[0, 2].axvspan(bad_phase_region[0], 1, color="k", alpha=greyness_alpha)

# RR Cet
axs[1, 0].set_title(cases[3] + " (ab)", fontsize=font_size_subtitles)
axs[1, 0].annotate("TESS", xy=(0.1,0.9), xytext=(0.1, 0.9), bbox=dict(boxstyle='round,pad=0.3', fc='white', alpha=1), fontsize=font_size_source)
[axs[1, 0].axvline(i) for i in df_phases["my_phase"][idx_rr_cet].values]
axs[1, 0].scatter(df_rr_cet["Phase"], df_rr_cet["y_photom_norm"], color="k", s=2,zorder=3)
axs[1, 0].plot(df_rr_cet["Phase"],df_rr_cet["y_spline_norm"], color="r", zorder=5)
axs[1, 0].set_xlim([0,1.0])
axs[1, 0].set_ylim([0,1.0])
#axs[1, 0].axvspan(0, bad_phase_region[1], color="k", alpha=greyness_alpha)
#axs[1, 0].axvspan(bad_phase_region[0], 1, color="k", alpha=greyness_alpha)

# SV Eri
axs[1, 1].set_title(cases[4] + " (ab)", fontsize=font_size_subtitles)
axs[1, 1].annotate("TESS", xy=(0.1,0.9), xytext=(0.1, 0.9), bbox=dict(boxstyle='round,pad=0.3', fc='white', alpha=1), fontsize=font_size_source)
[axs[1, 1].axvline(i) for i in df_phases["my_phase"][idx_sv_eri].values]
axs[1, 1].scatter(df_sv_eri["Phase"], df_sv_eri["y_photom_norm"], color="k", s=2,zorder=3)
axs[1, 1].plot(df_sv_eri["Phase"],df_sv_eri["y_spline_norm"], color="r", zorder=5)
axs[1, 1].set_xlim([0,1.0])
axs[1, 1].set_ylim([0,1.0])
#axs[1, 1].axvspan(0, bad_phase_region[1], color="k", alpha=greyness_alpha)
#axs[1, 1].axvspan(bad_phase_region[0], 1, color="k", alpha=greyness_alpha)

# VX Her
axs[1, 2].set_title(cases[5] + " (ab)", fontsize=font_size_subtitles)
axs[1, 2].annotate("AAVSO", xy=(0.1,0.9), xytext=(0.1, 0.9), bbox=dict(boxstyle='round,pad=0.3', fc='white', alpha=1), fontsize=font_size_source)
[axs[1, 2].axvline(i) for i in df_phases["my_phase"][idx_vx_her].values]
axs[1, 2].scatter(df_vx_her["Phase"], df_vx_her["y_photom_norm"], color="k", s=2,zorder=3)
axs[1, 2].plot(df_vx_her["Phase"],df_vx_her["y_spline_norm"], color="r", zorder=5)
axs[1, 2].set_xlim([0,1.0])
axs[1, 2].set_ylim([0,1.0])
#axs[1, 2].axvspan(0, bad_phase_region[1], color="k", alpha=greyness_alpha)
#axs[1, 2].axvspan(bad_phase_region[0], 1, color="k", alpha=greyness_alpha)

# RR Leo
axs[2, 0].set_title(cases[6] + " (ab)", fontsize=font_size_subtitles)
axs[2, 0].annotate("TESS", xy=(0.1,0.9), xytext=(0.1, 0.9), bbox=dict(boxstyle='round,pad=0.3', fc='white', alpha=1), fontsize=font_size_source)
[axs[2, 0].axvline(i) for i in df_phases["my_phase"][idx_rr_leo].values]
axs[2, 0].scatter(df_rr_leo["Phase"], df_rr_leo["y_photom_norm"], color="k", s=2,zorder=3)
axs[2, 0].plot(df_rr_leo["Phase"],df_rr_leo["y_spline_norm"], color="r", zorder=5)
axs[2, 0].set_xlim([0,1.0])
axs[2, 0].set_ylim([0,1.0])
#axs[2, 0].axvspan(0, bad_phase_region[1], color="k", alpha=greyness_alpha)
#axs[2, 0].axvspan(bad_phase_region[0], 1, color="k", alpha=greyness_alpha)

# TT Lyn
axs[2, 1].set_title(cases[7] + " (ab)", fontsize=font_size_subtitles)
axs[2, 1].annotate("TESS", xy=(0.1,0.9), xytext=(0.1, 0.9), bbox=dict(boxstyle='round,pad=0.3', fc='white', alpha=1), fontsize=font_size_source)
[axs[2, 1].axvline(i) for i in df_phases["my_phase"][idx_tt_lyn].values]
axs[2, 1].scatter(df_tt_lyn["Phase"], df_tt_lyn["y_photom_norm"], color="k", s=2,zorder=3)
axs[2, 1].plot(df_tt_lyn["Phase"],df_tt_lyn["y_spline_norm"], color="r", zorder=5)
axs[2, 1].set_xlim([0,1.0])
axs[2, 1].set_ylim([0,1.0])
#axs[2, 1].axvspan(0, bad_phase_region[1], color="k", alpha=greyness_alpha)
#axs[2, 1].axvspan(bad_phase_region[0], 1, color="k", alpha=greyness_alpha)

# TV Lyn
axs[2, 2].set_title(cases[8] + " (c)", fontsize=font_size_subtitles)
axs[2, 2].annotate("TESS", xy=(0.1,0.9), xytext=(0.1, 0.9), bbox=dict(boxstyle='round,pad=0.3', fc='white', alpha=1), fontsize=font_size_source)
[axs[2, 2].axvline(i) for i in df_phases["my_phase"][idx_tv_lyn].values]
axs[2, 2].scatter(df_tv_lyn["Phase"], df_tv_lyn["y_photom_norm"], color="k", s=2,zorder=3)
axs[2, 2].plot(df_tv_lyn["Phase"],df_tv_lyn["y_spline_norm"], color="r", zorder=5)
axs[2, 2].set_xlim([0,1.0])
axs[2, 2].set_ylim([0,1.0])
#axs[2, 2].axvspan(0, bad_phase_region[1], color="k", alpha=greyness_alpha)
#axs[2, 2].axvspan(bad_phase_region[0], 1, color="k", alpha=greyness_alpha)

# TW Lyn
axs[3, 0].set_title(cases[9] + " (ab)", fontsize=font_size_subtitles)
axs[3, 0].annotate("TESS", xy=(0.1,0.9), xytext=(0.1, 0.9), bbox=dict(boxstyle='round,pad=0.3', fc='white', alpha=1), fontsize=font_size_source)
[axs[3, 0].axvline(i) for i in df_phases["my_phase"][idx_tw_lyn].values]
axs[3, 0].scatter(df_tw_lyn["Phase"], df_tw_lyn["y_photom_norm"], color="k", s=2,zorder=3)
axs[3, 0].plot(df_tw_lyn["Phase"],df_tw_lyn["y_spline_norm"], color="r", zorder=5)
axs[3, 0].set_xlim([0,1.0])
axs[3, 0].set_ylim([0,1.0])
#axs[3, 0].axvspan(0, bad_phase_region[1], color="k", alpha=greyness_alpha)
#axs[3, 0].axvspan(bad_phase_region[0], 1, color="k", alpha=greyness_alpha)

# RR Lyr
axs[3, 1].set_title(cases[10] + " (ab)", fontsize=font_size_subtitles)
axs[3, 1].annotate("TESS", xy=(0.1,0.9), xytext=(0.1, 0.9), bbox=dict(boxstyle='round,pad=0.3', fc='white', alpha=1), fontsize=font_size_source)
[axs[3, 1].axvline(i) for i in df_phases["my_phase"][idx_rr_lyr].values]
axs[3, 1].scatter(df_rr_lyr["Phase"], df_rr_lyr["y_photom_norm"], color="k", s=2,zorder=3)
axs[3, 1].plot(df_rr_lyr["Phase"],df_rr_lyr["y_spline_norm"], color="r", zorder=5)
axs[3, 1].set_xlim([0,1.0])
axs[3, 1].set_ylim([0,1.0])
#axs[3, 1].axvspan(0, bad_phase_region[1], color="k", alpha=greyness_alpha)
#axs[3, 1].axvspan(bad_phase_region[0], 1, color="k", alpha=greyness_alpha)

# V535 Mon
axs[3, 2].set_title(cases[11] + " (c)", fontsize=font_size_subtitles)
axs[3, 2].annotate("KELT", xy=(0.1,0.9), xytext=(0.1, 0.9), bbox=dict(boxstyle='round,pad=0.3', fc='white', alpha=1), fontsize=font_size_source)
[axs[3, 2].axvline(i) for i in df_phases["my_phase"][idx_v535_mon].values]
axs[3, 2].scatter(df_v535_mon["Phase"], df_v535_mon["y_photom_norm"], color="k", s=2,zorder=3)
axs[3, 2].plot(df_v535_mon["Phase"],df_v535_mon["y_spline_norm"], color="r", zorder=5)
axs[3, 2].set_xlim([0,1.0])
axs[3, 2].set_ylim([0,1.0])
#axs[3, 2].axvspan(0, bad_phase_region[1], color="k", alpha=greyness_alpha)
#axs[3, 2].axvspan(bad_phase_region[0], 1, color="k", alpha=greyness_alpha)

# V445 Oph
axs[4, 0].set_title(cases[12] + " (ab)", fontsize=font_size_subtitles)
axs[4, 0].annotate("KELT", xy=(0.1,0.9), xytext=(0.1, 0.9), bbox=dict(boxstyle='round,pad=0.3', fc='white', alpha=1), fontsize=font_size_source)
[axs[4, 0].axvline(i) for i in df_phases["my_phase"][idx_v445_oph].values]
axs[4, 0].scatter(df_v445_oph["Phase"], df_v445_oph["y_photom_norm"], color="k", s=2,zorder=3)
axs[4, 0].plot(df_v445_oph["Phase"],df_v445_oph["y_spline_norm"], color="r", zorder=5)
axs[4, 0].set_xlim([0,1.0])
axs[4, 0].set_ylim([0,1.0])
#axs[4, 0].axvspan(0, bad_phase_region[1], color="k", alpha=greyness_alpha)
#axs[4, 0].axvspan(bad_phase_region[0], 1, color="k", alpha=greyness_alpha)

import ipdb; ipdb.set_trace()

# AV Peg
axs[4, 1].set_title(cases[13] + " (ab)", fontsize=font_size_subtitles)
axs[4, 1].annotate("KELT", xy=(0.1,0.9), xytext=(0.1, 0.9), bbox=dict(boxstyle='round,pad=0.3', fc='white', alpha=1), fontsize=font_size_source)
[axs[4, 1].axvline(i) for i in df_phases["my_phase"][idx_av_peg].values]
axs[4, 1].scatter(df_av_peg["Phase"], df_av_peg["y_photom_norm"], color="k", s=2,zorder=3)
axs[4, 1].plot(df_av_peg["Phase"]-1.0, df_av_peg["y_spline_norm"], color="r", zorder=5) # -1.0 in phase to shift plotted area to the region without the stray plotted line
axs[4, 1].set_xlim([0,1.0])
axs[4, 1].set_ylim([0,1.0])
#axs[4, 1].axvspan(0, bad_phase_region[1], color="k", alpha=greyness_alpha)
#axs[4, 1].axvspan(bad_phase_region[0], 1, color="k", alpha=greyness_alpha)

# BH Peg
axs[4, 2].set_title(cases[14] + " (ab)", fontsize=font_size_subtitles)
axs[4, 2].annotate("AAVSO", xy=(0.1,0.9), xytext=(0.1, 0.9), bbox=dict(boxstyle='round,pad=0.3', fc='white', alpha=1), fontsize=font_size_source)
[axs[4, 2].axvline(i) for i in df_phases["my_phase"][idx_bh_peg].values]
axs[4, 2].scatter(df_bh_peg["Phase"], df_bh_peg["y_photom_norm"], color="k", s=2,zorder=3)
axs[4, 2].plot(df_bh_peg["Phase"], df_bh_peg["y_spline_norm"], color="r", zorder=5)
axs[4, 2].set_xlim([0,1.0])
axs[4, 2].set_ylim([0,1.0])
#axs[4, 2].axvspan(0, bad_phase_region[1], color="k", alpha=greyness_alpha)
#axs[4, 2].axvspan(bad_phase_region[0], 1, color="k", alpha=greyness_alpha)

# AR Per
axs[5, 0].set_title(cases[15] + " (ab)", fontsize=font_size_subtitles)
axs[5, 0].annotate("KELT", xy=(0.1,0.9), xytext=(0.1, 0.9), bbox=dict(boxstyle='round,pad=0.3', fc='white', alpha=1), fontsize=font_size_source)
[axs[5, 0].axvline(i) for i in df_phases["my_phase"][idx_ar_per].values]
axs[5, 0].scatter(df_ar_per["Phase"], df_ar_per["y_photom_norm"], color="k", s=2,zorder=3)
axs[5, 0].plot(df_ar_per["Phase"], df_ar_per["y_spline_norm"], color="r", zorder=5)
axs[5, 0].set_xlim([0,1.0])
axs[5, 0].set_ylim([0,1.0])
#axs[5, 0].axvspan(0, bad_phase_region[1], color="k", alpha=greyness_alpha)
#axs[5, 0].axvspan(bad_phase_region[0], 1, color="k", alpha=greyness_alpha)


# RU Psc
axs[5, 1].set_title(cases[16] + " (c)", fontsize=font_size_subtitles)
axs[5, 1].annotate("KELT", xy=(0.1,0.9), xytext=(0.1, 0.9), bbox=dict(boxstyle='round,pad=0.3', fc='white', alpha=1), fontsize=font_size_source)
[axs[5, 1].axvline(i) for i in df_phases["my_phase"][idx_ru_psc].values]
axs[5, 1].scatter(df_ru_psc["Phase"], df_ru_psc["y_photom_norm"], color="k", s=2,zorder=3)
axs[5, 1].plot(df_ru_psc["Phase"], df_ru_psc["y_spline_norm"], color="r",zorder=5)
axs[5, 1].set_xlim([0,1.0])
axs[5, 1].set_ylim([0,1.0])
#axs[5, 1].axvspan(0, bad_phase_region[1], color="k", alpha=greyness_alpha)
#axs[5, 1].axvspan(bad_phase_region[0], 1, color="k", alpha=greyness_alpha)

# T Sex

axs[5, 2].set_title(cases[17] + " (c)", fontsize=font_size_subtitles)
axs[5, 2].annotate("TESS", xy=(0.1,0.9), xytext=(0.1, 0.9), bbox=dict(boxstyle='round,pad=0.3', fc='white', alpha=1), fontsize=font_size_source)
[axs[5, 2].axvline(i) for i in df_phases["my_phase"][idx_t_sex].values]
axs[5, 2].scatter(df_t_sex["Phase"], df_t_sex["y_photom_norm"], color="k", s=2,zorder=3)
axs[5, 2].plot(df_t_sex["Phase"], df_t_sex["y_spline_norm"], color="red",zorder=5)
axs[5, 2].set_xlim([0,1.0])
axs[5, 2].set_ylim([0,1.0])
#axs[5, 2].axvspan(0, bad_phase_region[1], color="k", alpha=greyness_alpha)
#axs[5, 2].axvspan(bad_phase_region[0], 1, color="k", alpha=greyness_alpha)

# TU UMa
axs[6, 0].set_title(cases[18] + " (ab)", fontsize=font_size_subtitles)
axs[6, 0].annotate("TESS", xy=(0.1,0.9), xytext=(0.1, 0.9), bbox=dict(boxstyle='round,pad=0.3', fc='white', alpha=1), fontsize=font_size_source)
[axs[6, 0].axvline(i) for i in df_phases["my_phase"][idx_tu_uma].values]
axs[6, 0].scatter(df_tu_uma["Phase"], df_tu_uma["y_photom_norm"], color="k", s=2,zorder=3)
axs[6, 0].plot(df_tu_uma["Phase"], df_tu_uma["y_spline_norm"], color="red",zorder=5)
axs[6, 0].set_xlim([0,1.0])
axs[6, 0].set_ylim([0,1.0])
#axs[6, 0].axvspan(0, bad_phase_region[1], color="k", alpha=greyness_alpha)
#axs[6, 0].axvspan(bad_phase_region[0], 1, color="k", alpha=greyness_alpha)


# All RRabs
alpha_val = 0.1
s_val = 1
[axs[6, 1].axvline(i) for i in df_phases["my_phase"][idx_x_ari].values]
[axs[6, 1].axvline(i) for i in df_phases["my_phase"][idx_rr_cet].values]
[axs[6, 1].axvline(i) for i in df_phases["my_phase"][idx_sv_eri].values]
[axs[6, 1].axvline(i) for i in df_phases["my_phase"][idx_vx_her].values]
[axs[6, 1].axvline(i) for i in df_phases["my_phase"][idx_rr_leo].values]
[axs[6, 1].axvline(i) for i in df_phases["my_phase"][idx_tt_lyn].values]
[axs[6, 1].axvline(i) for i in df_phases["my_phase"][idx_tw_lyn].values]
[axs[6, 1].axvline(i) for i in df_phases["my_phase"][idx_rr_lyr].values]
[axs[6, 1].axvline(i) for i in df_phases["my_phase"][idx_v445_oph].values]
[axs[6, 1].axvline(i) for i in df_phases["my_phase"][idx_av_peg].values]
[axs[6, 1].axvline(i) for i in df_phases["my_phase"][idx_bh_peg].values]
[axs[6, 1].axvline(i) for i in df_phases["my_phase"][idx_ar_per].values]
[axs[6, 1].axvline(i) for i in df_phases["my_phase"][idx_tu_uma].values]

axs[6, 1].scatter(df_x_ari["Phase"],df_x_ari["y_photom_norm"], color="k", alpha=alpha_val, s=s_val,zorder=5)
axs[6, 1].scatter(df_rr_cet["Phase"], df_rr_cet["y_photom_norm"], color="k", alpha=alpha_val, s=s_val,zorder=5)
axs[6, 1].scatter(df_sv_eri["Phase"], df_sv_eri["y_photom_norm"], color="k", alpha=alpha_val, s=s_val,zorder=5)
axs[6, 1].scatter(df_vx_her["Phase"], df_vx_her["y_photom_norm"], color="k", alpha=alpha_val, s=s_val,zorder=5)
axs[6, 1].scatter(df_rr_leo["Phase"], df_rr_leo["y_photom_norm"], color="k", alpha=alpha_val, s=s_val,zorder=5)
axs[6, 1].scatter(df_tt_lyn["Phase"], df_tt_lyn["y_photom_norm"], color="k", alpha=alpha_val, s=s_val,zorder=5)
axs[6, 1].scatter(df_tw_lyn["Phase"], df_tw_lyn["y_photom_norm"], color="k", alpha=alpha_val, s=s_val,zorder=5)
axs[6, 1].scatter(df_rr_lyr["Phase"], df_rr_lyr["y_photom_norm"], color="k", alpha=alpha_val, s=s_val,zorder=5)
axs[6, 1].scatter(df_v445_oph["Phase"], df_v445_oph["y_photom_norm"], color="k", alpha=alpha_val, s=s_val,zorder=5)
axs[6, 1].scatter(df_av_peg["Phase"], df_av_peg["y_photom_norm"], color="k", alpha=alpha_val, s=s_val,zorder=5)
axs[6, 1].scatter(df_bh_peg["Phase"], df_bh_peg["y_photom_norm"], color="k", alpha=alpha_val, s=s_val,zorder=5)
axs[6, 1].scatter(df_ar_per["Phase"], df_ar_per["y_photom_norm"], color="k", alpha=alpha_val, s=s_val,zorder=5)
axs[6, 1].scatter(df_tu_uma["Phase"], df_tu_uma["y_photom_norm"], color="k", alpha=alpha_val, s=s_val,zorder=5)
axs[6, 1].set_title(cases[19], fontsize=font_size_subtitles)
#axs[6, 1].annotate(cases[0], xy=(0.1,0.9), fontsize=font_size_source)
[axs[6, 1].axvline(i) for i in example_phase_phases_star_1]
axs[6, 1].set_xlim([0,1.0])
axs[6, 1].set_ylim([0,1.0])
#axs[6, 1].axvspan(0, bad_phase_region[1], color="k", alpha=greyness_alpha)
#axs[6, 1].axvspan(bad_phase_region[0], 1, color="k", alpha=greyness_alpha)

# All RRcs
[axs[6, 2].axvline(i) for i in df_phases["my_phase"][idx_rw_ari].values]
[axs[6, 2].axvline(i) for i in df_phases["my_phase"][idx_uy_cam].values]
[axs[6, 2].axvline(i) for i in df_phases["my_phase"][idx_tv_lyn].values]
#[axs[6, 2].axvline(i) for i in df_phases["my_phase"][idx_ru_psc].values]
[axs[6, 2].axvline(i) for i in df_phases["my_phase"][idx_t_sex].values]
axs[6, 2].scatter(df_rw_ari["Phase"],df_rw_ari["y_photom_norm"], color="k", alpha=alpha_val, s=s_val,zorder=5)
axs[6, 2].scatter(df_uy_cam["Phase"], df_uy_cam["y_photom_norm"], color="k", alpha=alpha_val, s=s_val,zorder=5)
axs[6, 2].scatter(df_tv_lyn["Phase"], df_tv_lyn["y_photom_norm"], color="k", alpha=alpha_val, s=s_val,zorder=5)
#axs[6, 2].scatter(df_v535_mon["Phase"], df_v535_mon["y_photom_norm"], color="k", s=s_val,zorder=5)
#axs[6, 2].scatter(df_ru_psc["Phase"], df_ru_psc["y_photom_norm"], color="k", alpha=alpha_val, s=s_val,zorder=5)
axs[6, 2].scatter(df_t_sex["Phase"], df_t_sex["y_photom_norm"], color="k", alpha=alpha_val, s=s_val,zorder=5)
axs[6, 2].set_title(cases[20], fontsize=font_size_subtitles)
#axs[6, 2].annotate(cases[0], xy=(0.1,0.9), fontsize=font_size_source)
[axs[6, 2].axvline(i) for i in example_phase_phases_star_1]
axs[6, 2].set_xlim([0,1.0])
axs[6, 2].set_ylim([0,1.0])
#axs[6, 2].axvspan(0, bad_phase_region[1], color="k", alpha=greyness_alpha)
#axs[6, 2].axvspan(bad_phase_region[0], 1, color="k", alpha=greyness_alpha)

for ax in axs.flat:
    ax.set(xlabel="Phase $\phi$", ylabel="$\Delta$m")
    ax.xaxis.label.set_size(font_size_source)
    ax.yaxis.label.set_size(font_size_source)
    #ax.tick_params(axis='y', labelsize=font_size_source)

# Hide x labels and tick labels for top plots and y ticks for right plots.
for ax in axs.flat:
    ax.label_outer()

axs[0, 0].invert_yaxis()
axs[0, 1].invert_yaxis()
axs[0, 2].invert_yaxis()
axs[1, 0].invert_yaxis()
axs[1, 1].invert_yaxis()
axs[1, 2].invert_yaxis()
axs[2, 0].invert_yaxis()
axs[2, 1].invert_yaxis()
axs[2, 2].invert_yaxis()
axs[3, 0].invert_yaxis()
axs[3, 1].invert_yaxis()
axs[3, 2].invert_yaxis()
axs[4, 0].invert_yaxis()
axs[4, 1].invert_yaxis()
axs[4, 2].invert_yaxis()
axs[5, 0].invert_yaxis()
axs[5, 1].invert_yaxis()
axs[5, 2].invert_yaxis()
axs[6, 0].invert_yaxis()
axs[6, 1].invert_yaxis()
axs[6, 2].invert_yaxis()

axs[0, 0].set_yticks([])

plt.tight_layout()

file_name_out = "test.png"
plt.savefig(file_name_out, dpi=300)
print("Wrote ", file_name_out)
