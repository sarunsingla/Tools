import json
import subprocess
import os


### Variable declaration
subject = 'Container count per application is above configured threshold'
recipient = ''  ##-- add email
running_container_count= 600
rm_host = "" ## -- Resorunce manager host
rm_port = "8088"


def send_message(recipient, subject,data):
    body = """ Application Id | Running Containers | Allocation MB | User | Queue | Queue_used_Percent \n""" +str(data)+ """"""
    try:
        process = subprocess.Popen(['mail', '-s', subject, recipient],stdin=subprocess.PIPE)
    except Exception, error:
                            print error
    process.communicate(body)



## Converting the api data to a well formed json file.

json_data_cmd = "curl -s http://%s:%s/ws/v1/cluster/apps?state=RUNNING|jq \'.\' > rm_data.json" %(rm_host,rm_port)
os.system(json_data_cmd)

data = []
## Read json data from file

with open('rm_data.json', 'r') as f:
    distros_dict = json.load(f)
applicationId= []
## Parse data to be sent to email list
for apps in distros_dict["apps"]["app"]:
    run_containers= apps['runningContainers']
    if run_containers > running_container_count:
        applicationId = apps['id']
        runningContainer = apps['runningContainers']
        allocatedMB = apps['allocatedMB']
        user = apps['user']
        queue = apps['queue']
        queue_used_percent = apps['queueUsagePercentage']
        data_for_email = "%s | %s | %s | %s | %s | %s " %(applicationId,runningContainer,allocatedMB,user,queue,queue_used_percent)
        data.append(data_for_email)

## send email
if data:
        send_message(recipient, subject,data)
        print("Email Sent Successfully")
else:
     print("No apps ")
