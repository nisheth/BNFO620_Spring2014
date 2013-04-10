##Kanika Sharma
## Created OTU

##### Variable declaration #######
my $infile = shift;
my $trimLength = shift;
# my $threshold = shift;
my $outfile = shift; 

my %HashOfSeq;
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
my $occurWords; 

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
		if(exists $HashofSeq{$seq}){
			$HashofSeq{$seq}{$occurWords}++; 
		} # end if 
		else {
			$HashofSeq{$seq}{$occurWords} = 1; 
		}
		push @{$HashOfSeq{$seq}{read}}, $header; 
		#print $seqLen, "\n"; 
	} # end else
	
} # end while

close IFH; 

@keys = keys %HashOfSeq; 
@sorted_values = sort {length($b) <=> length($a) || $HashOfSeq{$b} <=> $HashOfSeq{$a}} @keys; 

my $word; 
my @wordList; 
foreach(@sorted_values){
	#print $_, "\n\n"; 
	$seqLen1 = length($_);
	$Abund = $HashOfSeq{$_};
foreach my $i (0..$seqLen1-($window+1)){
	$word = substr($_, $i, $window); 
	#print $word, "\n\n";
	push @wordList, $word; 
} # end of second foreach
	if(%HashOfOtu){
		createOtu($seq, $abund, @wordList);
	} else {
		$curBestScore = createScore($seq,@wordList); 
	}
	if ($curBestScore >= $threshold) {
		OTUupdate($sequence, $abund,$ListWRef); 
	}
	else {
		createOtu($seq, $abund, @wordList);
	}
} # end first foreach


sub createOtu{
	my ($seq, $abund, $ListWRef) = @_;
	
	my $Otu;
	my $totalCount; 
	my $word; 
	
	foreach(@$ListWRef){
		$HashOfOtu{$otu}{totalC}++;
		$HashOfOtu{$otu}{seedSeq}= $seq;
		$HashOfOtu{$otu}{word}{$word} = $abund; 
	} # end foreach
	
	foreach (@HashOfSeq{$seq}{read}){
		push @{$HashOfOtu}{$otu}{read}, $header; 
	}
} # createOTU

sub createScore {
	my ($seq, $ListWRef) = @_;
	my $max_score=-999;
	my $theOTU;
	my $totalCount =0;	
	my $seedSeq;
	my $totalSum;
	my $atMomentScore;
	my $occWord; 
	
	foreach(keys %HashOfOtu){
		foreach (@ListWRef){
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
 $HashOfOtu{$otuName}{totalCount}++; 

	if(exists $HashOfOtu{$otu}{word}{$word})
    		$HashOfOtu{$otu}{word}{$word} += $abund;
	} else { 
		$HashOfOtu{$otu}{word}{$word} = $abund;	
	}	

}
 foreach(@$HashOfSeq{$seq}{read}}) {
 	push @{$HashOfOtu}{$otu}{read}, $header;
 }	
}	
