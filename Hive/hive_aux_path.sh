## How to set hive.aux.jars.path with multiple jar files.
## Sarun Singla

#!/bin/bash

value= `ls /tmp/jarfiles/ >hivercre`
##you can replace the directory above with the jar files locations.
update_hiverc=`sed ':a;N;$!ba;s/\n/,/g' hivercre`
#echo $update_hiverc
file1=`touch .hiverc`
file=".hiverc"
echo $file
if [ -f "$file" ]
then
  echo "set hive.aux.jars.path=$update_hiverc" >"$file"
fi
