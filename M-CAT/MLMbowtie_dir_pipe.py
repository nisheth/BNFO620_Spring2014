import sys
import os
import sample_pipe as bp

def runSystemCMD(cmd):
    print "Running below command using qsub ..."
    print cmd
    qsub_cmd = "qsub /home/martinezml2/qsub_general.sh \'" + cmd + "\'"
    bp.runSystemCMD(qsub_cmd)

def main():

    if len(sys.argv) < 4 :
        print "USAGE: python sys.argv[0] input-dir output-dir index1 index2 \n"
        sys.exit()

    indir = sys.argv[1]
    outdir = sys.argv[2]
    index1 = sys.argv[3]
    index2 = sys.argv[4]

    filepath = indir
    files = os.listdir(filepath)
    for filename in files:
        if filename.endswith("1x.1.fastq"):
            read1 = indir + filename
            read2 = indir + filename.replace("1x.1.fastq","1x.2.fastq")
            projectname = filename.replace(".1x.1.fastq","_bowtie_merged.bam")
            projectname1 = filename.replace(".1x.1.fastq","_index1")

            print read1
            print read2
            print projectname
            print projectname1

            cmd = "python sample_pipe.py " + read1 + " " + read2 + " " + index1 + " " + projectname1 + " " + outdir

            runSystemCMD(cmd)

            projectname2 = projectname1.replace("_index1","_index2")
            print projectname2
            cmd = "python sample_pipe.py " + read1 + " " + read2 + " " + index2 + " " + projectname2 + " " + outdir

            runSystemCMD(cmd)


            cmd = "/home/bnfo620/bin/samtools cat -o " + outdir+ projectname + " " + outdir + projectname1 + "_bowtie_sorted.bam " + outdir + projectname2 + "_bowtie_sorted.bam"

            print cmd
            runSystemCMD(cmd)

            merged = projectname.replace(".bam",".sam")

            cmd = "/home/bnfo620/bin/samtools view " +outdir+ projectname + " > " + outdir+ merged

            runSystemCMD(cmd)

if __name__ == '__main__':
    main()

