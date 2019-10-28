import sys

sys.path.insert(1, "/home/abramov/ASB-Project")
from scripts.HELPERS.paths import parameters_path
from scripts.HELPERS.helpers import make_list_for_VCFs

out_path = parameters_path + "MasterListForVCFs.tsv"

if __name__ == "__main__":
    make_list_for_VCFs(out_path)
