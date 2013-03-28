#! perl

use strict;
use warnings;

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
my $num_of_reads = 0;
my $uniq = 0;

$line = <IN>;
chomp $line;

$seq = "";

while($line = <IN>) {	
		if ($line =~ /^>(\w+)\|/)  {
			if($seq ne "") { 				
				$seq_length = length($seq) ;
				if(exists $Seq_Hash{$seq_length}{$seq}){
				    $Seq_Hash{$seq_length}{$seq}{count} +=1;
				}
				else{
				    $Seq_Hash{$seq_length}{$seq}{count} = 1;
				    $uniq ++;
				}				
			$SeqName =$1;
			$seq = "";	
		}
		else {
			$num_of_reads ++;
			$seq .= $line;  # sequence can be on multiple lines  
		}
#print OUT ($seq_length, "\t", $seq, "\n");			
		
				
}

foreach $seq_length ( sort (keys (%Seq_Hash))) {
	foreach my $seq (sort (keys ($Seq_Hash{$seq_length}) ) ){
		my $abundance = ($Seq_Hash{$seq_length}{$seq}{count}/2);
		
		print OUT ("Seq Length:", $seq_length, "\t", "Abundance:", $abundance, "\n");
		}
	}
	
	
print OUT ("Total Number of Reads In File:", $num_of_reads -1, "\n");
print OUT ("Total Number of Unique Reads:", $uniq -1);


close IN;
close OUT;	
	
exit;
