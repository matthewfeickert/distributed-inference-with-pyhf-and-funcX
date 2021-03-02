#!/bin/bash

# config_file="config/InclSS3L.json"
# analysis_name="3L-RJ"
# analysis_name="1Lbb"
analysis_name="staus"
config_file="config/${analysis_name}.json"
output_dir="output/${analysis_name}/batch"

if [ ! -d "${output_dir}" ];then
   mkdir -p "${output_dir}"
fi

for counter in {1..10}
do
   output_file="${output_dir}/run_${counter}.log"

   if [ -f "${output_file}" ];then
      echo "${output_file} already exists"
      exit 1
   fi
   printf "\n* Running test for %s \n\n" "${output_file}"
   # wrap in () to captrue output of time
   (time python fit_analysis.py --config-file "${config_file}") > "${output_file}" 2>&1
   tail -n 4 "${output_file}"
   sleep 5
done
