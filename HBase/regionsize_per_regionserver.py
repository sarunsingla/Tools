#!/usr/bin/python
import os
import commands

var1 = raw_input("Please enter region server list to parse and check: ")
var2 = raw_input("Please enter path to store output: ")
regions_server_list = "%s" %var1
path_to_store = "%s" %var2

#removes old files and created new files based on the curl call
def generate_files(region_list,path_to_store_data):
        print "removing old files"
        os.system("rm %s*" %unicode(path_to_store_data))
        with open(region_list,"r") as f:
                for line in f:
                        regionserver = line.strip()
                        os.system("curl -s http://%s:60030/jmx|grep storeFileSize|awk -F \"[_:]\" '{print $6,$9}'|cut -d \',\' -f1 >%s/output_%s" % (unicode(regionserver),  unicode(path_to_store_data), unicode(regionserver)))



# based on the files generate it gets you a list of region_server|region_id|size
def generate_data(path):
        status,files_list = commands.getstatusoutput("ls -d %s*" % unicode(path))
        files_list1 = files_list.split('\n')
        for files in files_list1:
                with open(files,"r") as files_read:
                         for newline in files_read:
                                strip_data = newline.strip()
                                split_data = strip_data.split( )
                                try:
                                        size_of_region = int(split_data[1])
                                except ValueError:
                                        print("Failure to convert the string to int" +split_data[1])
                                if string_to_int == 0:
                                        print "%s,%s,%s" % (unicode(files), unicode(split_data[0]), unicode(size_of_region))


generate_files(var1,var2)
print "Generated the data"
generate_data(path_to_store)
