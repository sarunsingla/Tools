#!/usr/bin/python
import os
#import sys

var1 = raw_input("Please enter region server list to parse and check: ")
print "you entered", var1

var2 = raw_input("Please enter path to store output: ")
print "you entered", var2

regions_server_list = "%s" %var1
path_to_store = "%s" %var2

print "Printing the path_to_store", path_to_store
#Cleaning the directory before adding more
print "removing old files"
os.system("rm %s*" %unicode(path_to_store))

with open(regions_server_list,"r") as f:
        for line in f:
                regionserver = line.strip()
                os.system("curl -s http://%s:60030/jmx|grep storeFileSize|awk -F \"[_:]\" '{print $6,$9}'|cut -d \',\' -f1 >%s/output_%s" % (unicode(regionserver),  unicode(var2), unicode(regionserver)))

print "Generated the files already if here"
indir = "%s" %(unicode(path_to_store))
print "please print the path where you will read from:", indir

for root,dirs,files in os.walk(indir):
        for name in files:
                file_path = os.path.join(root, name)
                opening_file = "%s" %file_path
                with open (opening_file,"r") as file_read:
                        for newline in file_read:
                                data1 = newline.strip()
                                splits = data1.split( )
                                #print(splits[1])
                                splits[1].strip('\n')
                                try:
                                        string_to_int = int(splits[1])
                                except ValueError:
                                        print("Failure w/ value " +splits[1])
                               # string_to_int = int(splits[1])
                                get_region_loc_name = file_path.split('/')
                                get_region_name = get_region_loc_name[5].split('_')
                                if string_to_int == 0:
                                        print "%s,%s,%s" % (unicode(get_region_name[1]), unicode(splits[0]), unicode(string_to_int))
