
use strict;
use warnings; 

my $inputfile = shift;
my $outputfile = shift;
my $trim = shift; 
my $threshold = shift;

my %seqHash;
my %otuHash;

my $wordSize = 8;
my @keys;
my @sort;
my $currSeqW_List;
my $tempBestScore; 

open SEQUENCE_FILE, "$inputfile" or die "Can't open $inputfile: $!\n";
open OUTFILE, ">$outputfile" or die "USAGE: Can't open $outputfile: $!\n";

#sub readFasta {
   #my ($inputfile, $outputfile) = $_;
   my $line;
   my $header;
   my $sequence = "";
   my $firstline = 1; 
   my $length;
   my $seq;
   
   while (<SEQUENCE_FILE>){
   		chomp;
   		if (m/^>(.*)/){
   			if (!$firstline){
   				$length = length ($sequence);
	   			if ($length > $trim) {
   					$seq = substr ($sequence, 0, $trim);
   					$sequence = $seq;
   				}
   				if (!exists $seqHash{$sequence}){
   					$seqHash{$sequence}{freqofWi} = 1;
   				} else {
   					$seqHash{$sequence}{freqofWi}++; 
   				}
   				push @{$seqHash{$sequence}{read}}, $header;
   			}
			$sequence = ""; 
   			$firstline = 0; 
   			$header = $1;  
   		} else {
   			$sequence .= $_;    			
   		}
	}

if (! exists $seqHash{$sequence}){
   		$seqHash{$sequence}{freqofWi} = 1;		  
} else {
   		$seqHash{$sequence}{freqofWi}++; 
}
push @{$seqHash{$sequence}{read}}, $header;

close SEQUENCE_FILE;
} #\\end of read fasta sub

@keys = keys %seqHash; 
@sort = sort {length($b) <=> length($a) || $seqHash{$b} <=> $seqHash{$a}} @keys; 

foreach my $seq (@sort) {
	$length = length($_);
	$abundance =  $seqHash{$_}; 
	$currSeqW_List = WordList ($seq, $wordSize); 
		if (%otuHash) {
			makeOTU($seq, $abundance, $currSeqW_List);
			} else {
			$tempBestScore = scoreOTU ($currSeqW_List);
			if ($tempBestScore >= $threshold){
				#updateOTU ();
			} else {
				makeOTU($seq, $abundance, $currSeqW_List);
				}
			}
	}

####### SUBROUTINES ######
sub scoreOTU {
 (@wordList) = @_;
 
 my $bestScore = -999;
 my $totalwordCount = 0; 
 my $sedSeq;  
 my $sumScoreforOTU = 0;
 my $CurrScoreforWord;
 my $freqofWi; 
 
 	foreach $seqWord (@wordList){
 		if (exists $otuHash{$otuName}{word}{$word}){
 		
 			$totalwordCount = $otuHash{$otuName}{totalCount}; 
 			$freqofWi = $seqHash{$sequence}{freqofWi};
 			$sedSeq = $otuHash{$otuName}{seedSeq} = $sequence; 
 			$CurrScoreforWord = (($freqofWi/$totalwordCount) * (length($sedSeq)/length($sequence));
 			$sumScoreforOTU += $CurrScoreforWord; 
 			
 		 } else {
 			continue; 
 		 }
		 
 	if $sumScoreforOTU >= $bestScore {
 		$bestScore = $sumScoreforOTU;
 		}
 	}
	return $bestScore;
}

sub WordList{
	($sequence, $wordSize) = $_; 
	my @wordList = ();
	
	my $length = length($sequence); 
	my $word;  

	for my $i (0..$length-($wordSize+1)){
		$word = substr ($sequence, $i, $i+$wordSize);
		push @wordList, $word;		
}
	return @wordList; 
}

sub makeOTU {
($sequence, $abundance) = $_;
(@wordList) = @_;

 my $otuName;
 my $totalCount;
 
 foreach my $word (@wordList) {
 $otuHash{$otuName}{totalCount}++; 
 $otuHash{$otuName}{seedSeq} = $sequence;
 $otuHash{$otuName}{read} = [$header];
 $otuHash{$outName}{word}{$word} = $abundance;
 }
 
 push @{$otuHash}{$otuName}{read}, $header;
}	

