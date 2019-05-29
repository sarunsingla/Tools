#!/usr/bin/env bash

# This script dumps all connections to the NameNode RPC port every
# 30 seconds.
#

THRESHOLD_CONNERROCESS=4
THRESHOLD_CONNER_NODE=100

if [[ -z "$1" ]]
then
  echo "  Usage: sudo dump_connections_to_nn.sh <output-file-name>"
  exit
fi

if [ "$EUID" -ne 0 ]
then
  echo "  Must be run as root."
  exit
fi

while [ 1 ]
do
  bFlag=0
  current_time=$(date "+%Y-%m-%d %H:%M:%S")
  echo "${current_time} Dumping all connections to port 8020 >>>>>>>>>>>>>" >> $1
  netstat -anp | grep -i 'tcp.*:8020\b' >> $1
  echo "${current_time} <<<<<<<<<<<<<<<<<<<<<<<<< Done dumping connections" >> $1
  netstat -anp | grep -i 'tcp.*:8020\b'|awk '{print $7}'|grep -v "\-"|awk -F"/" '{print $1}'|uniq -c|while read line
  do
   echo $line
   num_conn_perpid=$(echo $line | cut -f1 -d" ");
   each_pid=$(echo $line | cut -f2 -d" ");
if [ $num_conn_perpid -gt $THRESHOLD_CONNERROCESS ];
then
   echo "======= PID $each_pid , num_conn=$num_conn_perpid ======= " >> $1
   cat /proc/$each_pid/cmdline >> $1
   echo "" >> $1;
fi;
bFlag=1
done

total_conn_node=`netstat -anp | grep -i 'tcp.*:8020\b'|awk '{print $7}'|grep -v "\-"|awk -F"/" '{print $1}'|wc -l`
echo "Total connections : $total_conn_node" >> $1

if [[ $bFlag -eq 0 && $total_conn_node -gt $THRESHOLD_CONNER_NODE ]] ;
then
   for pid in `netstat -anp | grep -i 'tcp.*:8020\b'|awk '{print $7}'|grep -v "\-"|awk -F"/" '{print $1}'|uniq| sort -n`;
   do
    echo "=================== PID = $pid ===============" >> $1
    ps -ef|grep $pid|grep -v grep >> $1
    echo "---------- cmdline ---------" >> $1
    cat /proc/$pid/cmdline >> $1;
    echo "" >> $1;
   done
fi;
sleep 30
done
