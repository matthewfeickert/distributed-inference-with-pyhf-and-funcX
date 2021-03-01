#!/bin/bash

# analysis_name="InclSS3L"
analysis_name="staus"
config_file="config/${analysis_name}.json"

if [ ! -d "output/${analysis_name}" ];then
   mkdir -p "output/${analysis_name}"
fi

output_file="output/${analysis_name}_single_node_time.log"

printf "\n* Running test for %s \n\n" "${output_file}"
# wrap in () to captrue output of time
(time python test.py --config-file "${config_file}") > "${output_file}" 2>&1
