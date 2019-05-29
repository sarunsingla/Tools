#!/usr/bin/perl
use Data::Dumper;
use Scalar::Util qw(looks_like_number);

$meta_scan = $ARGV[0];
$attemp_logs = $ARGV[1];
$master_logs = $ARGV[2];

## GETTING START_KEY AND END_KEY
#@get_start_end_key = `cat meta_scan |grep "STARTKEY"|awk -F "," '{print \$3,\$9,\$10}'`;
@get_start_end_key = `cat $meta_scan |grep "STARTKEY"|awk -F "," '{print \$3,\$9,\$10}'`;
chomp(@get_start_end_key);

## GETTING ROW_KEY
#@get_row_key=`cat attempt_1463076948844_172053_r_000022_0 |grep "Hbase scan"|awk '{print \$1,\$2,\$9}'`;

@get_row_key=`cat $attemp_logs |grep "Hbase scan"|awk '{print \$1,\$2,\$9}'`;
chomp(@get_row_key);

@get_region_server= `cat $master_logs |grep Onlined|awk '{print \$1,\$2,\$7,\$9}'`;

open (R, ">regionserver_regionmapping");
open (X, ">master.out");
chomp(@get_region_server);
foreach $regions_get(@get_region_server)

{
	@case1 = split / /,$regions_get;
	@case2 = split /,/,$case1[1];
	@case3 = split /,/,$case1[3];
	print R  "$case1[2],$case3[0],$case1[0],$case2[0]\n";
}
foreach $rec1(@get_start_end_key)

{
	@region = split /\./,$rec1;
	@data=split /'/,$rec1;

	if(looks_like_number($data[1])  && looks_like_number($data[3]))
	{	
		foreach $rec(@get_row_key)
		{		
			@super_set_row = split / /,$rec;
    		@time_set_row = split /,/,$super_set_row[1];
    		@key_roow = split /:/,$super_set_row[2];
			if($key_roow[1] >= $data[0] && $key_roow[1] <= $data[1])
			{
				$region_server = `cat regionserver_regionmapping|grep $region[1]|tail -5`;
				chomp($region_server);
#####  key_id,region_id,region_server name,date,time
				print X "$key_roow[1],$region_server\n"
			}
		}
	}

}
