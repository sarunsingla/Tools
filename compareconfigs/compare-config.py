
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
import texttable as tt

'''Making sure we are taking the required user input'''
if len(sys.argv) < 4:
    print("Provide folder containing XML files and folder containing JSON file")
    print("Expected way for running the script should be : python <cluster-compare.py> <xmlfiles> <json-output>")
    print("python cluster-compare.py before_upgrade/ after_upgrade/ jsonfiles/")
    sys.exit(1)

'''Folders required for the script to work'''
before_upgrade = sys.argv[1]
after_upgrade = sys.argv[2]
json_out = sys.argv[3]

class cluster_compare():
    '''Function converting xml files to Json files'''
    def xmltojsonconverter(self,before_upgrade,after_upgrade,json_out):
        for filename in os.listdir(before_upgrade):
            if not filename.endswith('.xml'):
                continue
            fullname = os.path.join(before_upgrade, filename)
            with open(fullname, 'r') as f:
                xmlString = f.read()
            jsonString = json.dumps(xmltodict.parse(xmlString), indent=4)
            filename1 = (filename[:-4])
            '''Adding -beforeUpgrade to configuration files'''
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
            '''Adding -afterUpgrade to configuration files'''
            completeName = os.path.join(json_out, filename1 + "-afterUpgrade" + ".json")
            with open(completeName, "w") as f:
                f.write(jsonString)
    '''For future enhancements where you can functionalize table creation'''
    def table_gen(self,row):
        return

# load_compare_files=> Loads json files and compares files with same/similar names. e.g hdfs-site.xml to hdfs-site1.xml
    def load_compare_files(self,file1, file2):
        with open(file1) as f, open(file2) as f1:
            file1_data = json.load(f)
            file2_data = json.load(f1)
            '''List declaration for storing data for use at a later stage'''
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
                        '''If you want to print the configurations which remain the same after upgrade you can do the following
                        print("No Difference :", json_data['name'])'''
                        conf_remaining_same.append(json_data['name'])
                        miss_conf = "False"
                    if json_data['name'] == json_data1['name'] and json_data['value'] != json_data1['value']:
                        conf_diff.append(json_data['name'])
                        conf_diff_val1.append(json_data['value'])
                        conf_diff_val2.append(json_data1['value'])
                        miss_conf = "False"
                if miss_conf == "True":
                    not_present_file1.append(json_data['name'])
            '''Parsing over the second file to generate the difference between the files'''
            for json_data in file2_data['configuration']['property']:
                miss_conf2 = "True"
                for json_data1 in file1_data['configuration']['property']:
                    if json_data['name'] == json_data1['name'] and json_data['value'] == json_data1['value']:
                        miss_conf2 = "False"
                    if json_data['name'] == json_data1['name'] and json_data['value'] != json_data1['value']:
                        miss_conf2 = "False"
                if miss_conf2 == "True":
                    not_present_file2.append(json_data['name'])
        '''Generating Tabular output for configuration difference s between the 2 files'''
       ## #print("PRINTING DIFFERENCES BEFORE AND AFTER: ")
        tab = tt.Texttable()
        headings = ['Configuration Name','BeforeUpgrade','AfterUpgrade']
        tab.header(headings)

        for row in zip(conf_diff,conf_diff_val1,conf_diff_val2):
            tab.add_row(row)
        s = tab.draw()
        print("CONFIG VALUES CHANGED BEFORE AND AFTER UPGRADE :")
        print("================================================\n")
        # IN THE CONFIGConfiguration Difference before and after upgrade")
        print(s)

        '''Generating Tabular output for before and after upgrades'''
        tab1 = tt.Texttable()
        headings1 = ['Configuration Present BEFORE Upgrade','Configuration Present After Upgrade']
        tab1.header(headings1)
        print("")
        print("CONFIGS MISSING BEFORE AND AFTER UPGRADE:")
        print("=========================================\n")
        for present in zip(not_present_file1,not_present_file2):
            tab1.add_row(present)
        draw1= tab1.draw()
        print(draw1)

'''Function to walk over all the json files generated and calls function load_compare_files to compare'''
def glob_parse(pathname, name):
    filename = (name + "*.json")
    pathname = (pathname + "/" + filename)
    mylist = [f for f in glob.glob(pathname)]
    if not mylist:
        print("Config files missing for "+name+"-site.xml")
        print("")
    elif len(mylist) > 2:
        x = 0
        print("======================================================================")
        print("Cases where we have multiple config file for a component after upgrade", name.upper())
        print("=======================================================================\n")

        while x < len(mylist):
            print("IN While loop :")
            print("Comparing the following : ")
            print(mylist[x], mylist[x + 1])
            class_inst.load_compare_files(mylist[x], mylist[x + 1])
            print("Comparing the following : ")
            print(mylist[x], mylist[x + 2])
            class_inst.load_compare_files(mylist[x], mylist[x + 2])
            break
    else:
        print("======================================================\n")
        print("COMPARING FOR THE FOLLOWING COMPONENT =>", name.upper())
        print(mylist)
        print("======================================================\n")
        class_inst.load_compare_files(mylist[0], mylist[1])

class_inst = cluster_compare()
class_inst.xmltojsonconverter(before_upgrade,after_upgrade, json_out)

'''Add more componenbts here for comparing the xml before and after the upgrade'''
components = {'core','hdfs','hive','yarn','mapred'}
for key in components:
    glob_parse(json_out, key)
