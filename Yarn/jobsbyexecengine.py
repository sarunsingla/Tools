#!/usr/bin/python

## Importing modules that help to parse json
import json
import urllib2
import sys
import os
import re

data = []
applicationId= []
mydict = {}
final_dict = {}
execution_engine = 'MAPREDUCE'
rm_host = ''  ### Add the rm host from where we want to get the app information
rm_port = '' ### RM port
regex = ['INSERT','SELECT','OVERWRITE','HIVE','CREATE']
user_list = []

### Generate url and get jmx in json format
def getfileurl(rm_host,rm_port):
    json_data_cmd = "curl -s http://%s:%s/ws/v1/cluster/apps?state=FINISHED|jq \'.\' > rm_data.json" %(rm_host,rm_port)
    os.system(json_data_cmd)


### Read json file for data
def get_data(filename):
    with open(filename,'r') as f:
         return json.load(f)

### Parse json and get required data points in interested in
def parse_data():
    distros_dict = get_data("rm_data.json")
    for apps in distros_dict["apps"]["app"]:
        applicationId = apps['id']
        applicationName = apps['name']
        applicationType = apps['applicationType']
        userSubmitted = apps['user']
        queueName = apps['queue']
        mydict = {applicationId: [applicationType,userSubmitted,applicationName,queueName]}
        final_dict.update(mydict)

### Call functions

getfileurl(rm_host,rm_port)
parse_data()

for key,value in final_dict.items():
    if value[0] == execution_engine:
       for pattern in regex:
           if re.search(pattern,value[2]):
              user_list.append(value[1])
              print key,value

userList = set(user_list)

print ""
print "==================================="
print "Users running jobs in hive are: "
print "==================================="
print ""
for users in userList:
    print users
