#!/bin/bash

AlignmentsPath="/home/abramov/Alignments/"
IntervalsPath="/home/abramov/intervals/"
RepPath="/home/abramov/Repeats/repeats_regions.filtered.tsv"
ScriptsPath="/home/abramov/ASB-Project/scripts/"
PEAKannotationScriptsPath=${ScriptsPath}PEAKannotation/
LINE=$1
IFS=$'\t'
read -ra ADDR <<< "$LINE"
	ExpName=${ADDR[0]}
	TF=${ADDR[1]}
	AlignName=${ADDR[6]}
	PeaksName=${ADDR[7]}
if [ "$ExpName" == "#*" ]; then
  exit 1
fi
VCFPath="${AlignmentsPath}EXP/$TF/$ExpName/$AlignName.vcf.gz"
echo "$VCFPath"

echo "Making $ExpName"
echo "Checking exp VCF"
if ! [ -f "$VCFPath" ]; then
  echo "There is no VCF for exp $ExpName ($TF)"
  exit 1
fi

if  [ -f "${AlignmentsPath}EXP/$TF/$ExpName/${AlignName}_table_annotated.txt" ]; then
	echo "Remaking $ExpName"
else
	echo "Making $ExpName first time"
fi

if [ -f "$IntervalsPath/macs/${PeaksName}.interval.zip" ];then
	PeakM="-macs"
	PEAKM="$IntervalsPath/macs/${PeaksName}.interval.zip"
else
  PeakM=""
  PEAKM=""
fi

if [ -f "$IntervalsPath/gem/${PeaksName}.interval.zip" ];then
  PeakG="-gem"
  PEAKG="$IntervalsPath/gem/${PeaksName}.interval.zip"
else
  PeakG=""
  PEAKG=""
fi

if [ -f "$IntervalsPath/cpics/${PeaksName}.interval.zip" ];then
  PeakC="-cpics"
  PEAKC="$IntervalsPath/cpics/${PeaksName}.interval.zip"
else
  PeakC=""
  PEAKC=""
fi

if [ -f "$IntervalsPath/sissrs/${PeaksName}.interval.zip" ];then
  PeakS="-sissrs"
  PEAKS="$IntervalsPath/sissrs/${PeaksName}.interval.zip"
else
  PeakS=""
  PEAKS=""
fi

bash ${PEAKannotationScriptsPath}MakeAnnotatedTable.sh -Out $AlignmentsPath/EXP/"$TF/$ExpName" \
		-Rep "$RepPath" \
		$PeakM $PEAKM $PeakS $PEAKS $PeakG $PEAKG $PeakC $PEAKC\
		-VCF "$VCFPath"
if [ $? != 0 ]; then
  echo "Failed to make tables"

fi

