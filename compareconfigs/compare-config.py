
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
from datetime import datetime


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
        # IN THE CONFIGConfiguration Difference before and after upgrade")
        print("<br>")
        table = "<table id=\"configs\">\n"
        data = ["Configuration Name", "Before Upgrade", "After Upgrade"]
        table += "  <tr>\n"
        for column in data:
            table += "    <th>{0}</th>\n".format(column.strip())
        table += "  <tr>\n"

        for line in zip(conf_diff, conf_diff_val1, conf_diff_val2):
            table += "  <tr>\n"
            for column in line:
                table += "    <td>{0}</td>\n".format(column.strip())
            table += "  </tr>\n"

        table += "</table>"
        print(table)

        '''Generating Tabular output for before and after upgrades'''
        print("<br>")
        print("<h2>Configurations that were present before the upgrade and are missing now, compared to configurations that are added new after the upgrade.</h2>")
        table = "<table id=\"configs\">\n"
        data = ["Configurations Present Before Upgrade", "Configurations Added After Upgrade"]
        table += "  <tr>\n"
        for column in data:
            table += "    <th>{0}</th>\n".format(column.strip())
        table += "  <tr>\n"

        for line in zip(not_present_file1,not_present_file2):
            table += "  <tr>\n"
            for column in line:
                table += "    <td>{0}</td>\n".format(column.strip())
            table += "  </tr>\n"
        table += "</table>"
        print(table)

    '''Function to walk over all the json files generated and calls function load_compare_files to compare'''
    def glob_parse(self,pathname, name):
        filename = (name + "*.json")
        pathname = (pathname + "/" + filename)
        mylist = [f for f in glob.glob(pathname)]
        if not mylist:
            print("Config files missing for "+name+"-site.xml")
            print("")
        elif len(mylist) > 2:
            x = 0
            #print("<br>")
            print("<h1>"+name.upper()+"</h1>")
            while x < len(mylist):
                print("<h2><i>Multiple files and hence generating a separate difference/compare for each sub-component</i></h2>")
                print("<h3>Comparing {} and {} :</h3>".format(mylist[x].split("/")[1],mylist[x + 1].split("/")[1]))
                class_inst.load_compare_files(mylist[x], mylist[x + 1])
                print("<h3>Comparing {} and {} :</h3>".format(mylist[x].split("/")[1],mylist[x + 2].split("/")[1]))
                class_inst.load_compare_files(mylist[x], mylist[x + 2])
                break
        else:
            print("<br>")
            print("<h1>Component Read : " + name.upper() + "</h1>")
            class_inst.load_compare_files(mylist[0], mylist[1])

class_inst = cluster_compare()
class_inst.xmltojsonconverter(before_upgrade,after_upgrade, json_out)

'''Add more componenbts here for comparing the xml before and after the upgrade'''
components = {'core','hdfs','hive','yarn','mapred'}
for key in components:
    now = datetime.now()
    sys.stdout = open("output.html", "a+")
    print('''<!DOCTYPE html>
    <html>
    <head>
        <style>
            #configs {
              font-family: Arial, Helvetica, sans-serif;
              border-collapse: collapse;
              width: 90%;
              table-layout: fixed;
            }
            #configs td, #configs th {
              border: 1px solid #ddd;
              padding: 4px;
              word-wrap: break-word;
            }
            #configs tr:nth-child(even){background-color: #f2f2f2;}
            #configs tr:hover {background-color: #ddd;}
            #configs th {
              padding-top: 8px;
              padding-bottom: 8px;
              text-align: left;
              background-color: #f96702;
              color: white;
            }
        </style>
        <title>CLUSTER COMPARE</title>
    </head>
    <body>''')
    class_inst.glob_parse(json_out, key)
    sys.stdout.close()
