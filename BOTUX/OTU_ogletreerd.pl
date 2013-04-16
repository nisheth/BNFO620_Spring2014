use strict;
use warnings;

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

if (!defined ($threshold)) {
die "USAGE: Please provide an input file, output file, trimlength, and a threshold.";
}

open SEQUENCE_FILE, "$inputfile" or die "Can't open $inputfile: $!\n";
open OUTFILE, ">$outputfile" or die "USAGE: Can't open $outputfile: $!\n";

readFasta();

@keys = keys %seqHash;
@sort = sort {length($b) <=> length($a) || $seqHash{$b}{freqofWi} <=> $seqHash{$a}{freqofWi}} @keys;

foreach my $seq (@sort) {
  my $len = length($seq);
  
  if(exists $seqHash{$seq}{freqofWi}) {   
    $abundance = $seqHash{$seq}{freqofWi};  
  } else { 
    $abundance = 0;
    print "$seq not found in hash.\n";
  }  
  print "Abudance = $abundance\n";

  $currSeqW_List = WordList ($seq, $wordSize);

  if ($otucount == 1) {
	  makeOTU($seq, $abundance, $currSeqW_List);
	 } else {
	 ($tempBestScore,$tempBestOTU) = scoreOTU ($seq, $currSeqW_List);
   print "$tempBestScore,$tempBestOTU,\n $seq\n";
    if ($tempBestScore >= $threshold){
	       updateOTU($seq, $abundance, $currSeqW_List);
	   } else {
	       makeOTU($seq, $abundance, $currSeqW_List);
		  }
	}
}

#Printing Here!
print OUTFILE "\nBest Score\tLength\tAbundance\n";

exit;



sub readFasta { 
####### SUBROUTINES ######

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
    print "$header\t$unique\n";
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
 
 foreach my $otuName (keys %otuHash) {
 print "OTU NAMe = $otuName in otu score method\n"; 
 $sumScoreforOTU = 0;
  $totalwordCount = $otuHash{$otuName}{totalCount};
  print "$otuName,$totalwordCount\n";
 foreach my $word (@$wordListRef){
    
   if (exists $otuHash{$otuName}{word}{$word}){
 
      $freqofWi = $otuHash{$otuName}{word}{$word};
      $CurrScoreforWord = ($freqofWi /$totalwordCount) ;
      $sumScoreforOTU += $CurrScoreforWord;
      print "$otuName, $word,$freqofWi,$totalwordCount,$CurrScoreforWord\n";
    }
  } # for loop end for wordlist
  print "$otuName,$sumScoreforOTU\n";
  
  $sedSeq = $otuHash{$otuName}{seedSeq};
  print "SEED seq = $sedSeq\n";
  $sumScoreforOTU *= (length($sedSeq)/length($sequence));
  print "$otuName,$sumScoreforOTU\n";

  if ($sumScoreforOTU >= $bestScore) {
  $bestScore = $sumScoreforOTU;
  $bestOTU = $otuName;
  }
 }
return ($bestScore, $bestOTU);
}

sub makeOTU {
my ($sequence, $abundance,$wordListRef) = @_;
my $header;
my $otuName = "OTU".$otucount;
my $totalCount;
my $i = 1; 
$otucount++;

$otuHash{$otuName}{totalCount} = 0;
print "In makeOTU, $sequence, $abundance\t$otuName\n";

$otuHash{$otuName}{seedSeq} = $sequence;

 foreach my $word (@$wordListRef) {
 $otuHash{$otuName}{totalCount} += $abundance;
 $otuHash{$otuName}{word}{$word} = $abundance;
# print "$otuName,$word,$abundance\n";
 }
 
 foreach $header (@{$seqHash{$sequence}{read}}) {
  push @{$otuHash{$otuName}{read}}, $header;
 }

print "SEED seq = $otuHash{$otuName}{seedSeq}\n";
}

sub updateOTU {
my ($sequence, $abundance,$wordListRef) = @_;

my $otuName;
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
