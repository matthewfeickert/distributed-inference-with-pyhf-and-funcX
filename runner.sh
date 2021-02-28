#!/bin/bash

config_file="config/InclSS3L.json"

for counter in {6..10}
do
   output_file="output/InclSS3L/run_${counter}.log"

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
