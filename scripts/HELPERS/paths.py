import os
from scripts.HELPERS.paths_for_components import alignments_path, badmaps_path, tf_dict_path, \
    cl_dict_path


def get_ending(for_what):
    if for_what == "vcf":
        return ".vcf.gz"
    if for_what == "annotated":
        return "_table_annotated.tsv"
    if for_what == "p-value":
        return "_table_p.tsv"
    if for_what == "BAD":
        return "_table_BAD.tsv"
    if for_what == 'base':
        return ''
    raise AssertionError('Incorrect input parameter')


def create_path_from_master_list_df(line, for_what='base'):
    return os.path.join(alignments_path, line['EXP'], line['ALIGNS'] + get_ending(for_what))


def create_badmaps_path_function(name, model):
    return os.path.join(badmaps_path, model, name + ".badmap.tsv")


def open_aggregation_dict(what_for):
    aggregation_dict_path = None
    if what_for == "TF":
        aggregation_dict_path = tf_dict_path
    if what_for == "CL":
        aggregation_dict_path = cl_dict_path
    if aggregation_dict_path is None:
        raise ValueError("Incorrect usage of open_aggregation_dict function")
    return aggregation_dict_path

