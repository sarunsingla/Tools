#!/bin/sh
shopt -s extglob

path=$1
cd $path
#check for the number of jars in the folder
count=$(find . -type f -name "*.jar" | wc -l)

#check if number of jars is more than 1
if [ $count -gt 1 ]
then

# Create a list of files that are in fatjar
   ls *.jar >jarslist.txt
#   cat jarslist.txt

# Create tmp directory and copy all the jars
   mkdir -p tmp
   cp -r *.jar tmp
   cd tmp

# Create the fatjar
   jar -cvf combined.jar .
   cp combined.jar ../
   echo "Created fatjar combined.jar"
else
   echo "Less than 2 jars in the folder"
fi
