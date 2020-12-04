
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

import json
import os
import xmltodict
import glob
import sys

# Increment the version when you make modifications
scriptVersion = "1.6"
print("Script version is : ",scriptVersion)

if len(sys.argv) < 3:
    print("Provide folder containing XML files and folder containing JSON file")
    print("Expected way for running the script should be : python <cluster-compare.py> <xmlfiles> <json-output>")
    print("python cluster-compare.py xmlfiles/ jsonfiles/")
    sys.exit(1)


xmlpath = sys.argv[1]
json_out = sys.argv[2]

class cluster_compare():

## xmltojsonconverter=> xml to json converter function
    def xmltojsonconverter(self,in_xml_path, out_json_path):
        for filename in os.listdir(in_xml_path):
            if not filename.endswith('.xml'):
                continue
            fullname = os.path.join(in_xml_path, filename)
            with open(fullname, 'r') as f:
                xmlString = f.read()
            jsonString = json.dumps(xmltodict.parse(xmlString), indent=4)
            filename1 = (filename[:-4])
            completeName = os.path.join(out_json_path, filename1 + ".json")
            with open(completeName, "w") as f:
                f.write(jsonString)

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
            for json_data in file2_data['configuration']['property']:
                miss_conf2 = "True"
                for json_data1 in file1_data['configuration']['property']:
                    if json_data['name'] == json_data1['name'] and json_data['value'] == json_data1['value']:
                        miss_conf2 = "False"
                    if json_data['name'] == json_data1['name'] and json_data['value'] != json_data1['value']:
                        miss_conf2 = "False"
                if miss_conf2 == "True":
                    not_present_file2.append(json_data['name'])
## Printing the output captured
        print("CONFIGS WHICH REMAIN SAME BEFORE AND AFTER : ", conf_remaining_same)
        print("")
        print("CONFIGS WHOSE VALUES CHANGED : ", conf_diff, conf_diff_val1, conf_diff_val2)
        print("")
        print("CONFIGS THAT ARE NOT PRESENT IN FIRST FILE :", not_present_file1)
        print("")
        print("CONFIGS THAT ARE NOT PRESENT IN SECOND FILE :", not_present_file2)
        print("")

class_inst = cluster_compare()
class_inst.xmltojsonconverter(xmlpath, json_out)

def glob_parse(pathname, name):
    filename = (name + "*.json")
    pathname = (pathname + "/" + filename)
    mylist = [f for f in glob.glob(pathname)]
    print("===============================================================")
    print("COMPARING", name, "FILES BEFORE AND AFTER UPGRADES : ", mylist)
    print("================================================================")
    print("")
    class_inst.load_compare_files(mylist[0], mylist[1])

components = {'core','hdfs'}
for key in components:
    glob_parse(json_out, key)
