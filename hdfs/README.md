#### hdfs-audit-parser
- Purpose: Perl script that aids hdfs audit log analysis by loading it into an an [SQLite](https://www.sqlite.org/) database file. The created Database has a single table named `audit`. Each audit log line is parsed as a set of key-value pairs with the keys as columns in the `audit` table.
- Inputs: hdfs-audit.log
- Usage: `hdfs-audit-parser [--db dbFile] hdfs-audit.log`
- Notes: If dbFile is specified then records are loaded into the existing database file. Else a new database file is created under `/tmp`.
- Example Usages:
    1. Loading Records
       
            $ hdfs-audit-parser hdfs-audit.log
            >> Opened Database /tmp/audit-4662259.db
            >> Imported 1607875 total records
    
    1. Get the top 5 users

            $ sqlite3 /tmp/audit-4662259.db 'select ugi,count(*) as thecount from audit group by ugi order by thecount DESC';
            mapred|1595240
            hive|11024
            spark|610
            yarn|516
            nagios|246
    
    1. Get the top 5 commands

            $ sqlite3 /tmp/audit-4662259.db 'select cmd,count(*) as thecount from audit group by cmd order by thecount DESC limit 5'
            getfileinfo|1111915
            open|168865
            create|160012
            mkdirs|157074
            listStatus|5959
    
    1. Get the top 5 most active times, grouped by seconds.

            $ sqlite3 /tmp/audit-4662259.db 'select time,count(*) as thecount from audit group by time order by thecount DESC limit 5'
            2015-12-30 16:52:23|2413
            2015-12-30 16:47:13|1640
            2015-12-30 16:52:22|1213
            2015-12-30 16:27:08|1211
            2015-12-30 16:17:21|1154
