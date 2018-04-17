import subprocess, datetime, time, sys
from subprocess import Popen, PIPE
from datetime import datetime
try:
    path = sys.argv[1]
except:
    print("NO PATH PROVIDED, DEFAULTING TO /hbase/region-in-transition")
    path = '/hbase/region-in-transition'
day = time.strftime("%c")
proc = subprocess.Popen('hbase zkcli', shell = True, stdin = PIPE, stdout = PIPE, stderr = PIPE)
time.sleep(5)
regionlst = proc.communicate('ls ' + path + '\n')[0].split("\n")[-2]
if regionlst != '[]':
    regionlst = regionlst[1:-1].split(",")
    print(regionlst)
    for region in regionlst:
        proc = subprocess.Popen('hbase zkcli', shell = True, stdin = PIPE, stdout = PIPE, stderr = PIPE)
        time.sleep(5)
        output = proc.communicate('\nget ' + path + '/' + str(region) + '\n')[1].splitlines()[-10:-6]
        ctime = output[0][8:]
        mtime = output[2][8:]
        ctime = ctime[:19] + " " + ctime[-4:]
        mtime = mtime[:19] + " " + mtime[-4:]
        #convert day, ctime, mtime to milliseconds. Then see if its within 30 mins which means < 1800000 ms.
        day = datetime.strptime(day, '%a %b %d %H:%M:%S %Y').strftime('%s')
        ctime = datetime.strptime(ctime, '%a %b %d %H:%M:%S %Y').strftime('%s')
        mtime = datetime.strptime(mtime, '%a %b %d %H:%M:%S %Y').strftime('%s')
        if int(day) * 1000 - int(ctime) * 1000 > 1800000 and int(day) * 1000 - int(mtime) * 1000 > 1800000:
            #PLEASE MODIFY THIS LINE. I'M NOT SURE MYSELF ON HOW TO SEND EMAILS FROM THE TERMINAL, BUT EVERYTHING ELSE IS RIGHT.
            #str(region) = STRING REPRESENTATION OF REGION ID. 
            proc = subprocess.Popen("mailx -s '" + str(region) + " has RIT ' <email.email.com>", shell=True)
