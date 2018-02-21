#!/usr/bin/python
from itertools import chain

import requests
from bs4 import BeautifulSoup
import sys
import os

array1 = ['2.1', '2.1.15', '2.1.10', '2.1.7', '2.1.5', '2.1.4', '2.1.3', '2.1.2', '2.1.1']
array2 = ['2.6.0', '2.5', '2.5.3', '2.5.0', '2.5.5', '2.6.1', '2.6.2', '2.6.3', '2.6.4']
array3 = ['2.4', '2.4.3', '2.4.2', '2.4.0', '2.3.6', '2.3.4.7', '2.3.4', '2.3.2', '2.2', '2.2.9']

def scrap_web(url):
    r = requests.get(url)
    soup = BeautifulSoup(r.text,"html.parser")
    list = []
    for story_heading in soup.find_all(class_="link"):
        if story_heading:
            list.append(str(story_heading.text.replace("\n", " ").strip()))
        else:
            print("No changes in version here")
    print("")
    print("LIST OF BUGS FIXED IN HDP-{}".format(version_to_check))
    print("================================")
    print ",".join(list)

def known_bugs(url):
    r = requests.get(url)
    soup = BeautifulSoup(r.text,"html.parser")
    list2 = []
    for story_heading1 in soup.find_all(class_="link"):
        if story_heading1:
            list2.append(str(story_heading1.text.replace("\n", " ".strip())))
        #    print(story_heading1.text.replace("\n", " ").strip())
        else:
            print("NO CHANGES WERE MADE TO HDP-{}".format(version_to_check))
    print("")
    print("LIST OF BUGS KNOWN IN HDP-{}".format(version_to_check))
    print("================================")
    print(",".join(list2))

if len(sys.argv) >= 2:
    version_to_check = sys.argv[1]
    if version_to_check in array1:
        url= ("http://docs.hortonworks.com/HDPDocuments/HDP2/HDP-{}/bk_releasenotes_hdp_2.1/content/ch_relnotes-HDP-{}-fixed.html".format(version_to_check,version_to_check))
        scrap_web(url)
    if version_to_check == "2.1.4":
        os.system(
            "curl -s http://docs.hortonworks.com/HDPDocuments/HDP2/HDP-{}.0/README-HDP-2.1.4.0.txt|awk '{print $1,$2}'|awk -F \"[\" '{print $2}'|"
            "tr -d \"]\"|grep -v -e '^$'".format(version_to_check))
        scrap_web(url)
    elif version_to_check in array2:
        url = ("http://docs.hortonworks.com/HDPDocuments/HDP2/HDP-{}/bk_release-notes/content/fixed_issues.html".format(version_to_check))
        scrap_web(url)
        #get known bugs
        url2 = ("https://docs.hortonworks.com/HDPDocuments/HDP2/HDP-{}/bk_release-notes/content/known_issues.html".format(version_to_check))
        known_bugs(url2)
    elif version_to_check in array3:
        url= ("http://docs.hortonworks.com/HDPDocuments/HDP2/HDP-{}/bk_HDP_RelNotes/content/fixed_issues.html".format(version_to_check))
        scrap_web(url)
        #get known bugs
        url2 = ("https://docs.hortonworks.com/HDPDocuments/HDP2/HDP-{}/bk_HDP_RelNotes/content/known_issues.html".format(version_to_check))
        known_bugs(url2)
    elif version_to_check == "2.3.0":
        url= ("http://docs.hortonworks.com/HDPDocuments/HDP2/HDP-{}/bk_HDP_RelNotes/content/fixed-230.html".format(version_to_check))

        url2 = ("https://docs.hortonworks.com/HDPDocuments/HDP2/HDP-{}/bk_HDP_RelNotes/content/known-issues-230.html".format((version_to_check)))
        scrap_web(url)
        known_bugs(url2)

## Throws exception when the version passed does not match to any of the versions we have already
    elif version_to_check not in chain( array1, array2, array3):
        print("NOT A VALID VERSION OF HDP")

        # Throws exception when no version is passed.
else:
    print("You have to enter the HDP version after the script name")
    print("python <scriptname.py> <HDP_version>")
    print("python functionalize_apache.py 2.6.0")
