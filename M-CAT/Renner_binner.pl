use strict;
use warnings;
use POSIX;

my $inputref = shift;
my $inputgi = shift;
my $outfile = shift;
my $binsize = shift;

if(!defined($binsize)){
    die "USAGE: perl $0 input reference file, input gi file, output file, bin size\n";
}

my ($line, $gi, $taxid, $tax, $mod, $seqlength, $iteration, $i, $j, $printstat, $start, $end);
my $seq = "";
my $binnum = 1;
my $bincount = 1;
my %gihash;
my (@value,@giarray,@seqarray);

open IFH, "<$inputgi" or die "Error in opening gi file $inputgi\n";

while($line = <IFH>){
    chomp $line;
    @value = split(/\t/, $line);
    $gi = $value[0];
    $taxid = $value[1];
    $gihash{$gi} = $taxid;
}

close IFH;

open IFH2, "<$inputref" or die "Error in opening genome file $inputref\n";

while($line = <IFH2>){
    chomp $line;
    if($line =~ />/){
        @value = split(/\|/, $line);
        $gi = $value[1];
  
	if(exists($gihash{$gi})){
	    $tax = $gihash{$gi};
	}

        push(@giarray, $gi);
        push(@seqarray, $seq);
	$seq = "";
    }
    else{
        $seq .= $line;
    }
}

close IFH2;

push(@seqarray, $seq);
shift(@seqarray);

open OFH, ">$outfile" or die "Error in opening outfile $outfile\n";

for($i = 0; $i < scalar(@giarray); $i++){
    $mod = length($seqarray[$i]) % $binsize;
    
#  print "$seqarray[5]\n";
# print "$mod\n";

    if($mod < ($binsize/2)){
	$iteration = int(length($seqarray[$i])/$binsize);
    }
    else{
	$iteration = int((length($seqarray[$i])/$binsize) + 1);
    }

# print "$iteration\n";
    
    $start = 1;
    $end = ($binsize);
    $bincount = 1;

    for($j = 1; $j <= $iteration; $j++){
	$seqlength = length($seqarray[$i]);
	
	if($j != $iteration){
	    print OFH "$gihash{$giarray[$i]}\t$giarray[$i]\t$start\t$end\t$bincount\n";
	    $start += $binsize;
	    $end += $binsize;
	    $bincount++;
	}
	else{
	    $end = $seqlength;
	    print OFH "$gihash{$giarray[$i]}\t$giarray[$i]\t$start\t$end\t$bincount\n";
	}
    }
}

close OFH;
exit;
