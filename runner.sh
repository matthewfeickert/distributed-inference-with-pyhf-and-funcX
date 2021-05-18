#!/bin/bash

analysis_name="1Lbb"
config_file="config/${analysis_name}.json"
endpoint_machine="expanse"
backend="jax"
n_trials=10

if [ ! -d "output/${analysis_name}/${endpoint_machine}" ];then
   mkdir -p "output/${analysis_name}/${endpoint_machine}"
fi

for counter in $(seq 1 "${n_trials}");
do
   output_file="output/${analysis_name}/${endpoint_machine}/run_${counter}.log"

   if [ -f "${output_file}" ];then
      echo "${output_file} already exists"
      exit 1
   fi
   printf "\n* Running test for %s \n\n" "${output_file}"
   # wrap in () to captrue output of time
   (time python fit_analysis.py --config-file "${config_file}" --backend "${backend}") > "${output_file}" 2>&1
   tail -n 4 "${output_file}"
   sleep 5
done
