
############################################################################
#
# This is a python script to compare configurations for a cluster before and after the upgrades
#
# This tool can be run from Windows, Mac or Linux machines installed with python 3.x
# Please note for the successful running of the code you need these modules
# glob, xmltodict, os, json
# This is a standalone and offline tool and hence needs no direct access to the cluster.
# You will need the config file from the cluster before and after to run with the tool
#
#
# For any questions or suggestions please contact : ssingla@cloudera.com
############################################################################
import itertools
import json
import os
import xmltodict
import glob
import sys
import texttable as tt



# Increment the version when you make modifications
scriptVersion = "1.7"
print("Script version is : ",scriptVersion)

if len(sys.argv) < 4:
    print("Provide folder containing XML files and folder containing JSON file")
    print("Expected way for running the script should be : python <cluster-compare.py> <xmlfiles> <json-output>")
    print("python cluster-compare.py before_upgrade/ after_upgrade/ jsonfiles/")
    sys.exit(1)


before_upgrade = sys.argv[1]
after_upgrade = sys.argv[2]
json_out = sys.argv[3]

class cluster_compare():

## xmltojsonconverter=> xml to json converter function
    def xmltojsonconverter(self,before_upgrade,after_upgrade,json_out):
        for filename in os.listdir(before_upgrade):
            if not filename.endswith('.xml'):
                continue
            fullname = os.path.join(before_upgrade, filename)
            with open(fullname, 'r') as f:
                xmlString = f.read()
            jsonString = json.dumps(xmltodict.parse(xmlString), indent=4)
            filename1 = (filename[:-4])
            completeName = os.path.join(json_out, filename1 + "-beforeUpgrade" + ".json")
            with open(completeName, "w") as f:
                f.write(jsonString)
        for filename in os.listdir(after_upgrade):
            if not filename.endswith('.xml'):
                continue
            fullname = os.path.join(after_upgrade, filename)
            with open(fullname, 'r') as f:
                xmlString = f.read()
            jsonString = json.dumps(xmltodict.parse(xmlString), indent=4)
            filename1 = (filename[:-4])
            completeName = os.path.join(json_out, filename1 + "-afterUpgrade" + ".json")
            with open(completeName, "w") as f:
                f.write(jsonString)

    def table_gen(self,row):
        return

# load_compare_files=> Loads json files and compares files with same/similar names. e.g hdfs-site.xml to hdfs-site1.xml
    def load_compare_files(self,file1, file2):
        with open(file1) as f, open(file2) as f1:
            file1_data = json.load(f)
            file2_data = json.load(f1)
            conf_remaining_same = []
            conf_diff = []
            conf_diff_val1 = []
            conf_diff_val2 = []
            not_present_file1 = []
            not_present_file2 = []
            for json_data in file1_data['configuration']['property']:
                miss_conf = "True"
                for json_data1 in file2_data['configuration']['property']:
                    if json_data['name'] == json_data1['name'] and json_data['value'] == json_data1['value']:
                        # print("No Difference :", json_data['name'])
                        conf_remaining_same.append(json_data['name'])
                        miss_conf = "False"
                    if json_data['name'] == json_data1['name'] and json_data['value'] != json_data1['value']:
                        conf_diff.append(json_data['name'])
                        conf_diff_val1.append(json_data['value'])
                        conf_diff_val2.append(json_data1['value'])
                        miss_conf = "False"
                if miss_conf == "True":
                    not_present_file1.append(json_data['name'])
## Parsing over second file
            for json_data in file2_data['configuration']['property']:
                miss_conf2 = "True"
                for json_data1 in file1_data['configuration']['property']:
                    if json_data['name'] == json_data1['name'] and json_data['value'] == json_data1['value']:
                        miss_conf2 = "False"
                    if json_data['name'] == json_data1['name'] and json_data['value'] != json_data1['value']:
                        miss_conf2 = "False"
                if miss_conf2 == "True":
                    not_present_file2.append(json_data['name'])
    ## Generating tablular format for configurations with differences
       ## #print("PRINTING DIFFERENCES BEFORE AND AFTER: ")
        tab = tt.Texttable()
        headings = ['Configuration Name','Before Upgrade','After Upgrade']
        tab.header(headings)
        for row in zip(conf_diff,conf_diff_val1,conf_diff_val2):
            tab.add_row(row)
        s = tab.draw()
        print(s)

    ## Configs present before upgrade
        #print("Configs with no change => ", conf_remaining_same)
        print("")
        print("Configs present AFTER upgrade", not_present_file2)
        print("")
        print("Configs present BEFORE Upgrade", not_present_file1)
        #print("")

class_inst = cluster_compare()
class_inst.xmltojsonconverter(before_upgrade,after_upgrade, json_out)


def glob_parse(pathname, name):
    filename = (name + "*.json")
    pathname = (pathname + "/" + filename)
    mylist = [f for f in glob.glob(pathname)]
    if not mylist:
        print("Config files missing for "+name+"-site.xml")
    elif len(mylist) > 2:
        x = 0
        print("")
        print("Cases where we have multiple config file for a component after upgrade", name.upper())
        print("=======================================================================")
        print("")
        while x < len(mylist):
            #print("IN While loop :")
            print("Comparing the following files : ",mylist[x], mylist[x + 1])
            class_inst.load_compare_files(mylist[x], mylist[x + 1])
            print("Comparing the following files : ",mylist[x], mylist[x + 2])
            class_inst.load_compare_files(mylist[x], mylist[x + 2])
            break
    else:
        print("===============================================================")
        print("COMPARING", name, "FILES BEFORE AND AFTER UPGRADES : ", mylist)
        print("================================================================")
        print("")
        class_inst.load_compare_files(mylist[0], mylist[1])

# Please add the components you are trying to get a diff for
components = {'core','hdfs','hive','yarn','mapred'}
for key in components:
    glob_parse(json_out, key)
