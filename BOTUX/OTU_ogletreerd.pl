
#use strict;
use warnings; 
use Data::Dumper; 

#COMMAND-LINE OPTIONS: Fasta file, output file, and desired trim length. 
my $inputfile = shift; 
my $outfile = shift; 
my $trimLength = shift; 

if (!defined ($trimLength)) {
	die "USAGE: Please provide an input file, output file, and trimlength."; 
}

#VARIABLES AND CONSTANTS
my (%seqHash, $lengthOfSeq, $cutLength, $subSeq, $Length, $SeqLength, $uniqueSeq, $score, $size);  
my (@keys, @sort, $abundance, $length, $word);
my ($seedSeq, %OTUhash, $totalWords);
my $maxScore = -999; 
my $sequence = "";
my $firstline = 1; 
my $totalReads = 0; 
my $THRESHOLD = 0.7;  

# OPEN FASTA FILE AND OUPUT FILE
open INFILE, "$inputfile" or die "USAGE: Error in opening the $inputfile\n"; 
open OUTFILE, ">$outfile" or die "USAGE: Error in opening the $outfile\n";

#### GET FASTA SEQUENCE
# Opens sequence file in FastA format

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
				$lengthOfSeq = length ($sequence); 
				
				if ($lengthOfSeq > $trimLength) {
					$subSeq = substr($sequence,0,($lengthOfSeq- $trimLength));
					} 
			 
			 	CreateWords ($sequence);	
				$totalReads++; 
				if(exists $seqHash{$sequence}) {
					$seqHash{$sequence} += 1; 
				} else {
					$seqHash{$sequence} = 1; 
					$uniqueSeq++; 
				}
			}	 
		} #end of while-loop

@keys = keys %seqHash; 
@sort = sort {length($b) <=> length($a) || $seqHash{$b} <=> $seqHash{$a}} @keys; 

foreach (@sort) {
	$length = length($_);
	$abundance =  $seqHash{$_}; 
	}

print OUTFILE ("\nTotal Reads:", $totalReads, "\n", "Total unique sequences:", $uniqueSeq, "\n"); 

###### SUBROUTINES #######

# RUN WINDOW THROUGH SEQUENCE
# Move window from beginning to end of sequence
# Extract word from sequence

sub CreateWords {
	($sequence) = $_; 
	for (my $i=0;$i<=length($sequence)-8;$i++){
		$word = substr ($sequence, $i, 8);
		print OUTFILE "$word\n";
		
		if (exists $wordHash{$word}) { 
			$wordHash{$word} += 1; 
		} else {
			$wordHash{$word}{wordCount} =1;  
			}
		}
}

#ADD WORD
#Adds a new word to an appropriate OTU bucket

sub addWord {
($myWord) = $_; 
foreach $word (keys %seqHash) {
	if (exists $wordHash{$myWord}){
		$wordHash{$myWord} +=1;
	}else {
		$wordHash{$myWord} = 1; 
		}
	}
}

#CREATES A NEW OTU 
#Creates a new OTU with the attributes: seed sequence, list of words, and Sequence ID

sub createOTU {
	($sequence, $myWord) = $_; 
	$seedSeq = $sequence; 
	%OTUhash = (); 
	addWord($myWord);
	}

# SCORES A READ
# Gives a score to a read

# sub Score {
# ($sequence, $seedSeq) = $_;
# 
# freqOfWi = OTUhash{}
#  
#   
#  }



# sub Bucket_Reads {
# 	($reads, $OTU, $threshold) = $_;
# 	foreach $otu (keys %OTUhash){
# 	#$score = Score ();
# 		if ($score > $maxScore) {
# 			$maxScore = $score;
# 			$newOTU = currOTU;
# 		}	
# 		if ($maxScore > $threshold){
# 		
# 		
# 		}	
# 	}
# }

close INFILE; 
close OUTFILE; 
	

