import sys
import os.path
from statistics import median_grouped
from scipy import stats
import numpy as np
import json
import statsmodels.stats.multitest
import pandas as pd

sys.path.insert(1, "/home/abramov/ASB-Project")
from scripts.HELPERS.paths_for_components import parameters_path, results_path, tf_dict_path, cl_dict_path
from scripts.HELPERS.helpers import callers_names, unpack, pack, check_if_in_expected_args, expected_args, states

for table_name in os.listdir("/home/abramov/RESULTS/release-180120_Tambry/TF_P-values/"):
    table_path = "/home/abramov/RESULTS/release-180120_Tambry/TF_P-values/" + table_name
    out_path = "/home/abramov/RESULTS/CheckBH/TF_P-values/" + table_name
    table = pd.read_table(table_path)
    list_of_chr = set("chr" + str(i) for i in range(11, 23))
    for chr in list_of_chr:
        table = table[table["chr"] != chr]
    mc_filter_array = np.array(table['max_cover'] >= 10)
    if sum(mc_filter_array) != 0:
        bool_ar_ref, p_val_ref, _, _ = statsmodels.stats.multitest.multipletests(table[mc_filter_array]["logitp_ref"],
                                                                                 alpha=0.05, method='fdr_bh')
        bool_ar_alt, p_val_alt, _, _ = statsmodels.stats.multitest.multipletests(table[mc_filter_array]["logitp_alt"],
                                                                                 alpha=0.05, method='fdr_bh')
    else:
        p_val_ref = []
        p_val_alt = []
        bool_ar_ref = []
        bool_ar_alt = []

    fdr_ref = np.array(['NaN'] * len(table.index), dtype=np.float128)
    fdr_ref[mc_filter_array] = p_val_ref
    table["fdrp_bh_ref"] = fdr_ref

    fdr_alt = np.array(['NaN'] * len(table.index), dtype=np.float128)
    fdr_alt[mc_filter_array] = p_val_alt
    table["fdrp_bh_alt"] = fdr_alt

    table.to_csv(out_path, sep="\t", index=False)