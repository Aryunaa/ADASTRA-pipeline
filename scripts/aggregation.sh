#!/bin/bash

source HELPERS/paths_for_components.py

njobs=$1
indicator=$2

if [ "$indicator" == "--forCL" ];then
  python3 "$scripts_path"/PARAMETERS/make_params_aggregation.py "CL"
  parallel --jobs "$njobs" python3 "$scripts_path"/ASBcalling/Aggregation.py "CL" :::: "$parallel_parameters_path"/Agr_parameters.cfg
fi
if [ "$indicator" == "--forTF" ];then
  python3 "$scripts_path"/PARAMETERS/make_params_aggregation.py "TF"
  parallel --jobs "$njobs" python3 "$scripts_path"/ASBcalling/Aggregation.py "TF" :::: "$parallel_parameters_path"/Agr_parameters.cfg
fi