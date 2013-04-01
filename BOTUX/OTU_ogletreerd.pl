use strict;
use warnings; 

my $inputfile = shift; 
my $outfile = shift; 

if (!defined ($outfile)) {
	die "USAGE: Please provide an input file and output file"; 
}

my %seqHash; 
my ($lengthOfSequence, $duplicatedSeq); 
my $sequence = "";
my $firstline = 1; 
my $totalReads = 0; 
my $uniqueSeq; 

open INFILE, "$inputfile" or die "Error in opening the $inputfile\n"; 
open OUTFILE, ">$outfile" or die "Error in opening the $outfile\n";

while(<INFILE>) {	
		if (m/^>/)  {
			if(!$firstline) {
				$sequence = ""; 
				} 
				$firstline = 0; 
			}
			else { 
				chomp;
				$sequence .= $_; 
				$lengthOfSequence = length ($sequence); 
				$totalReads++; 
				#print OUTFILE $lengthOfSequence. "\t";

				if(exists $seqHash{$lengthOfSequence}{$sequence}) {
					$seqHash{$lengthOfSequence}{$sequence} += 1; 
				} else {
					$seqHash{$lengthOfSequence}{$sequence} = 1; 
					$uniqueSeq++; 
				}
			} 
			#print OUTFILE $sequence. "\n";
		} #end of while-loop

my $abundance; 
my $length; 

foreach my $firstKey (reverse sort keys %seqHash){
	print OUTFILE ("--------------------------------", "\n");
	foreach my $secondKey (sort keys %{$seqHash{$firstKey}}){

		#print OUTFILE ("Sequence:", $secondKey, "\n"); 
		$abundance = $seqHash{$firstKey}{$secondKey};
		$length = $firstKey;
		print OUTFILE ("Length:", $length, "\t", "\t", "\t", "Abundance:", $abundance, "\n"); 
	}
}

print OUTFILE ("\nTotal Reads:", $totalReads, "\n", "Total unique sequences:", $uniqueSeq, "\n"); 

close INFILE; 
close OUTFILE; 
