use strict;
use warnings;

my $infile = shift;
my $ref = shift;
my $outfile = shift;
my $name = shift;

if(!defined($name)){
    die "USAGE: perl $0 input file, reference, outfile, projectname\n";
}

my $samformat1 = "$outfile"."/"."$name"."_1".".sam";
my $samformat2 = "$outfile"."/"."$name"."_2".".sam";
my $bamformat1 = "$outfile"."/"."$name"."_1".".bam";
my $bamformat2 = "$outfile"."/"."$name"."_2".".bam";
my $sortformat1 = "$outfile"."/"."$name"."_1_sorted.bam";
my $sortformat2 = "$outfile"."/"."$name"."_2_sorted.bam";
my $mergeformat = "$outfile"."/"."$name"."_merged.bam";
my $finalformat = "$outfile"."/"."$name"."_results.sam";
my $command;

unless(-e $samformat1){
    $command = "/home/bnfo620/bin/bowtie2-2.0.6/bowtie2 -p 4 -x "."$ref"." -U "."$infile"." -S "."$samformat1";
    runSystemCommand($command);
    
    $ref =~ s/1/2/;
    $command = "/home/bnfo620/bin/bowtie2-2.0.6/bowtie2 -p 4 -x "."$ref"." -U "."$infile"." -S "."$samformat2";
    runSystemCommand($command);
}

unless(-e $bamformat1){
    $command = "/home/bnfo620/bin/samtools view -bS "."$samformat1"." > "."$bamformat1";
    runSystemCommand($command);

    $command = "/home/bnfo620/bin/samtools view -bS "."$samformat2"." > "."$bamformat2";
    runSystemCommand($command);
}

$command = "/home/bnfo620/bin/samtools sort -no "."$bamformat1"." "."$sortformat1";
runSystemCommand($command);

$command = "/home/bnfo620/bin/samtools sort -no "."$bamformat2"." "."$sortformat2";
runSystemCommand($command);

$command = "/home/bnfo620/bin/samtools cat -o "."$mergeformat"." "."$sortformat1"." "."$sortformat2";
runSystemCommand($command);

$command = "/home/bnfo620/bin/samtools view -h "."$mergeformat"." > "."$finalformat";
runSystemCommand($command);


sub runSystemCommand {
    my $cmd = shift;
    `$cmd`;
}
