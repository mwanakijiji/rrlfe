class CompareFehSynthetic():
    '''
    Retrieves pickle files and plots injected and retrieved Fe/H
    '''

    def __init__(self, module_name):

        self.name = module_name

    def run_step(self, attribs = None):

        calib_read_file = attribs["data_dirs"]["DIR_SRC"] + attribs["file_names"]["CALIB_SOLN"]
        calib_file = calib_read_file ## ## vestigial?
        write_pickle_dir = attribs["data_dirs"]["DIR_PICKLE"]

        # excavate all pickle files in the directory
        pickle_list = glob.glob(write_pickle_dir + "/*.p")
        import ipdb; ipdb.set_trace()
        # initialize data frame to hold values
        # cols:
        # 'inj_feh':        injected [Fe/H]
        # 'err_inj_feh'     plus/minus error in injected [Fe/H]
        # 'retr_med_feh'    retrieved [Fe/H]
        # 'lower_sig_feh'   1-sigma lower bound of [Fe/H]
        # 'upper_sig_feh'   1-sigma upper bound of [Fe/H]
        # 'logg'            injected logg
        # 'Teff'            injected effective temperature Teff

        df = pd.DataFrame(columns=["inj_feh", "err_inj_feh", "retr_med_feh",
                                    "lower_err_ret_feh", "upper_err_ret_feh", "logg", "teff", "pickle_file_name"]) #, index=range(len(pickle_list)))


        for file_name in pickle_list:

            # load each item in pickle file (maybe redundant, since it is one dictionary)
            with open(file_name, "rb") as f:
                data_all = pickle.load(f)

            # calculate errors (just stdev for now, probably want to improve this later)
            feh_retrieved = np.nanmedian(data_all["feh_sample_array"])
            err_feh_retrieved = np.nanstd(data_all["feh_sample_array"])

            values_to_add = {"inj_feh": data_all["injected_feh"],
                            "err_inj_feh": data_all["err_injected_feh"],
                            "logg": data_all["logg"],
                            "teff": data_all["Teff"],
                            "retr_med_feh": feh_retrieved,
                            "lower_err_ret_feh": err_feh_retrieved,
                            "upper_err_ret_feh": err_feh_retrieved,
                            "pickle_file_name": os.path.basename(file_name)}

            row_to_add = pd.Series(values_to_add, name="x")
            df = df.append(row_to_add)

        print(data_all)

        # plot retrieved and injected metallicities
        # matplotlib to show error bars

        fig, axes = plt.subplots(2, 1, figsize=(15, 24), sharex=True)
        fig.suptitle("Retrieval comparison, from MCMC file\n" + str(self.calib_file))

        # Fe/H difference
        df["feh_diff"] = np.subtract(df["retr_med_feh"],df["inj_feh"])

        # introduce scatter in x
        scatter_x = 0.1*np.random.rand(len(df["inj_feh"]))
        df["inj_feh_scatter"] = np.add(scatter_x,df["inj_feh"])

        cmap = sns.color_palette("YlOrBr", as_cmap=True)
        #cmap = sns.rocket_palette(rot=-.2, as_cmap=True)

        axes[0].plot([-2.5,0.5],[-2.5,0.5],linestyle="--",color="k",zorder=0)

        # underplot error bars
        axes[0].errorbar(x=df["inj_feh_scatter"],y=df["retr_med_feh"],xerr=df["err_inj_feh"],yerr=df["lower_err_ret_feh"],linestyle="",color="k",zorder=1)

        g_abs = sns.scatterplot(
            ax=axes[0],
            data=df,
            x="inj_feh_scatter", y="retr_med_feh",
            hue="teff", size="logg",
            edgecolor="k",
            palette=cmap, sizes=(50, 150),
            zorder=10
        )
        axes[0].set_ylabel("Retrieved: [Fe/H]$_{r}$")

        axes[1].plot([-2.5,0.5],[0,0],linestyle="--",color="k",zorder=0)
        g_diff = sns.scatterplot(
            ax=axes[1],
            data=df,
            x="inj_feh_scatter", y="feh_diff",
            hue="teff", size="logg",
            edgecolor="k",
            palette=cmap, sizes=(50, 150),
            legend=False,
            zorder=10
        )
        axes[1].set_ylabel("Residual: [Fe/H]$_{r}$-[Fe/H]$_{i}$")
        axes[1].set_xlabel("Injected: [Fe/H]$_{i}$")
        #axes[0].set_ylim([-3.,10.])
        #axes[1].set_ylim([-0.45,0.8])

        plt.savefig("/Users/bandari/Desktop/junk.pdf")

        #g.set(xscale="log", yscale="log")
        #g.ax.xaxis.grid(True, "minor", linewidth=.25)
        #g.ax.yaxis.grid(True, "minor", linewidth=.25)
        #g.despine(left=True, bottom=True)
