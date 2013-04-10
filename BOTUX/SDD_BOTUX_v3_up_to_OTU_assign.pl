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
my ($line, $SeqName, $i, $particular_seq, $mom_best, $best, $particular_seq_word_list, $seq, $abundance, $seq_length, $name, $read_in_seq, $word, $score, $word_freq, $total_OTU_words, $OTU_length);	
my $num_of_reads = 1;
my $uniq = 0;
my $arb_sev = 7;
my $arb_eight = 8;
my $mom_max = 0;
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
		} #ends 2nd if loop
		
	} #ends 1st if loop
	
	else {
		if($line ne "") {
		chomp $line;
		$read_in_seq = $line; # sequence can be on multiple lines
		$seq_length = length($read_in_seq) - $trim;
		$seq = substr($read_in_seq, 0, $seq_length);
		#print OUT $seq;
				 if(exists $Seq_Hash{$seq}){
					$Seq_Hash{$seq} +=1;
					#$Seq_Hash{$seq}{name} = $SeqName;
				 }
				 else{
					 $Seq_Hash{$seq} = 1;
					 #$Seq_Hash{$seq}{name} = $SeqName;
					 $uniq ++;	 
				 }	
				push(@{$Seq_Hash{$seq}{name}},$SeqName);  #adds value to the end of array stored in hash by "seq" as key    http://stackoverflow.com/questions/3779213/how-do-i-push-a-value-onto-a-perl-hash-of-arrays
	#print OUT ($seq_length, "\t", $seq, "\n");
		 } #ends if loop
	} #ends else loop
} #ends while loop			 

my @keys = keys %Seq_Hash;
my @sorted_keys = sort{ length($b) <=> length($a) || $Seq_Hash{$b} <=> $Seq_Hash{$a}} @keys;

foreach $seq (keys (%Seq_Hash))  {
#print OUT (length($seq), "\t", $seq, "\t", $Seq_Hash{$seq}, "\n");	
my $Seq_Hash_seq_name = $Seq_Hash{$seq}{name};
#print OUT $Seq_Hash_seq_name ,"\n" ;   ### should work - prints an array reference
}

foreach (@sorted_keys){
$abundance = $Seq_Hash{$_} ;
$particular_seq = length($_ );
$particular_seq_word_list = Create_Words($seq);
print OUT ("Length:", $particular_seq, "\t", "\t", "\t", "abundance:","\t", $abundance , "\t",    "\n" );

	if (%OTU_Hash) {
		Create_OTU($seq, $abundance, $particular_seq_word_list);
	}
	else {
		($best, $max_score ) = Score($seq);
		if ($mom_max >= $thresh) {
		
		}
		else{
		Create_OTU($seq, $abundance, $particular_seq_word_list);
		}
	}
}
print OUT ("Total Number of Reads In File:", $num_of_reads, "\n");
print OUT ("Total Number of Unique Reads:", $uniq );


close IN;
close OUT;	

exit;
	

#there should be approx 7 OTUs in the final result
#change outfiles and such
#compensate for seqs on multiple lines

####################################################################################################################################################################

sub Create_Words {
my ($seq) = @_ ;

my %WordHash;
my $end = length($seq) - $arb_sev;
my $word;
my $arb_eight = 8;
my $arb_seven = 7;
my @WordArray;

	
	for($i=0; $i < $end; $i++) { #  end=length(seq)-8+1
	$word = substr($seq, $i, $arb_eight);
		if (length($word) == 8){
			# if(exists $WordHash{$word}){
			#	$WordHash{$word} +=1;
			# }
			# else{
			#	$WordHash{$word} =1; 
			#}
			push @WordArray, $word;
		} 
	 }
#foreach $word (keys %WordHash) {
#print OUT $word, "\t", $WordHash{$word}, "\n" ;
#}
return \@WordArray;
} # end of Create_Word subroutine



sub Create_OTU {
my ($seq, $abundance, $particular_seq_word_list) = @_ ;
	
	for( my $n = 1; $n < 100; $n ++) {
		my $OTU = "OTU"."_".$n;
	}

	#foreach my $word (keys %WordHash) {
	  # if(exists $OTU_Hash{$OTU}){
	  #		$OTU_Hash{$OTU}{OTU_word_count} +=1;
	#		$OTU_Hash{$OTU}{Seed} = $seq;
		#	$OTU_Hash{$OTU}{word_abundance} = $abundance;
		#}
		#else{
		#	$OTU_Hash{$OTU}{OTU_word_count} =1; 
		#	$OTU_Hash{$OTU}{Seed} = $seq;
		#	$OTU_Hash{$OTU}{word_abundance} = $abundance;
		#}
	 
	foreach my $word (@WordArray) {
		$OTU_Hash{$OTU}{OTU_total_word_count} +=1;
		$OTU_Hash{$OTU}{Seed} = $seq;
		$OTU_Hash{$OTU}{word_abundance}{$word} = $abundance;
	}
	print OUT $OTU;
}  #ends Create_OTU subroutine





sub Score {
my ($seq) = @_;

my $total_word_count = 0;
my $OTU_sum = 0;
my $min_score = 999999999999999;
#my $max_score = -77777777777777;
my ($word_freq, $word_socre, $OTU_word_abundnace, $score, $best, $worst, $seed_seq, $seed_length, $read_length);

	foreach my $OTU (keys %OTU_Hash) {
		$read_length = length($seq);
		$seed_length = length($OTU_Hash{$OTU}{Seed});
		$OTU_word_abundance = $OTU_Hash{$OTU}{word_abundance}{$word};
		$Total_words_in_OTU = $OTU_Hash{$OTU}{OTU_total_word_count};
		$word_score = ($OTU_word_abundance/$Total_words_in_OTU);
		$OTU_sum += $word_score;
		$score = (($OTU_word_abundance/$Total_words_in_OTU) * ($seed_length/$read_length));
		$max_score = $score;
		$best = $OTU;
	}

 return ($best, $max_score);
}  #ends Score subroutine

sub Modify_OTU {
my ($seq, $abundance, $particular_seq_word_list) = @_ ;

for( my $n = 1; $n < 100; $n ++) {
		my $OTU = "OTU"."_".$n;
	}

	foreach $word (@WordArray) {
	
		if(exists $OTU_Hash{$OTU}{word}{$word}) {
			$OTU_Hash{$OTU}{word_abundance}{$word} += $abundance;
		}
		else{
		$OTU_Hash{$OTU}{OTU_total_word_count} +=1;
		$OTU_Hash{$OTU}{word_abundance}{$word} = $abundance;
		}
	}
} #ends Modify_OTU subroutine
