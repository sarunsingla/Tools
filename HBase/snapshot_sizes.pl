#!/usr/bin/perl

#use Number::Bytes::Human qw(format_bytes);
use Data::Dumper;
use feature qw(say);
my @sizes=qw( B KB MB GB TB PB);
$log=$ARGV[0];
$directory=$ARGV[1];
if(!$log)
{
		print "Usage: \n";
		print "        " . $0 . " <logfile> \n";
}
else
{
        my %dir_map;
        $count = 0;
		open (my $logfile, '<:encoding(UTF-8)', $log);

		while (my $line = <$logfile>) {
				if(!(($line=~/\/hbase/) && ($line=~/\/archive\/data\//))) {
				        next;
				}
		        if($directory) {
				        if(!($line=~/$directory/)) {
								next;
						}
				}
				my @values = split(/\s+/,$line);
				my $size = $values[4];
				my $directory = $values[7];
				my @hbsplit  = split("hbase",$directory);
				my @dirsplit = split("data", @hbsplit[1],2);
				my @dirnames = split("/", @dirsplit[1]);

                my $name;
				if( grep( /data/, @dirnames )) {
				  $name = $dirnames[4];
				}
				else {
				  $name = $dirnames[2];
				}
				my $count_dir = 0;
				if (exists $dir_map{$name}) {
						$count_dir = $dir_map{$name}	
				}
				$count_dir += $size;

                $dir_map{$name} = $count_dir;
		}
		foreach my $dirname (sort {$dir_map{$a} <=> $dir_map{$b} } keys %dir_map) {
				printf "%15s %s\n", nice_size($dir_map{$dirname}), $dirname ;
		}
}
# Taken from http://www.perlmonks.org/?node_id=378538
sub nice_size
{
  my $size = shift;
  my $i = 0;

  while ($size > 1024)
  {
    $size = $size / 1024;
    $i++;
  }
  return sprintf("%.2f$sizes[$i]", $size);
}
