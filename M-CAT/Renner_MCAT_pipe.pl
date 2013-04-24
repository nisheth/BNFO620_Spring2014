use strict;
use warnings;

my $infile = shift;
my $infile2 = shift;
my $ref = shift;
my $outfile = shift;
my $name = shift;

if(!defined($name)){
    die "USAGE: perl $0 input file1, input file2, reference, out directory, projectname\n";
}

unless(-e $outfile or mkdir $outfile){
    die "Unable to create $outfile\n";
}

my $samformat1 = "$outfile"."/"."$name"."_1".".sam";
my $samformat2 = "$outfile"."/"."$name"."_2".".sam";
my $bamformat1 = "$outfile"."/"."$name"."_1".".bam";
my $bamformat2 = "$outfile"."/"."$name"."_2".".bam";
my $sortformat1 = "$outfile"."/"."$name"."_1_sorted".".bam";
my $sortformat2 = "$outfile"."/"."$name"."_2_sorted".".bam";
my $mergeformat = "$outfile"."/"."$name"."_merged.bam";
my $finalformat = "$outfile"."/"."$name"."_results.sam";
my $command;

my $bowtiepath = "/home/bnfo620/bin/bowtie2-2.0.6/bowtie2";
my $samtoolspath = "/home/bnfo620/bin/samtools";

unless(-e $samformat1){
    $command = "$bowtiepath -p 4 -1 $infile -2 $infile2 -x $ref -S $samformat1";
    print "Starting $command\n";
    runSystemCommand($command);
    
    $ref =~ s/1/2/;
    $command = "$bowtiepath -p 4 -1 $infile -2 $infile2 -x $ref -S $samformat2";
    print "Starting $command\n";
    runSystemCommand($command);
}

unless(-e $bamformat1){
    $command = "$samtoolspath view -bS $samformat1 > $bamformat1";
    print "Starting $command\n";
    runSystemCommand($command);

    $command = "$samtoolspath view -bS $samformat2 > $bamformat2";
    print "Starting $command\n";
    runSystemCommand($command);
}

unless(-e $sortformat1){
    $command = "$samtoolspath sort -no $bamformat1 placeholder > $sortformat1";
    print "Starting $command\n";
    runSystemCommand($command);

    $command = "$samtoolspath sort -no $bamformat2 placeholder >  $sortformat2";
    print "Starting $command\n";
    runSystemCommand($command);
}

$command = "$samtoolspath cat -o $mergeformat $sortformat1 $sortformat2";
print "Starting $command\n";
runSystemCommand($command);


$command = "$samtoolspath view $mergeformat > $finalformat";
print "Starting $command\n";
runSystemCommand($command);


sub runSystemCommand {
    my $cmd = shift;
    `$cmd`;
}
