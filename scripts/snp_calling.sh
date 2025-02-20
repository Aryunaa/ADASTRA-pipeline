#!/bin/bash

source scripts/HELPERS/paths_for_components.py
source scripts/HELPERS/soft_configs.cfg
njobs=$1

if [ ! -f "${dbsnp_vcf_path}.tbi" ]; then
	echo "Index file for ${dbsnp_vcf_path} not found, indexing.."
	$Java $JavaParameters  -jar "$GATK" IndexFeatureFile -l ${dbsnp_vcf_path}
fi

parallel --delay 600 --jobs "$njobs" \
bash "$scripts_path/SNPcalling/ProcessLine.sh" :::: "${parallel_parameters_path}/sorted_master_list.tsv"
