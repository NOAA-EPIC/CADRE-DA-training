#!/bin/bash

#WFLOW_LOG_FN="log.run_expt"

# Initialize the default status of the workflow to "IN PROGRESS".
wflow_status="IN PROGRESS"

while [ "$wflow_status" == "IN PROGRESS" ]; do

  # Run task
  rocotorun -w land_analysis.xml -d land_analysis.db

  # Run rocotostat
  rocotostat_output=$( rocotostat -w land_analysis.xml -d land_analysis.db )

  while read -r line; do
    if echo "$line" | grep -q "DEAD"; then
      wflow_status="FAILURE"
      break
    fi
  done <<< ${rocotostat_output}

  # Print out rocotostat
  printf "%s" "${rocotostat_output}" #> ${WFLOW_LOG_FN}

  rocotostat_s_output=$( rocotostat -w land_analysis.xml -d land_analysis.db -s )

  regex_search="^[ ]*([0-9]+)[ ]+([A-Za-z]+)[ ]+.*"
  cycle_str=()
  cycle_status=()
  i=0
  while read -r line; do
    if [ $i -gt 0 ]; then
      im1=$((i-1))
      cycle_str[im1]=$( echo "$line" | sed -r -n -e "s/${regex_search}/\1/p" )
      cycle_status[im1]=$( echo "$line" | sed -r -n -e "s/${regex_search}/\2/p" )
    fi
    i=$((i+1))
  done <<< "${rocotostat_s_output}"

  # Get the number of cycles
  num_cycles_total=${#cycle_str[@]}
  num_cycles_completed=0
  for (( i=0; i<=$((num_cycles_total-1)); i++ )); do
    if [ "${cycle_status[i]}" = "Done" ]; then
      num_cycles_completed=$((num_cycles_completed+1))
    fi
  done

  # Check whether all cycles are complete
  if [ ${num_cycles_completed} -eq ${num_cycles_total} ]; then
    wflow_status="SUCCESS"
  fi
  
  # Print out result
  printf "%s" "

Summary of workflow status:
=====================================================
  ${num_cycles_completed} out of ${num_cycles_total} cycles completed.
  Workflow status:  ${wflow_status}
=====================================================
" #>> ${WFLOW_LOG_FN}

  # Check if expt is done; otherwise nap
  if [ "$wflow_status" == "IN PROGRESS" ]; then
    echo " "
    echo "Sleeping for 30 seconds."
    sleep 30
  else
    break
  fi
done

