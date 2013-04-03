#! perl

#use strict;
use warnings;
use Data::Dumper;

my $input = shift;
my $output = shift;
my $trim = shift;
my $thresh = shift;

if(!defined($thresh))
{
die "You did not enter a correct input file, output file, trim length, or threshold: $!\n"
}
open IN, "<$input";
open OUT, ">$output";


my %Seq_Hash;
my %WordHash;
my %OTU_Hash;
my ($line, $SeqName, $seq, $seq_length, $name, $read_in_seq, $word, $end, $score, $word_freq, $total_OTU_words, $OTU_length);  
my $num_of_reads = 1;
my $uniq = 0;
my $word_length;

$line = <IN>;
chomp $line;

$read_in_seq = "";

while($line = <IN>) {	
	if ($line =~ /^>(\w+)\|/) {
	$num_of_reads ++;
		if($line ne "") {
	$SeqName = $1;
	$line = "";
	}
	}
	else {
		if($line ne "") {
		chomp $line;
		$read_in_seq = $line; # sequence can be on multiple lines
		$seq_length = length($read_in_seq) - $trim;
		$seq = substr($read_in_seq, 0, $seq_length);
		#print OUT $seq;
			
				 if(exists $Seq_Hash{$seq}){
					$Seq_Hash{$seq} +=1;
					}
				 else{
					 $Seq_Hash{$seq} = 1;
					 $uniq ++;	 
				 }
				 
				$end = $seq_length-7;
				for(my $i =0; $i <= $end; $i++) { #  end=length(seq)-8+1
				$word = substr($seq, $i, 8);
	
				 if(exists $Seq_Hash{$seq}){
					$Seq_Hash{$seq}{name} = $SeqName;
					$Seq_Hash{$seq}{words} = $word;
					$Seq_Hash{$seq}{$word}{word_count} ++;
				 }
				 else{
					$Seq_Hash{$seq}{name} = $SeqName;
					$Seq_Hash{$seq}{words} = $word;
					$Seq_Hash{$seq}{$word}{word_count} =1;
				 }	
				} 
				 
	#print OUT ($seq_length, "\t", $seq, "\n");
		 }
	}
		 

}




#foreach $word (keys (%WordHash))  {

#$score = (($word_freq/$total_OTU_words);
#print OUT ($word, "\t", $word_freq, "\t", $name, "\n");

#}


 my @keys = keys %Seq_Hash;
 my @sorted_keys = sort{ length($b) <=> length($a) || $Seq_Hash{$b} <=> $Seq_Hash{$a}} @keys;

foreach (@sorted_keys){
$word_freq = $Seq_Hash{$seq}{$word}{word_count} ++;
$name = $Seq_Hash{$seq}{name};
my $word_output = $Seq_Hash{$seq}{words};
my $word_count = $Seq_Hash{$seq}{$word}{word_count} ++;
$total_OTU_words = length($seq)-7;

$score = (($word_freq/$total_OTU_words)*(length($seq)/(length($seq))));

print OUT ("Length:", length($_ ), "\t", "word freq:", $word_freq, "\t", "seq_name:", $name, "\t", "words", $word_output, "\t", "word_count", $word_count, "abundance:", $Seq_Hash{$_} ,"score:", $score, "\n" );

}

print OUT ("Total Number of Reads In File:", $num_of_reads, "\n");
print OUT ("Total Number of Unique Reads:", $uniq );


close IN;
close OUT;	

exit;
	


