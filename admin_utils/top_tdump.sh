LOOP=10
# Interval in seconds between data points.
INTERVAL=3

# Setting the Java Home, by giving the path where your JDK is kept
# USERS MUST SET THE JAVA_HOME before running this script following:

JAVA_HOME=/usr/jdk64/jdk1.8.0_77
PID=$1

$JAVA_HOME/bin/jmap -heap $PID > /tmp/jmap-heap-$PID-$USER-$HOSTNAME-$(date +%d-%m-%Y-%H%M).out

for ((i=1; i <= $LOOP; i++))
do
   $JAVA_HOME/bin/jstack -l $PID >> /tmp/jstack-$PID-$USER-$HOSTNAME-$(date +%d-%m-%Y-%H%M).out
   _now=$(date)
   echo "${_now}" >> /tmp/high-cpu-$USER-$HOSTNAME-$(date +%d-%m-%Y-%H%M).out
   top -b -n 1 -H -p $PID >> /tmp/high-cpu-$USER-$HOSTNAME-$(date +%d-%m-%Y-%H%M).out
   echo "thread dump #" $i
   if [ $i -lt $LOOP ]; then
    echo "sleeping..."
    sleep $INTERVAL
  fi
done
