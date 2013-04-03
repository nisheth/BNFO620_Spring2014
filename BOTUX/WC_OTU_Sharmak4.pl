# use strict;
# use warnings;
# use Data::Dumper;


## new stuff added on April 1, 2013
#use constant WINDOW = 8; 

my $infile = shift;
my $trimLength = shift; 
my $wordsize = shift;
my $outfile = shift;


if(!defined ($outfile)) {
  die "ERROR MSG: Please provide an input file, trim length and an output file\n"; 
}
open IFH, "$infile" or die "Error in opening the infile\n";
open OFH, ">$outfile" or die "Error in opening the infile\n";

my %HashOfSeq;
my $line; 
my $Header; 
my $Seq;
my $LenSeq =0; 
my $TotalSeqInFile =0; 
my $nonDuplicatedSeq =0; 
my $LenSubString;
my $subString;
my $bothSeq; 
my $Multiple_Read;
my $word;
my %HashOfWords;

while($line = <IFH>){
if ($line =~ /(^>\w+\|)/g) {
	chomp $line; 
	$Header = $1; 
	#print $Header, "\n\n"; 
}
else {
	$Seq = $line; 
	for(my $i=0; $i <= length($Seq) - 8; $i++){
		$word = substr($Seq, $i, 8);
	#print $word, "\n"; 
	#print $Seq, "\n\n"; 
	$LenSeq = length($Seq); 

if ($LenSeq > $trimLength) {
	$subString = substr($Seq, 0, ($LenSeq - $trimLength));
	#print $subString, "\n";
	#print $LenSubString = length($subString), "\n"; 
} # end if loop
elsif($LenSeq <= $trimLength) {
	#print $LenSeq, "\n"; 
	#$bothSeq = ($Seq, $subString);
	#print $bothLen, "\n\n";

if (exists $HashOfSeq{$Seq}){
	$HashOfSeq{$Seq}{name} = $Header; 
	$HashOfSeq{$Seq}{words}=$word;
	$HashOfSeq{$Seq}{count_words}++;  
} # end if exists loop

else {
	$HashOfSeq{$Seq}{name} = $Header; 
	$HashOfSeq{$Seq}{words}=$word;
	$HashOfSeq{$Seq}{count_words} =1; 
	$nonDuplicatedSeq++; 
} # end second else loop
	
}
	$TotalSeqInFile++; 
} # end else loop
} # end while
}

my @keys = keys %HashOfSeq;
my @sorted_values = sort{ length($b) <=> length($a) || $HashOfSeq{$b} <=> $HashOfSeq{$a}} @keys;

my $lenOfSeq; 
my $Abundance; 
foreach (@sorted_values){ 
$lenOfSeq = length($_);
#$Abundance = $HashOfSeq{$Seq}; 
$Header = $HashOfSeq{$Seq}{name};
my $wo = $HashOfSeq{$Seq}{words};
my $wc = $HashOfSeq{$Seq}{count_words}; 

print OFH ("Length: $lenOfSeq\tHeader:$Header\tWO= $wo\tWC = $wc\n");

} # end first foreach

print OFH ("Total number of sequences = $TotalSeqInFile, \n Single Read = $nonDuplicatedSeq \n"); 
