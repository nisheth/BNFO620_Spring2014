use strict;
use warnings;
use POSIX;

my $inputref = shift;
my $inputgi = shift;
my $outfile = shift;
my $binsize = shift;

if(!defined($binsize)){
    die "USAGE: perl $0 input reference file, input gi file, output file, binsize\n";
}

my ($line, $gi, $taxid,$tax,$mod, $iteration, $i, $seqlength,$printstat,$start,$end);
my $binnum = 1;
my $bincount = 1;
my %gihash;
my @value;

open IFH, "<$inputgi" or die "Error in opening gi file $inputgi\n";

#Read in gi file and parse out gi value and taxid into hash for later
while($line = <IFH>){
    chomp $line;
    @value = split(/\t/, $line);
    $gi = $value[0];
    $taxid = $value[1];
    $gihash{$gi} = $taxid;
}

close IFH;

open IFH2, "<$inputref" or die "Error in opening genome file $inputref\n";

#Read in ref file and parse out gi value, associate with previous hash
while($line = <IFH2>){
    chomp $line;
    if($line =~ />gi/){
  @value = split(/\|/, $line);
	$gi = $value[1];

	if(exists($gihash{$gi})){
	    $tax = $gihash{$gi};
	}
    } 
    else{
	#Determine iteration number for later for loop, number of bins
	$mod = length($line) % $binsize;
	if($mod < ($binsize/2)){
	    $iteration = int(length($line)/$binsize);
	}
	else{
	    $iteration = int((length($line)/$binsize) + 1);
	}

	$start = 0;
	$end = ($binsize-1);

	#Seperate and print bins
	for($i=1;$i <= $iteration;$i++){
	    $seqlength = length($line);

	    if($i != $iteration){
		print "$tax\t$gi\t$start\t$end\t$bincount\n"; 
		$start += $binsize;
		$end += $binsize;
		$bincount++;
	    }

	    else{
		$end = $seqlength;
		print "$tax\t$gi\t$start\t$end\t$bincount\n"; 
	    }

	}

    }

}




