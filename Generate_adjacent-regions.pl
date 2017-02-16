#!/usr/bin/perl
use Data::Dumper;
use Math::Round;

## Sarun Singla

## taking user input for lsr output and mets scan
######   $meta_file will be the file which containe the scan of meta from hbase shell
######  $lsr will have will have the lsr output of meta scan

my $lsr_file=$ARGV[0];
my $meta_file=$ARGV[1];
my $file1 = "sorted_regions_with_size";
my $file2 = "parsed_meta";

my $size_for_region=$ARGV[2];
chomp($size_for_region);
print "Size of regions you are looking for:  $size_for_region\n";

if($lsr_file && $meta_file)
{

### This code will parse the lsr output of the lsr_file and get the region and size for each.
       	$genrate_data_file=`cat $lsr_file|grep -v ".regioninfo"|grep -v ".tabledesc"|grep -v ".tmp"|grep -v "recovered.edits" >data_file_new.out`;

       	my $f = 'data_file_new.out';
       	open (F, "<", $f);
       	open (R, ">temp");

       	my  %data_hash;

       	while (<F>) {
       		my $line = $_;
       		chomp $line;
       		if($line =~ m/(\/[\w]*){7,}/)
       		{
       			@line_arr = split ('\s+', $line);
       			@curr_keys = split ('/', $line_arr[7]);
       			$data_hash{$curr_keys[7]} += $line_arr[4];
       		}

       	}
       	foreach my $key (keys(%data_hash))
       	{
       		$val_in_mb=$data_hash{$key};
       		$val=$val_in_mb/1024;
       		my $rounded = round( $val );
#      		print   "$key : $data_hash{$key} \n";
       		print R  "$key : $data_hash{$key} \n";
       	}
       	$del_file=`rm data_file_new.out`;
       	$sorted_file=`cat temp|sort >sorted_regions_with_size`;
       	$del_temp=`rm temp`;

### Once we have the above temp file this code block then gets executed which is comparing the output of the first file with the scan of the meta to get the list of size 0 regions.
       	open (X, ">parsed_meta");
       	my @line=`cat $meta_file|awk -F "," '{print \$3,\$4,\$5,\$6,\$7,\$8,\$9,\$10}'`;
       	chomp(@line);
       	foreach my $rec1(@line)
       	{
       		my @tokens = split / /, $rec1;
       		chomp(@tokens);
       		my @regions = split /\./, $tokens[0];
        if( $tokens[15] =~ m/STARTKEY/)
       		{
            print X "Regions: $regions[1]\n";
            print X "START KEY: $tokens[17]\n";
            print X "END KEY: $tokens[21]\n";
       		}
       	}

       	open (S, ">adjacent_region_list");
       	my @size_check =`cat $file1|awk '{print \$3}'`;
       	chomp(@size_check);
       	@regions_size_zero = `cat $file1`;
       	foreach $gen_new_arr(@regions_size_zero)
       	{
       	    push(@new_arr,$gen_new_arr);
       	}
       	chomp(@new_arr);
       	foreach $check_val(@new_arr)
       	{
       	    @size1=split /:/,$check_val;
       		if($size1[1] <= "$size_for_region")
       		{
       			print "$size1[0] : $size1[1] \n";
       			print S "Searching for region: $size1[0]\n";
       		  	$adj_regions= `cat $file2|grep -C3 $size1[0]|grep -v $size1[0]|grep Regions`;
       			print S "$adj_regions\n";
       			print S "\n";
       		}
       	}
}
else
{
       	print "Please add the lsr output file and the meta scan file\n";
       	print "The pattern should be :\n";
       	print "./<script.pl> file1 file2\n";
}
