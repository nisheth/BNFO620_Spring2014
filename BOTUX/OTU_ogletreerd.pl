use warnings;
use strict;
use Data::Dumper;

my $inputfile = shift;
my $outputfile = shift;
my $trim = shift;
my $threshold = shift;

my %seqHash;
my %otuHash;

my $wordSize = 8;
my $otucount = 1;
my @keys;
my @sort;
my $currSeqW_List;
my $tempBestScore;
my $tempBestOTU;
my $abundance;
my $totalRead =0; 
 
if (!defined ($threshold)) {
die "USAGE: Please provide an input file, output file, trimlength, and a threshold.";
}

open SEQUENCE_FILE, "$inputfile" or die "Can't open $inputfile: $!\n";
open OUTFILE, ">$outputfile" or die "USAGE: Can't open $outputfile: $!\n";

my $SEED_FILE = 'OTU_SEED.txt';
my $FREQUENCY_FILE = 'OTU_FREQUENCY.txt';
my $ASSIGNMENT_FILE = 'OTU_ASSIGNMENT.txt';
my $WORD_FILE = 'OTU_WORD.txt';

open (my $outSEED, '>', $SEED_FILE) or die "Could not open file '$FREQUENCY_FILE' !";
open (my $outFREQ, '>', $FREQUENCY_FILE) or die "Could not open file '$FREQUENCY_FILE' !";
open (my $outASSIGN, '>', $ASSIGNMENT_FILE) or die "Could not open file '$ASSIGNMENT_FILE' !";
open (my $outWORD, '>', $WORD_FILE) or die "Could not open file '$WORD_FILE' !";

readFasta();

@keys = keys %seqHash;
@sort = sort {length($b) <=> length($a) || $seqHash{$b}{freqofWi} <=> $seqHash{$a}{freqofWi}} @keys;

foreach my $seq (@sort) {
  my $len = length($seq);
  
  if($len > 10 ) { 
    if(exists $seqHash{$seq}{freqofWi}) {   
      $abundance = $seqHash{$seq}{freqofWi};  
    } else { 
      $abundance = 0;
      print "$seq not found in hash.\n";
    }  
    
    $currSeqW_List = WordList ($seq, $wordSize);

    if ($otucount == 1) {
  	  makeOTU($seq, $abundance, $currSeqW_List);
  	 } else {
  	 ($tempBestScore,$tempBestOTU) = scoreOTU ($seq, $currSeqW_List);
      if ($tempBestScore >= $threshold){
  	       updateOTU($seq, $abundance, $currSeqW_List);
  	   } else {
  	       makeOTU($seq, $abundance, $currSeqW_List);
  		  }
  	}
  }
}

printFrequency();

exit;

########## SUBROUTINES ############
sub printFrequency{
  my @headerArray;
  my ($count,$percentage);
  foreach my $otuName (keys %otuHash){
    @headerArray = @{$otuHash{$otuName}{read}};
    $count = @headerArray;
    $percentage = ($count/ $totalRead);
    print $outFREQ "$otuName\t$count\t$percentage\n"; #### WORKS FOR FREQ DONE
  }
}

sub readFasta { 
   my $line;
   my $header;
   my $sequence = "";
   my $firstline = 1;
   my $length;
   my $seq;
   my $unique;
   
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
	$unique++;
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

	if (!exists $seqHash{$sequence}){
    $seqHash{$sequence}{freqofWi} = 1;
} else {
    $seqHash{$sequence}{freqofWi}++;
}
push @{$seqHash{$sequence}{read}}, $header;
}
return;
}

sub WordList{
my ($sequence, $wordSize) = @_;

my @wordList = ();
my $word;

for my $i (0..length($sequence)-($wordSize+1)){
$word = substr ($sequence, $i, $wordSize);
push @wordList, $word;
}
return \@wordList;
}

sub scoreOTU {
my ($sequence,$wordListRef) = @_;
 
 my $bestScore = -999;
 my $bestOTU = "";
 my $totalwordCount = 0;
 my $sedSeq;
 my $sumScoreforOTU = 0;
 my $CurrScoreforWord;
 my $freqofWi;
 my $avgScore = 0;
 my $otuName;

 foreach my $otuName (keys %otuHash) {

 $sumScoreforOTU = 0;
 $totalwordCount = $otuHash{$otuName}{totalCount};

 foreach my $word (@$wordListRef){
   if (exists $otuHash{$otuName}{word}{$word}){
      $freqofWi = $otuHash{$otuName}{word}{$word};
      $CurrScoreforWord = ($freqofWi /$totalwordCount) ;
      $sumScoreforOTU += $CurrScoreforWord;
    }
  } # for loop end for wordlist
 
  $sedSeq = $otuHash{$otuName}{seedSeq};
  $sumScoreforOTU *= (length($sedSeq)/length($sequence));
  
  if ($sumScoreforOTU >= $bestScore) {
  $bestScore = $sumScoreforOTU;
  $bestOTU = $otuName;
  }

print $outASSIGN "@{$seqHash{$sequence}{read}}, $otuName, $bestScore\n"; #####WORKS ASSIGN FILE DONE
 }
return ($bestScore, $bestOTU);
}

sub makeOTU {
my ($sequence, $abundance,$wordListRef) = @_;
my $header;
my $otuName = "OTU_".$otucount;
my $totalCount;
my $i = 1; 
$otucount++;

$otuHash{$otuName}{totalCount} = 0;
$otuHash{$otuName}{seedSeq} = $sequence;

 foreach my $word (@$wordListRef) {
 $otuHash{$otuName}{totalCount} += $abundance;
 $otuHash{$otuName}{word}{$word} = $abundance;

print $outWORD "$otuName, $word, $abundance\n"; ###WORKS WORD FILE DONE
 }
 
 foreach $header (@{$seqHash{$sequence}{read}}) {
  push @{$otuHash{$otuName}{read}}, $header;
  $totalRead++;
 }

print $outSEED "\t", $otuHash{$otuName}{seedSeq}, "\n"; ###WORKS SEED FILE DONE
}

sub updateOTU {
my ($sequence, $abundance,$wordListRef) = @_;

my $otuName = "";
my $totalCount;
my $header;

 foreach my $word (@$wordListRef) {
 $otuHash{$otuName}{totalCount}++;

if(exists $otuHash{$otuName}{word}{$word}) {
     $otuHash{$otuName}{word}{$word} += $abundance;
} else {
$otuHash{$otuName}{word}{$word} = $abundance;
	}
}
 foreach $header (@{$seqHash{$sequence}{read}}) {
  push @{$otuHash{$otuName}{read}}, $header;
  }
}

close SEQUENCE_FILE;
close OUTFILE;
