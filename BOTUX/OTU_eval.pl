use strict;
use warnings;

my $infile = shift;
my $outfile = shift;
if(!defined ($outfile)) {
  print "USAGE Instruction: Please provide an input file and output file"; 
}

my %seqHash;
my @SeqArray;
my $count =0;
my $Seq = "";  
my $lenSeq; 
my @len; 
my @sortLenSeq; 
my $header; 
open IFH, "$infile" or die "Error in opening the $infile\n";
open OFH, ">$outfile" or die "Error in opening the $outfile\n"; 

my $line = <IFH>;
while ($line = <IFH>) {
	chomp $line;
	if ($line =~ /^>(\w+)\|/) # reg ex to extract all the accession Ids
	{	
		$header = $1;
		#print $header; 
	
	} 
	else {
	$Seq = $line; 
	
}
$lenSeq = length($Seq);

if (exists $seqHash{$Seq}) {
		$seqHash{$Seq}{$count}++; 
}
	else {
	$seqHash{$Seq}{$count}= 1; 
}
print OFH "\nLength = $lenSeq\t"; 
}

foreach my $element (sort {$seqHash{$b}{$count} <=> $seqHash{$a}{$count}} keys %seqHash) {
	my $abundance = $seqHash{$element}{$count};
	print OFH "\nAbundance = $abundance\t";	
}


