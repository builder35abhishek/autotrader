#!/bin/bash

mytime=`date +%Y%m%d_%H%M%S`

last_trigger_value=/tmp/last_trigger_value.txt
current_trigger_value=/tmp/current_trigger_value_${mytime}.txt
script_log=/tmp/script_log_${mytime}.txt

truncate -s 0 $current_trigger_value

#printf "Enter Name of Symbol from YahooFinance :- "
#read symbol_name

/root/trade.py INFY.NS | awk '{print $NF}' | tail -3 | head -1 > $current_trigger_value

for st in `cat $current_trigger_value`
do
  if [ "$st" = "BUY" ] || [ "$st" = "SELL" ]; then
    if [ "`cat $last_trigger_value`" != "$st" ]; then
      echo $st > $last_trigger_value
      printf "\nshift from `cat $last_trigger_value` to $st" | tee -a $script_log
    else
      printf "\nNo action required" | tee -a $script_log
    fi
  else
    continue
  fi
done
