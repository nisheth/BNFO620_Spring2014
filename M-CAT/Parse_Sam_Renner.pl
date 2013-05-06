use strict;
use warnings;

my $inbin = shift;
my $insam = shift;
my $out = shift;

if(!defined($out)){
    die "USAGE: perl $0 bin file, sam file, out file\n";
}

my ($i, $line, $tax, $match, $mismatch, $mdmatch, $mdmismatch, $mdcount, $gi, $start, $end, $bin, $taxbin, $samtax, $cigar, $samstart, $mdlong, $md, $cigarcount, $score, $max);
my (@value, @data, @cigarArray, @mdArray, @sams);
my (%taxHash, %bins, %binCount);
$max = -99999;

############### Read in bin file and store it for later use
open IFH, "<$inbin" or die "Error in opening bin file $inbin\n";

while($line = <IFH>){
    chomp $line;
    @value = split(/\t/, $line);
    $tax = $value[0];
    $gi = $value[1];
    $start = $value[2];
    $end = $value[3];
    $bin = $value[4];

    $taxbin = "$tax" . "-" . "$bin";

    $bins{$taxbin} = [$tax, $start, $end, $bin, $gi];
    $taxHash{$gi} = $tax;
  
#    print "$bins{$taxbin}[1]\n";
}

close IFH;

################## Begin processing of Sam file, splitting out and storing information
open IFH2, "<$insam" or die "Error in opening sam file $insam\n";

while($line = <IFH2>){
    chomp $line;
    @data = ();
    @value = split(/\|/, $line);
    $samtax = $value[1];

    @value = split(/\s+/, $line);
    $cigar = $value[5];
    $samstart = $value[3];
    
    $line =~ /MD:Z:(\S+)\s+/;
    $md = $1;

    push(@data, ($samtax, $samstart, $cigar, $md));

################# Gathering information from cigar string to use in scoring

    @cigarArray = ();
    $cigarcount = 0;
    $match = 0;
    $mismatch = 0;
    @cigarArray = $cigar =~ /([0-9]+)([A-Z]+)/g;

#    print "$cigarArray[1]\n";

    for($i = 0; $i < scalar(@cigarArray); $i++){
	if($cigarArray[$i] eq "M"){
	    $cigarcount += $cigarArray[($i-1)];
	    $match += $cigarArray[($i-1)];
	}
	elsif($cigarArray[$i] eq "I"){
	    $cigarcount += $cigarArray[($i-1)];
	    $mismatch += $cigarArray[($i-1)];
	}
	elsif($cigarArray[$i] eq "D"){
	    $cigarcount -= $cigarArray[($i-1)];
	    $mismatch += $cigarArray[($i-1)];
	}
    }

#    print "$md\n";
################# Same process as above, just for MD

    @mdArray = ();
    $mdcount = 0;
    $mdmatch = 0;
    $mdmismatch = 0;
    @mdArray = $md =~/([0-9]+)([A-Z]|\^[A-Z]+)/g;

    for($i = 0; $i < scalar(@mdArray); $i++){
	if($mdArray[$i] =~ /([0-9]+)/){
	    $mdcount += $mdArray[$i];
	    $mdmatch += $mdArray[$i];
	}
	elsif($mdArray[$i] eq "A" | $mdArray[$i] eq "G" | $mdArray[$i] eq "C" | $mdArray[$i] eq "T"){
	    $mdcount++;
	    $mdmismatch++;
	}
	######### Next else takes care of ^ deletions
	else{
	    $mdcount--;
	    $mdmismatch++;
	}
    }

################ Scoring, five percent deduction

    if($match != 0){
	$score = (($mdmatch-$mdmismatch)/$match) * 100;
    }

    if($score > $max){
	$max = $score;
    }

    push(@sams, ($data[0], $data[1], $score));

#    print "$sams[0]\t$sams[1]\t$sams[2]\n";
#    print "$data[0]\t$data[1]\t$data[2]\t$data[3]\t$max\n";

}

$max -= 5;

##############Counting and output

while($taxbin = each (%bins)){
#print "$bins{$taxbin}[0]\n";
#print "$sams[0]\n";
    if($sams[2] >= $max){
	    if($sams[0] == $bins{$taxbin}[0]){
	      if($sams[1] >= $bins{$taxbin}[1] && $sams[1] <= $bins{$taxbin}[2]){
		      if(exists($binCount{$taxbin})){
		        $binCount{$taxbin}[2]++;
		      } 
		      else{
		        $binCount{$taxbin} = ($bins{$taxbin}[4], $bins{$taxbin}[3], 1);
		      }   
	      }
      }
    }
}

open OFH, ">$out" or die "Error in opening out file $out\n";
print OFH "Tax\tBin\tCount\n";

foreach $taxbin (sort keys %binCount){
    print OFH "$binCount{$taxbin}[0]\t$binCount{$taxbin}[1]\t$binCount{$taxbin}[2]\n";
}
