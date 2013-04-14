##Kanika Sharma
## Created OTU
use strict;
use warnings;

##### Variable declaration #######
my $infile = shift;
my $trimLength = shift;
my $threshold = shift;
my $outfile = shift; 

my %SeqHash;
my %HashOfOtu; 
my $window = 8;
my @keys;
my @sorted_values;
my $SeqWordList;
my $curBestScore; 
my $line; 
my $seq; 
my $trimSeq; 
my $header; 
my $seqLen; 
my $seqLen1; 
my $Abund; 
my $occurWords =0; 

if (!defined($outfile)){
	die "Error Msg: Please enter an infile, trimlength, threshold and an outfile\n";
} # end if

###### Open Files ######
open IFH, "$infile" or die "Cannot open/locate the $infile\n";
#open OFH, ">$outfile" or die "Cannot write to the $outfile\n"; 

##### MAIN METHOD ########
while($line = <IFH>){
	if($line =~ /^>(.*)/g) {
		chomp $line; 
		$header = $1; 
		#print $header, "\n";
	} # end if
	else {
		$seq = ""; 
		$seq .= $line;  
		$seqLen = length($seq);
		if ($seqLen > $trimLength){
			$seq = substr($seq, 0, $trimLength);
		} # end if
		#print $seq, "\n\n"; 
		if(exists $SeqHash{$seq}){
			$SeqHash{$seq}{$occurWords}++; 
		} # end if 
		else {
			$SeqHash{$seq}{$occurWords} = 1; 
		}
		push @{$SeqHash{$seq}{read}}, $header; 
		#print $seqLen, "\n"; 
	} # end else
	
} # end while

close IFH; 

@keys = keys %SeqHash; 
@sorted_values = sort {length($b) <=> length($a) || $SeqHash{$b} <=> $SeqHash{$a}} @keys; 

my $word; 
my @wordList; 
foreach(@sorted_values){
	#print $_, "\n\n"; 
	$seqLen1 = length($_);
	$Abund = $SeqHash{$_};
foreach my $i (0..$seqLen1-($window+1)){
	$word = substr($_, $i, $window); 
	#print $word, "\n\n";
	push @wordList, $word; 
} # end of second foreach
	if(%HashOfOtu){
		createOtu($seq, $Abund, $wordList[$_]);
	} else {
		$curBestScore = createScore($seq,$wordList[$_]); 
	}
	if ($curBestScore >= $threshold) {
		OTUupdate($seq, $Abund,$wordList[$_]); 
	}
	else {
		createOtu($seq, $Abund, $wordList[$_]);
	}
} # end first foreach


sub createOtu{
	my ($seq, $abund, $ListWRef) = @_;
	
	my $otu;
	my $totalCount; 
	my $word; 
	
	foreach(@$ListWRef){
		$HashOfOtu{$otu}{totalC}++;
		$HashOfOtu{$otu}{seedSeq}= $seq;
		$HashOfOtu{$otu}{word}{$word} = $abund; 
	} # end foreach
	
	foreach (@{$SeqHash{$seq}{read}}){
		push @{$HashOfOtu{$otu}{read}}, $header; 
	}
} # createOTU

sub createScore {
	my ($seq, $ListWRef) = @_;
	my $max_score=-999;
	my $otu;
	my $totalCount =0;	
	my $seedSeq;
	my $totalSum;
	my $atMomentScore;
	my $occWord; 
	
	foreach(keys %HashOfOtu){
		foreach my $Wlist (@$ListWRef){
			if(exists $HashOfOtu{$otu}{$word}){
				$totalCount = $HashOfOtu{$otu}{totalC};
				$occWord = $HashOfOtu{$otu}{word}{$word}; 
				$atMomentScore = ($occWord/$totalCount); 
				$totalSum += $atMomentScore; 
			} # end if
		} # end second foreach
	} # end first foreach
	
} # end ScoreOTU

sub OTUupdate {
my ($sequence, $abund,$ListWRef) = @_;


 my $otu;
 my $totalCount;
 
 foreach my $word (@$ListWRef) {
 $HashOfOtu{$otu}{totalCount}++; 

	if(exists $HashOfOtu{$otu}{word}{$word}){
    		$HashOfOtu{$otu}{word}{$word} += $abund;
	} else { 
		$HashOfOtu{$otu}{word}{$word} = $abund;	
	}	

}
 foreach (@{$SeqHash{$seq}{read}}) {
 	push @{$HashOfOtu{$otu}{read}}, $header;
 }	
}
