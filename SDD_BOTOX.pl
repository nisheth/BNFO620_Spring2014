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
my ($line, $SeqName, $locus, $species, $genus, $number, $seq, $seq_length);	
my $seq_length_min = 99999999999;
my $seq_length_max = 0;

$line = <IN>;
chomp $line;

	while($line = <IN>) {	
			if ($line =~ /^>(\w+)\|/)  {
			$SeqName =$1;
			}
			else {
			$seq = $line;
			}
#print OUT ($seq_length, "\t", $seq, "\n");			
			$seq_length = length($seq);
			
				if(exists $Seq_Hash{$seq_length}){
					if(exists $Seq_Hash{$seq_length}{$seq}){
					$Seq_Hash{$seq_length}{$seq}{count} ++;
					}
					else{
					$Seq_Hash{$seq_length}{$seq}{count} =1;
					}
				}
				else{
					$Seq_Hash{$seq_length}{$seq}{count} =1;
				}
}
foreach my $seq_length ( sort keys %Seq_Hash ) {
	print OUT ($seq_length);
	foreach my $seq ( sort keys {%Seq_Hash{$seq_length}} ) {
		print OUT ($seq_length, "\t", $seq, "\t", "\n");
		
		
	}
}


close IN;
close OUT;	
	
exit;	
