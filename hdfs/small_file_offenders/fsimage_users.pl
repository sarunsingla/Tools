#!/usr/bin/env perl
use strict;
# Before beginning, process the image file into TSV format, as shown in this example command:
# hadoop oiv -i /hadoop/hdfs/namesecondary/current/fsimage_0000000000003951761 -o fsimage-delimited.tsv -p Delimited
# then pipe the output file (fsimage-delimited.tsv) into this program, eg. cat fsimage-delimited.tsv | fsimage_users.pl

# Change these as needed
my $BLOCK_SIZE =  134217728;
my $LIMIT_TOP_N = 10;

print "Limiting output to top $LIMIT_TOP_N items per list. A small file is considered anything less than $BLOCK_SIZE. Edit the script to adjust these values.\n";

my $users;
my $first = 0;
while (<>) {
  if ($first == 0) {
    $first = $first + 1;
    next;
  }
  my @vals = split /\t/;
  $users->{$vals[10]}->{"ttlsize"} = (0 + $users->{$vals[10]}->{"ttlsize"}) + $vals[6];
  $users->{$vals[10]}->{"numfiles"} = (0 + $users->{$vals[10]}->{"numfiles"}) + 1;
  if ($vals[6] < $BLOCK_SIZE) {
    $users->{$vals[10]}->{"smaller"} = (0 + $users->{$vals[10]}->{"smaller"}) + 1;
  }
}

set_avg($users);
print_offenders($users);

exit(0);

sub set_avg() {
  my ($h) = @_;
  my $username;
  foreach $username (keys %{$h}) {
    $h->{$username}->{"avgsize"} = $h->{$username}->{"ttlsize"}  / $h->{$username}->{"numfiles"};
  }
}


sub print_offenders() {
  my ($h) = @_;
  my $username;
  my %offenders;
  my %smalls;
  my $size;
  foreach $username (keys %{$h}) {
    push @{$offenders{$h->{$username}->{"avgsize"}}}, $username;
    push @{$smalls{$h->{$username}->{"smaller"}}}, $username;
  }
  my $count = 0;
  foreach $size (sort {$a<=>$b} keys %offenders) {
    print "Average File Size (bytes): $size; Users:\n";
    my $innercnt = 0;
    foreach $username (reverse sort {$h->{$a}->{"numfiles"}<=>$h->{$b}->{"numfiles"}} @{$offenders{$size}}) {
      print "\t$username (total size: $h->{$username}->{\"ttlsize\"}; number of files: $h->{$username}->{\"numfiles\"})\n";
      $innercnt = $innercnt + 1;
      last if ($innercnt >= $LIMIT_TOP_N);
    }
    $count = $count + 1;
    last if ($count >= $LIMIT_TOP_N);
  }
  print "\nUsers with most small files:\n";
  $count = 0;
  foreach $size (sort {$b<=>$a} keys %smalls) {
    foreach $username (sort @{$smalls{$size}}) {
      print "\t$username: $size small files\n";
    }
    $count = $count + 1;
    last if ($count >= $LIMIT_TOP_N);
  }

}
