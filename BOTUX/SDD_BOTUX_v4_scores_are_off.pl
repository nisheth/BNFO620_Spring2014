#! perl

use strict;
use warnings;
use Data::Dumper;

my $input = shift;
#my $output = shift;
my $trim = shift;
my $thresh = shift;

if(!defined($thresh))
{
die "You did not enter a correct input file, trim length, and threshold: $!\n"
}
open IN, "<$input";
#open OUT, ">$output";
open SEED, ">SDD_Seed.txt";
open SCORE, ">SDD_Scoring.txt";
open WORD, ">SDD_WORDS_AND_WORD_FREQUENCY.txt";
open OTU, ">SDD_OTUs_AND_INFO.txt";


my %Seq_Hash;
my %WordHash;
my %OTU_Hash;
my @WordArray = ();
my ($line, $SeqName, $i, $particular_seq, $mom_best, $best, $particular_seq_word_list, $seq, $abundance, $seq_length, $name, $read_in_seq, $word, $score, $word_freq, $total_words_in_OTU, $OTU_length);  
my ($max_score, $OTU, $OTU_word_abundance, $word_score);
my $num_of_reads = 1;
my $Total_OTUs = 1;
my $uniq = 0;
my $end = 0;
my $arb_sev = 7;
my $arb_eight = 8;
my $mom_max = "";
my $word_length;

$line = <IN>;
chomp $line;

$read_in_seq = "";

while($line = <IN>) {
	
	if($line =~ /^>(.*)/g) {
	$num_of_reads ++;
	
		if($line ne "") {
		$SeqName = $1;
		$line = "";
		#print $SeqName, "\n";
		} #ends 2nd if loop
		#print $SeqName, "\n";
	} #ends 1st if loop
	 
	
	else {
		if($line ne "") {
		chomp $line;
		$read_in_seq = $line; # sequence can be on multiple lines
		}
	} #ends else loop
		
			if (length($read_in_seq) > $trim) {
			$seq_length = length($read_in_seq) - $trim;
			}
			else {
			$seq_length = length($read_in_seq);
			}
			
		$seq = substr($read_in_seq, 0, $seq_length);
		#print OUT $seq;
				 if(exists $Seq_Hash{$seq}){  # 
					$Seq_Hash{$seq}{count} +=1;
				 }
				 else{
					 $Seq_Hash{$seq}{count} = 1;
					 $uniq ++;	 
				 }	
				push(@{$Seq_Hash{$seq}{name}}, $SeqName);  #adds value to the end of array stored in hash by "seq" as key    http://stackoverflow.com/questions/3779213/how-do-i-push-a-value-onto-a-perl-hash-of-arrays
	#print OUT ($seq_length, "\t", $seq, "\n");
		 #} #ends if loop
	
} #ends while loop			

	  

my @keys = keys %Seq_Hash;
my @sorted_keys = sort{ length($b) <=> length($a) || $Seq_Hash{$b} <=> $Seq_Hash{$a}} @keys;

#foreach $seq (keys (%Seq_Hash))  {
#print OUT (length($seq), "\t", $seq, "\t", $Seq_Hash{$seq}, "\n");	
#}    ########################if you need to check what the seq and length thereof is doing - use this loop

foreach $seq (@sorted_keys){
#$abundance = $Seq_Hash{$seq}{count} ;
# print $abundance; die;
#$particular_seq = length($seq);
$particular_seq_word_list = Create_Words($seq);
#print Dumper @WordArray; die;
# print ("Length:", $particular_seq, "\t", "\t", "\t", "abundance:","\t", $abundance , "\t",    "\n" );
	if (exists $Seq_Hash{$seq}{count})  {
		$abundance = $Seq_Hash{$seq}{count} ;
		}
	else{
	$abundance = 0;
	}
	
	#if (%OTU_Hash) {
	if ($Total_OTUs == 1){
	Create_OTU($seq, $abundance, $particular_seq_word_list);
	}
	else {
	($best, $max_score ) = Score($seq, $particular_seq_word_list);
		if ($max_score >= $thresh) {
		Modify_OTU($seq, $abundance, $particular_seq_word_list);
		}
		else{
		Create_OTU($seq, $abundance, $particular_seq_word_list);
		}
	}


}
#print OUT ("Total Number of Reads In File:", $num_of_reads, "\n");
#print OUT ("Total Number of Unique Reads:", $uniq );


close IN;
close SEED;	
close SCORE;
close WORD;
close OTU;

exit;
	

#there should be approx 7 OTUs in the final result
#change outfiles and such
#compensate for seqs on multiple lines

####################################################################################################################################################################

sub Create_Words {
my ($seq) = @_ ;

my $word;
$end = length($seq) - $arb_sev;

	for($i=0; $i < $end; $i++) { #  end=length(seq)-8+1 so that it's inclusive
	$word = substr($seq, $i, $arb_eight);
		if (length($word) == 8){
			push @WordArray, $word;
		} 
	 }
#print $word, "\n";
#print WORD @WordArray;
return \@WordArray;

} 

####################################################################################################################################################################

sub Create_OTU {
my ($seq, $abundance, $particular_seq_word_list) = @_ ;
$OTU = "OTU"."_".$Total_OTUs;
$Total_OTUs ++;
$OTU_Hash{$OTU}{OTU_total_word_count} = 0;

#print ($OTU,"\n");
		
    $OTU_Hash{$OTU}{Seed} = $seq;
	
	#print WORD("----------------------------------------------------------","\n");
	foreach my $word (@$particular_seq_word_list) {   ####### ?!@#?!@$!@$?!@$?!@$?!$@
		$OTU_Hash{$OTU}{OTU_total_word_count} += $abundance;
		$OTU_Hash{$OTU}{word_abundance}{$word} = $abundance;
		print WORD $OTU, "\t", $word, "\t", $abundance, "\n";
	}
	
	foreach $SeqName (@{$Seq_Hash{$seq}{name}}) {
	push (@{$OTU_Hash{$OTU}{name}}, $SeqName);
	
	
	}
	
	#foreach $OTU (%OTU_Hash) {   ######issue print out seqName
		print SEED ("OTU_Name:", $OTU, "\n", "Sequence_Info=", @{$OTU_Hash{$OTU}{name}}, "\n", $OTU_Hash{$OTU}{Seed}, "\n", "\n");
	#}  

} 	

########################################################################################################################################################################


sub Score {
my ($seq, $particular_seq_word_list) = @_;

my $total_word_count = 0;
my $OTU_sum = 0;
my $min_score = 999999999999999;
my $max_score = -99999999999999;
my $best = "";
my ($word_freq, $word, $OTU_word_abundnace, $score, $seed_seq);
my $read_length = 0;
my $seed_length =0;
my $word_score=0;
	
	
	foreach my $OTU (keys %OTU_Hash) {
	$total_words_in_OTU = $OTU_Hash{$OTU}{OTU_total_word_count};
	$OTU_sum = 0;
	print SCORE ("OTU:", $OTU, "\t", "Words_in_OTU: ", $total_words_in_OTU, "\n");
	
	
	#print $seq;
	
	foreach $word (@$particular_seq_word_list){
		if (exists $OTU_Hash{$OTU}{word_abundance}{$word}) {
		$OTU_word_abundance = $OTU_Hash{$OTU}{word_abundance}{$word};	
		#print FREQ ( $word, "\t", $OTU_word_abundance, "\n");
		#$word_score=0;
		$word_score = ($OTU_word_abundance/$total_words_in_OTU);
		#print SCORE ( "Word_Score:", $word_score, "\n");
		$OTU_sum += $word_score;
		$read_length = length($seq);
		$seed_length = length($OTU_Hash{$OTU}{Seed});
		#print $seed_length, "\n";
		#print $read_length, "\n";
		
		$score = $OTU_sum *($seed_length/$read_length);
		$max_score = $score;
		$best = $OTU;
		}
		
		else {   ###########don't know if this else part is necessary, but maybe.... 
		$OTU_Hash{$OTU}{word_abundance}{$word} = $abundance;
		$OTU_word_abundance = $OTU_Hash{$OTU}{word_abundance}{$word};	
		$word_score = ($OTU_word_abundance/$total_words_in_OTU);
		$OTU_sum += $word_score;
		$read_length = length($seq);
		$seed_length = length($OTU_Hash{$OTU}{Seed});
		$score = $OTU_sum *($seed_length/$read_length);
		$max_score = $score;
		$best = $OTU;
		}    ######### end of else loop that may or may not be necessary...
	}
	
	
	#$score = 0;
	
	print SCORE ("OTU_sum: ", $OTU_sum, "\t", "   Total_OTU_score:   ", $score, "\n");
	#print SCORE ("Read_length:", $read_length, "\t", "Seed_length;", $seed_length, "\t", "Score:", $score, "\n");
	
		#$OTU_sum += $word_score;
	if ($OTU_sum >= $score){
	$max_score = $score;
	$best = $OTU;
	print SCORE ("Best_OTU:  ", $best, "\t", "Max_Scoring_For_OTU:", $max_score, "\n", "\n");
	}
	else{ 
	print SCORE ("Nope The best OTU is still:  ", $best, "with a score of   :", $max_score);
	}
	
}
 return ($best, $max_score);
 
 #print FREQ ("OTU_Name:", $OTU, "\t", "Total_Words_In_OTU:", $OTU_word_abundance, "\n", "Best_OTU=", $best, "\t", "Best_scoring_OTU", );
}  


################################################################################################################################################################################

sub Modify_OTU {
($seq, $abundance, $particular_seq_word_list) = @_ ;



	foreach my $word (@$particular_seq_word_list) {
		$OTU_Hash{$OTU}{OTU_total_word_count} += $abundance;
	
		if(exists $OTU_Hash{$OTU}{word_abundance}{$word}) {
			$OTU_Hash{$OTU}{word_abundance}{$word} += $abundance;
		}
		else{
			$OTU_Hash{$OTU}{word_abundance}{$word} = $abundance;
		}	
	}
	
	foreach $SeqName (@{$Seq_Hash{$seq}{name}}) {
	push @{$OTU_Hash{$OTU}{name}}, "\n",$SeqName;
	}
	#print $Total_OTUs, "\n";
	#print SCORE ("I've made it throught the modify cycle", "\n");
	
	foreach my $OTU (%OTU_Hash) {
	print OTU ("OTU:", $OTU, "\n", @{$OTU_Hash{$OTU}{name}}, "\n");
	} 

} 

		
