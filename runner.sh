#!/bin/bash

# config_file="config/InclSS3L.json"
analysis_name="SUSY-2018-04"
config_file="config/${analysis_name}.json"

if [ ! -d "output/${analysis_name}" ];then
   mkdir -p "output/${analysis_name}"
fi

for counter in {1..10}
do
   output_file="output/${analysis_name}/run_${counter}.log"

   if [ -f "${output_file}" ];then
      echo "${output_file} already exists"
      exit 1
   fi
   printf "\n* Running test for %s \n\n" "${output_file}"
   # wrap in () to captrue output of time
   # (time python -c "import time; print('hello'); time.sleep(5); print('bye')") > "${output_file}" 2>&1
   (time python fit_analysis.py --config-file "${config_file}") > "${output_file}" 2>&1
   tail -n 4 "${output_file}"
done
