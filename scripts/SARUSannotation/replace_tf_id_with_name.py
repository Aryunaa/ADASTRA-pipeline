import os
import pandas as pd
from scripts.HELPERS.paths_for_components import results_path


def generate_uniprot_dict(uniprot_dict_file):
    u_df = pd.read_table(uniprot_dict_file)
    return pd.Series(u_df['Entry name'].values, index=u_df['Entry']).to_dict()


def main(uniprot_dict_file):
    uniprot_dict = generate_uniprot_dict(uniprot_dict_file)
    for file in os.listdir(os.path.join(results_path, 'TF_P-values')):
        root_ext = os.path.splitext(file)
        try:
            new_file = uniprot_dict[root_ext[0]] + '.' + root_ext[1]
        except KeyError:
            print('No name found for given id {}'.format(root_ext[0]))
            continue
        print('Renaming {} in {}'.format(file, new_file))
        os.rename(file, new_file)
