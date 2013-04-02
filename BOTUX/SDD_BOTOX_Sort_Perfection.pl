#! perl

use strict;
use warnings;
use Data::Dumper;

my $input = shift;
my $output = shift;

if(!defined($output))
{
die "You did not enter a correct input or output file: $!\n"
}
  open IN, "<$input";
open OUT, ">$output";


my %Seq_Hash;
my %seq;
my %seq_length;
my @sorted_array_of_hash_values;
my ($line, $SeqName, $seq, $seq_length);  
my $num_of_reads = 1;
my $uniq = 0;

$line = <IN>;
chomp $line;

$seq = "";

while($line = <IN>) {	
	if ($line =~ /^>(\w+)\|/) {
	$num_of_reads ++;
		if($line ne "") {
	$SeqName = $1;
	$line = "";
	}
	}
	else {
		if($line ne "") {
		chomp $line;
		$seq = $line; # sequence can be on multiple lines
		#print OUT $seq
			
				 if(exists $Seq_Hash{$seq}){
					$Seq_Hash{$seq} +=1;
					}
				 else{
					 $Seq_Hash{$seq} = 1;
					 $uniq ++;	 
				 }	
	#print OUT ($seq_length, "\t", $seq, "\n");
		 }
		 }
		 
		
}
 my @keys = keys %Seq_Hash;
 my @sorted_keys = sort{ length($b) <=> length($a) || $Seq_Hash{$b} <=> $Seq_Hash{$a}} @keys;

foreach (@sorted_keys){
print OUT ( length($_ ), "abundance", $Seq_Hash{$_} ,"\n" );
}


print OUT ("Total Number of Reads In File:", $num_of_reads, "\n");
print OUT ("Total Number of Unique Reads:", $uniq );


close IN;
close OUT;	

exit;
	


