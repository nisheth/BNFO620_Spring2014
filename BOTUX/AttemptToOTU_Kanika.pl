##Kanika Sharma
## Created OTU

##### Variable declaration #######
my $file = shift;
my $trimLength = shift;
my $threshold = shift;
my $output = shift;

my $SeedSeqFile = "OTU_SeedSeq.txt";
my $FreqFile = "OTU_Frequency.txt";
my $AssignmentFile = "OTU_Assignment.txt";
my $WordFile = "OTU_Word.txt"; 

open OFH1, ">$SeedSeqFile" or die "Cannot open $SeedSeqFile\n"; 
open OFH2, ">$FreqFile" or die "Cannot open $FreqFile\n"; 
open OFH3, ">$AssignmentFile" or die "Cannot open $AssignmentFile\n"; 
open OFH4, ">$WordFile" or die "Cannot open $WordFile\n"; 


my %HSeq;
my %H_otu;
my $id = "";
my $seq = "";
my $len;
my $GC;
my $hsa_seq_count;
my @seqArray;
my $returnedIndex;
my @id_seq_extractor; 
my @sub_id_extractor;
my $window = 8;
my @keys;
my @sorted_values;
my $SeqWordList;
my $curBestScore=1;
my $line;
my $trimSeq;
my $header;
my $seqLen;
my $seqLen1;
my $Abund;
my $occurWords =0;
my $flag;
if (!defined($file)){
die "Error Msg: Please enter an infile, trimlength, threshold and an outfile\n";
} # end if

##### MAIN METHOD ########
$returnedIndex = parseFASTA($file, $output);
@seqArray = @$returnedIndex;
foreach my $line1 (@seqArray){
@id_seq_extractor = split ('\t',$line1);
    $id = $id_seq_extractor[0];
    @sub_id_extractor = split(' ', $id);
    $id = $sub_id_extractor[0];

    $seq = $id_seq_extractor[1];
    
    $seqLen = lengthSEQ($seq);
	#print $seqLen, "\n\n"; 
	
### TRIM LENGTH THE SEQUENCE###
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
push @{$HSeq{$seq}{read}}, $id;
} # end foreach

my $occurwords =0; 
@keys = keys %HSeq;
@sorted_values = sort {length($b) <=> length($a) || $HSeq{$b}{$occurwords} <=> $HSeq{$a}{$occurwords}} @keys;

my $word;
my @wordList;

foreach $seq (@sorted_values){
$seqLen1 = length($seq);
$Abund = $HSeq{$seq}{$occurwords};
@wordList = ();
foreach my $i (0..$seqLen1-($window+1)){
$word = substr($seq, $i, $window);
#print $word, "\n\n";
push @wordList, $word;
} # end of second foreach
if(%H_otu ==1){
createOtu($seq, $Abund, \@wordList);
} else {
$curBestScore = Calc_Score($seq,\@wordList);
#print $curBestScore; 
}
if ($curBestScore >= $threshold) {
OTUupdate($seq, $Abund,\@wordList);
}
else {
createOtu($seq, $Abund, \@wordList);
}
} # end first foreach


##------------------------------------------------------------------------------------------------------------------------------------##


###########SUBROUTINES##################
sub parseFASTA{
        ############# open files #################
    open (IFH, "$file") or die "Cannot open input file$!\n";
    open (OFH, ">$output") or die "Cannot open output file$!\n";
        # ">" overwrites file, ">>" adds to the end of the existing file

        ########### variable declarations ########
    my $line;
    my $header;
    my $sequence;
    my $flag = 0;
    my $index;
    my @returnedArray;
        while($line = <IFH>) #IFH gives us next line
        {
            chomp $line;
                if($line =~ /^>(.*)/g) # "=~" implies regular expression
                {
                        if ($flag != 0)
                        {
                            $index = "$header\t$sequence";
                            push(@returnedArray, $index);
                                #print "$header\t$sequence\n";
                                ##print OFH "$header\t$sequence\n";
                            $header = $line;
                            $sequence = "";
                        } #end flag if statement
        #                print "$header\n";
        #                <STDIN>;
                        else
                        {
                            $header = $line;
                            $sequence = "";
                            $flag++;
                        } #end inner else statement
                    } # end if condition
                else
                {
                    $sequence .= $line; # concatinates new value onto $sequence
                } # end else
        } # end while
    $index = "$header\t$sequence";
    push(@returnedArray, $index);
        #print "$header\t$sequence\n";
        ##print OFH "$header\t$sequence\n";
    return \@returnedArray; #"\" takes reference to
}

sub lengthSEQ{
    my ($input) = @_;
    my $len;
    $len = length($input);
    #print "Length is -------------------|$len\n";  
    return $len;
}

sub createOtu{
my ($seq, $abund, $ListWRef) = @_;
my $count=0; 
my $totalCount=0;
my $wordin="";
$count++;
my $otu = "Otu".$count; 

$H_otu{$otu}{$totalCount}=0;
print OFH3 "Making $otu |Seq = $seq | Abund = $abund |\n"; 
print OFH3 "Total=$H_otu{$otu}{$totalCount}\n"; 
print OFH3 "Total abund =$abund\n"; 
$H_otu{$otu}{seedSeq}= $seq;
foreach $wordin (@$ListWRef){
print OFH4 "The Words are: $wordin\n"; 
$H_otu{$otu}{$totalCount}++; 
$H_otu{$otu}{W}{$wordin}=$abund; 
} # end foreach
print OFH4 "The total Count =$H_otu{$otu}{$totalCount}\n"; 
print OFH4 "The abundance = $abund\n"; 

foreach my $headLine (@{$HSeq{$seq}{read}}){
push @{$H_otu{$otu}{read}}, $headLine;
#print "Header=@{$H_otu{$otu}{read}}, $headLine\n"; 
}
print OFH1 "Seed_Seq = $H_otu{$otu}{seedSeq}\n\n"; 
} # createOTU

sub Calc_Score {
my ($seq, $ListWRef) = @_;
my $max_score=-999;
my $otu="";
my $theBestOTU; 
my $TotWinOtu =0;	
my $seedSeq="";
my $totalScore=0;
my $atMomentScore=0;
my $occWord=0;
my $seedSq; 

	foreach $otu (keys %H_otu){
		$totalScore=0;
		$TotWinOtu = $H_otu{$otu}{totalC};
		print OFH4 "OTU:$otu||Total_Word_In OTU:$TotWinOtu\n"; 
		foreach my $W(@$ListWRef){
			if(exists $H_otu{$otu}{W}{$W}){
			$occWord = $H_otu{$otu}{W}{$W}; # freq of a word
			print OFH2 "Occurrance of a word: $H_otu{$otu}{W}{$W}\n"; 
			#print $occWord, "\n\n"; 
			$atMomentScore = ($occWord/$TotWinOtu);
			$totalScore += $atMomentScore;
			} # end if
		} # end second foreach
	$seedSq = $H_otu{$otu}{seedSq};
	$totalScore*=(length($seedSq)/length($seq));
	if($totalScore >= $max_score){
		$max_score=$totalScore;
		$theBestOTU = $otu; 
		print OFH3 "Max_Score = $max_score || BestOTU = $theBestOTU\n";
	}
	
	
	} # end first foreach

	return($max_score, $theBestOTU); 
} # end ScoreOTU

sub OTUupdate {
my ($sequence, $abund,$ListWRef) = @_;
 my $otu="";
 my $totalCount;
 
 foreach my $word (@$ListWRef) {
 print $word; 
 $H_otu{$otu}{totalCount}++;

if(exists $H_otu{$otu}{word}{$word}){
    $H_otu{$otu}{word}{$word} += $abund;
} else {
$H_otu{$otu}{word}{$word} = $abund;	
}	

} # end foreach

 foreach my $header(@{$HSeq{$seq}{read}}) {
  push @{$H_otu{$otu}{read}}, $header;
 }	
} ## end OTUupdate

close IFH;
close OFH; 
