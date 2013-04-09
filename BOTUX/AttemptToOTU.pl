use strict;
use warnings;

my $infile = shift;
my $trimLength = shift; 
my $outfile = shift;

if(!defined ($outfile)) {
  print "ERROR MSG: Please provide an input file, trimlength and an output file\n"; 
}
open IFH, "$infile" or die "Error in opening the infile\n";
open OFH, ">$outfile" or die "Error in opening the infile\n";

########## MAIN METHOD#####################
my $file = makeTrimString($infile, $outfile);

my %HashOfSeq;
my $line; 
my $Header; 
my $Seq = "";
my $LenSeq =0; 
my $TotalSeqInFile =0; 
my $nonDuplicatedSeq =0; 
my $LenSubString;
my $subString;
my $bothLen; 
my $Multiple_Read;
my @SeqList; 
my @wordList;
my @OTUList; 
my $word;




############## SUBROUTINES ##################
sub makeTrimString{
my ($infile, $outfile) = @_;
while($line = <IFH>){
if ($line =~ /(^>\w+\|)/g) {
  chomp $line; 
	$Header = $1; 
}
else {
	$Seq = $line; 
	$LenSeq = length($Seq); 
foreach my $range (0..($LenSeq-9)){
	$word = substr($Seq, $range, 8);
	push (@wordList, $word);
} # end for loop
if ($LenSeq > $trimLength) {
	$subString = substr($Seq, 0, $trimLength);
	#print OFH $subString, "\n\n\n";
}
elsif($LenSeq <= $trimLength) {
	$bothLen = ($LenSubString, $LenSeq);

if (exists $HashOfSeq{$Seq}){
	$HashOfSeq{$Seq}++; 
} # end if exists loop

else {
	$HashOfSeq{$Seq} = 1; 
	$nonDuplicatedSeq++; 
} # end second else loop

}
	$TotalSeqInFile++; 
} # end else loop
} # end while

} # end makeTrimString

my $bestScore = -999; 
my %WordHash;
my $words; 
my $la; 
my $OtuScore; 
my $totalScoreinCurrentOtu =0; 
foreach(@wordList){
$words = $_; 
	if (exists $WordHash{$words}){
		$WordHash{$words}++; 
		$HashOfSeq{$Seq}{$words}++; 
	} # end if
	else{
		$WordHash{$words} =1; 
		$HashOfSeq{$Seq}{$words} =1; 
	}
} # end foreach

my @keys = keys %HashOfSeq;
my @sorted_values = sort{ length($b) <=> length($a) || $HashOfSeq{$b} <=> $HashOfSeq{$a}} @keys;

my $lenOfSeq; 
my $Abundance; 
foreach (@sorted_values){ 
print $sorted_values[1], "\n"; 
$lenOfSeq = length($_);
$Abundance = $HashOfSeq{$_}; 

#print OFH ("Length: $lenOfSeq\tAbundance:$Abundance\n\n");

} # end first foreach

#print OFH ("Total number of sequences = $TotalSeqInFile, \n Single Read = $nonDuplicatedSeq \n");



