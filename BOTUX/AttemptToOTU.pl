##Kanika Sharma
## Created OTU
use strict;
use warnings;

##### Variable declaration #######
my $infile = shift;
my $trimLength = shift;
my $threshold = shift;
my $outfile = shift; 

my %HSeq;
my %H_otu; 
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
open OFH, ">$outfile" or die "Cannot write to the $outfile\n"; 

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
		if(exists $HSeq{$seq}){
			$HSeq{$seq}{$occurWords}++; 
		} # end if 
		else {
			$HSeq{$seq}{$occurWords} = 1; 
		}
		push @{$HSeq{$seq}{read}}, $header; 
		#print $seqLen, "\n"; 
	} # end else
	
} # end while

close IFH; 

@keys = keys %HSeq; 
@sorted_values = sort {length($b) <=> length($a) || $HSeq{$b} <=> $HSeq{$a}} @keys; 

my $word; 
my @wordList; 
foreach(@sorted_values){
	#print $_, "\n\n"; 
	$seqLen1 = length($_);
	$Abund = $HSeq{$_};
foreach my $i (0..$seqLen1-($window+1)){
	$word = substr($_, $i, $window); 
	#print $word, "\n\n";
	push @wordList, $word; 
} # end of second foreach
	if(%H_otu){
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


###########SUBROUTINES##################

sub createOtu{
	my ($seq, $abund, $ListWRef) = @_;
	
	my $otu;
	my $totalCount; 
	my $word; 
	
	foreach(@$ListWRef){
		$H_otu{$otu}{totalC}++;
		$H_otu{$otu}{seedSeq}= $seq;
		$H_otu{$otu}{W}{$_} = $abund; 
	} # end foreach
	
	foreach (@{$HSeq{$seq}{read}}){
		push @{$H_otu{$otu}{read}}, $_; 
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
	
	foreach $otu (keys %H_otu){
		foreach my $W(@$ListWRef){
			if(exists $H_otu{$otu}{W}{$W}){
				$totalCount = $H_otu{$otu}{totalC};
				$occWord = $H_otu{$otu}{W}{$W}; 
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
 $H_otu{$otu}{totalCount}++; 

	if(exists $H_otu{$otu}{word}{$word}){
    	$H_otu{$otu}{word}{$word} += $abund;
	} else { 
		$H_otu{$otu}{word}{$word} = $abund;	
	}	

} # end foreach

 foreach (@{$HSeq{$seq}{read}}) {
 	push @{$H_otu{$otu}{read}}, $_;
 }	
} ## end OTUupdate


close OFH; 
