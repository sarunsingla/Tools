# Hadoop Ecosystem Management Tools

This repository contains a collection of tools designed to assist in managing and troubleshooting various components of the Hadoop ecosystem. These tools can help with tasks related to HDFS, YARN, HBase, and other related services.

## Available Tools

### HBase Tools
- `Generate_adjacent-regions.pl`: Generates a list of adjacent regions in an HBase cluster.
- `regionserver_performance.pl`: Analyzes and reports on HBase RegionServer performance metrics.
- `regionsize_per_regionserver.py`: Calculates and displays the total region size for each RegionServer.
- `snapshot_sizes.pl`: Determines and shows the size of HBase snapshots.

### Hive Tools
- `hive_aux_path.sh`: A shell script for managing Hive auxiliary JAR paths.

### YARN Tools
- `jobsbyexecengine.py`: Lists YARN jobs grouped by their execution engine (e.g., Tez, MapReduce).
- `monitoring_container_per_app.py`: Monitors and reports container usage per YARN application.
- `yarn-log-splitter/yarn-log-splitter.py`: A utility to split large YARN application logs into a structured, more analyzable format. See [Yarn/yarn-log-splitter/README.md](Yarn/yarn-log-splitter/README.md) for more details.

### ZooKeeper Tools
- `get_regions_in_transition.py`: Retrieves and displays information about HBase regions that are currently in transition (RIT) state, often helpful for troubleshooting region assignment issues.

### Admin Utilities
- `apache_jira_hdp_version.py`: A Python script likely used to interact with Apache JIRA to fetch information related to HDP (Hortonworks Data Platform) versions.
- `auto-jstack.pl`: A Perl script designed to automate the process of collecting jstack (Java thread dump) outputs, useful for diagnosing Java application issues.
- `generate_fatjar.sh`: A shell script that helps in packaging a project and its dependencies into a single "fat JAR" file.
- `top_tdump.sh`: A shell script that likely captures output from the `top` command during a thread dump (tdump) operation, providing system resource usage context.

### Configuration Comparison Tools
- `compareconfigs/compare-config.py`: A Python script for comparing cluster configurations before and after an upgrade. It can convert XML configs to JSON and highlight differences. See [compareconfigs/README.md](compareconfigs/README.md) for more details.

### HDFS Tools
- `dump_connections_nn.sh`: A shell script used to dump active connections to the HDFS NameNode.
- `hdfs-audit-parser`: A Perl script that parses HDFS audit logs and loads them into an SQLite database for easier analysis. See [hdfs/README.md](hdfs/README.md) for more details.
- `nn-monitor.pl`: A Perl script for monitoring HDFS NameNode health and performance.
- `small_file_offenders/fsimage_users.pl`: A Perl script that processes an HDFS fsimage dump to identify users consuming space with many small files. See [hdfs/small_file_offenders/README.md](hdfs/small_file_offenders/README.md) for more details.
