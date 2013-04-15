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
my $tempBestOTU;
my $abundance;

if (!defined ($threshold)) {
die "USAGE: Please provide an input file, output file, trimlength, and a threshold.";
}

open SEQUENCE_FILE, "$inputfile" or die "Can't open $inputfile: $!\n";
open OUTFILE, ">$outputfile" or die "USAGE: Can't open $outputfile: $!\n";

@keys = keys %seqHash;
@sort = sort {length($b) <=> length($a) || $seqHash{$b} <=> $seqHash{$a}} @keys;

foreach my $seq (@sort) {
$len = length($_);
$abundance = $seqHash{$_};
$currSeqW_List = WordList ($seq, $wordSize);

	if (%otuHash) {
		makeOTU($seq, $abundance, $currSeqW_List);
	} else {
		($tempBestScore,$tempBestOTU) = scoreOTU ($seq, $currSeqW_List);
			if ($tempBestScore >= $threshold){
				UpdateOTU($seq, $abundance, $currSeqW_List);
			} else {
				makeOTU($seq, $abundance, $currSeqW_List);
		}
	}
}

#Printing Here!
#print OUTFILE "\nBest Score\tLength\tAbundance\n"; 

####### SUBROUTINES ######
#sub read_Fasta {
my ($inputfile) = $_;

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
}

if (! exists $seqHash{$sequence}){
    $seqHash{$sequence}{freqofWi} = 1;
} else {
    $seqHash{$sequence}{freqofWi}++;
}
push @{$seqHash{$sequence}{read}}, $header;
#return ($sequence, $header);
#}

sub WordList{
my ($sequence, $wordSize) = $_;

my @wordList = ();
my $word;

for my $i (0..length($sequence)-($wordSize+1)){
$word = substr ($sequence, $i, $i+$wordSize);
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
 foreach my $word (@$wordListRef){
  if (exists $otuHash{$otuName}{word}{$word}){
 
  $totalwordCount = $otuHash{$otuName}{totalCount};
  $freqofWi = $otuHash{$otuName}{word}{$word};
  $CurrScoreforWord = ($freqofWi /$totalwordCount) ;
  $sumScoreforOTU += $CurrScoreforWord;
	}
  } # for loop end for wordlist
  
  $sedSeq = $otuHash{$otuName}{seedseq};
  $sumScoreforOTU *= (length($sedSeq)/length($sequence));

  if ($sumScoreforOTU >= $bestScore) {
  $bestScore = $sumScoreforOTU;
  $bestOTU = $otuName;
  }
 }
return ($bestScore, $bestOTU);
}

sub makeOTU {
my ($sequence, $abundance,$wordListRef) = @_;

my $otuName;
my $totalCount;
 
 foreach my $word (@$wordListRef) {
 $otuHash{$otuName}{totalCount}++;
 $otuHash{$otuName}{seedSeq} = $sequence;
 $otuHash{$otuName}{word}{$word} = $abundance;
 }
 
 foreach $header (@{$seqHash{$sequence}{read}}) {
  push @{$otuHash{$otuName}{read}}, $header;
 }
}

sub updateOTU {
my ($sequence, $abundance,$wordListRef) = @_;

my $otuName;
my $totalCount;
 
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
