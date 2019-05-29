# Small File Offenders
This perl script helps to inform you of the users that have the most "small files". 
If you are on HDP 2.5+, you do not need a script like this. Why? 
Because HDP 2.5 has a Zeppelin notebook that will help you identify 
what users are contributing to small file volume. This is part of [SmartSense](https://docs.hortonworks.com/HDPDocuments/SS1/SmartSense-1.4.0/index.html).
 Read more 
[here] (https://docs.hortonworks.com/HDPDocuments/SS1/SmartSense-1.3.0/bk_installation/content/activity_analysis.html) on that. 
If you are on an older HDP version, you 

# Why Worry About Small Files?
The HDFS NameNode architecture, explained [here](https://hadoop.apache.org/docs/r1.2.1/hdfs_design.html) mentions that 
"the NameNode keeps an image of the entire file system namespace and file Blockmap in memory." What this means is that 
every file in HDFS adds some pressure to the memory capacity for the NameNode process. Therefore, a larger max heap for 
the NameNode Java process will be required as the files system

# How to use this script
Before beginning, process the image file into TSV format, as shown in this example command:
```
hadoop oiv -i /hadoop/hdfs/namesecondary/current/fsimage_0000000000003951761 -o fsimage-delimited.tsv -p Delimited
```
then pipe the output file (fsimage-delimited.tsv) into this program, eg. cat fsimage-delimited.tsv | fsimage_users.pl

# Example
```
HW13177:~ clukasik$ ./fsimage_users.pl ./fsimage-delimited.tsv
Limiting output to top 10 items per list. A small file is considered anything less than 134217728. Edit the script to adjust these values.
Average File Size (bytes): 0; Users:
	hive (total size: 0; number of files: 12)
	yarn (total size: 0; number of files: 8)
	mapred (total size: 0; number of files: 7)
	hcat (total size: 0; number of files: 1)
	anonymous (total size: 0; number of files: 1)
Average File Size (bytes): 219.65; Users:
	ambari-qa (total size: 4393; number of files: 20)
Average File Size (bytes): 245.942307692308; Users:
	hbase (total size: 12789; number of files: 52)
Average File Size (bytes): 1096.625; Users:
	spark (total size: 8773; number of files: 8)
Average File Size (bytes): 34471873.6538462; Users:
	hdfs (total size: 896268715; number of files: 26)
Average File Size (bytes): 46705038.25; Users:
	zeppelin (total size: 186820153; number of files: 4)

Users with most small files:
	hbase: 52 small files
	hdfs: 23 small files
	ambari-qa: 20 small files
	hive: 12 small files
	spark: 8 small files
	yarn: 8 small files
	mapred: 7 small files
	zeppelin: 3 small files
	anonymous: 1 small files
	hcat: 1 small files
```
