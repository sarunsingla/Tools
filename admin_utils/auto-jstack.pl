#!/usr/bin/perl
use strict;
use warnings;
use Data::Dumper;
use Scalar::Util qw(looks_like_number);


print "Which component are you looking to take a jstack for:\n";
my $process=<>;
chomp($process);
print "Process name is :   $process\n";

###get the process id for the java process  based on the process name provided above.

my $process_id_namenode=`ps -ef|grep $process|grep -v grep|awk '{print \$2}'`;
print "Process id for $process is: $process_id_namenode";

### Number of jstack you want
print "How many jstack required:\n";
my $jstack_required= <>;

# Sleep required between each jstack
print "Sleep between each jstack\n";
my $sleep = <>;

if(!$process_id_namenode)
{
	print "No process found, please check the process for jstack\n";
}
else
{
## You need to have both the above values, the below caode validates if the user has added both values.

	if (looks_like_number($jstack_required) && looks_like_number($sleep))
	{
## test cases
		if($jstack_required == 0 && $sleep == 0)
		{
			print "You cannot have 0 as a value for the above 2 variables\n";
		}
		if($jstack_required == 0 && $sleep != 0)
		{
			print "Cannot take 0 jstacks\n";
		}
		elsif($jstack_required != 0 && $sleep != 0)
		{

## looping through and getting the required number of jstack for each $jstack_required and $sleep
			for (my $i=1;$i<=$jstack_required;$i++)
			{
				print "Process Id for Namenode: $process_id_namenode";
				print "Taking a jstack now\n";
				my $JAVA_HOME=`cat /etc/hadoop/conf/hadoop-env.sh |grep "JAVA_HOME="|awk -F "=" '{print \$2}'`;
				chomp($JAVA_HOME);
				my $cmd=`$JAVA_HOME/bin/jstack -F $process_id_namenode`;
				my $date_time=`date +%s`;
# print "$date_time";
				my $filename= "jstack_output_$date_time";
				print "$filename";
				open OUTPUT, ">$filename";
				print OUTPUT "$cmd";
				close OUTPUT;
				sleep ($sleep);
			}
		}
	}
	else
	{
		print "Please add numeric values only\n";
	}
}
