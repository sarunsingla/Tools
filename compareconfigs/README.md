# Config compare before and after upgrade
## XML to Json Converter
- Purpose
- Inputs: To run the script please make sure you have the following folders. Files(XML) before upgrade, Files(XML) after upgrade and an empty folder to store JSON outputs.
### USAGE
- `python <cluster-compare.py> <file_location_before_upgrade> <file_location_after_upgrade> <json-output>` 
- `python cluster_compare.py before_upgrade after_upgrade jsonfiles`
- `python cluster_compare.py before/ after/ json/ >/tmp/output.txt`
- Notes: This tool is required for comparing configurations before and after upgrading the cluster from hdp/cdh to CDP/CDP-DC
