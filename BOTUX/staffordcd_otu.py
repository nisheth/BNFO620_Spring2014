#! /usr/bin/env python

import argparse
import os.path
import sys
import re


SEED_FILE = 'OTU_seed.txt'
FREQ_FILE = 'OTU_frequency.txt'
ASS_FILE = 'OTU_Assignment.txt'
WORD_FILE = 'OTU_word.txt'


class Sequence:
    """
    Holds data for a particular sequence. Implemented comparison functions lt, gt, eq based on length of sequence first,
    then based on abundance of sequence. Implemented len based on length of sequence.
    """
    def __init__(self, defline = None, sequence = None, word_size = 8):
        self.deflines = []
        self.add_header(defline)
        self.sequence = sequence
        self.words = {}
        if sequence:
            self.length = len(sequence)
            self.make_words(sequence, word_size)
        else:
            self.length = None

    def __len__(self):
        return self.length

    def __lt__(self, other):
        if self.length == other.length:
            return self.get_abundance() < other.get_abundance()
        else:
            return self.length < other.length

    def __gt__(self, other):
        if self.length == other.length:
            return self.get_abundance() > other.get_abundance()
        else:
            return self.length > other.length

    def __eq__(self, other):
        if self.length == other.length:
            return self.get_abundance() == other.get_abundance()
        else:
            return self.length == other.length

    def make_words(self, sequence, word_size):
        for i in xrange(len(sequence) - word_size + 1):
            word = sequence[i:word_size + i]
            if word in self.words:
                self.words[word] += 1
            else:
                self.words[word] = 1

    def add_header(self, header):
        self.deflines.append(header)

    def increment_word_count(self):
        for (word, count) in self.words.items():
            self.words[word] += 1

    def get_abundance(self):
        return len(self.deflines)


class OTU:
    def __init__(self, seq, words, read_id):
        """
        With add_words and add_id, I'm trying to keep the implementation logic independent from how the methods
        are used, in case I decide to change things in the future. The call will stay the same, but the actual steps
        performed by the method might not.
        """
        self.seed_seq = seq
        self.words = {}
        self.add_words(words)
        self.read_ids = []
        self.add_id(read_id)
        # upon creation, the OTU will have an average score of 100% (it's totally identical to itself)
        self.avg_score = 1

    def __str__(self):
        return '{}\n'.format(self.read_ids)

    def add_id(self, read_id):
        # looks like the += operator has the desired effect of keeping the list flat
        self.read_ids += read_id

    def add_words(self, words):
        # TODO: make sure this is working correctly in tandem with the word building in the Sequence class
        for word in words:
            if word in self.words:
                self.words[word] += int(words[word])
            else:
                self.words[word] = 1

    def add_score(self, score):
        self.avg_score += score
        self.avg_score /= float(2)

    def tally_words(self):
        return sum(self.words.values())

    def get_seed_seq(self):
        return self.seed_seq

    def get_num_reads(self):
        """
        The number of reads assigned to an OTU is the same as the number of elements in the read_ids list
        """
        return len(self.read_ids)

    def get_word_and_freq(self):
        return self.words


class CustomCLOptionParser(argparse.ArgumentParser):
    def error(self, message):
        sys.stderr.write('error: {}\n'.format(message))
        self.print_help()
        sys.exit(2)


def set_up_CL_parser():
    """
    A simple argv parser, looks for one input file and one output directory (positional, mandatory); desired trim
    length, fastq format, word size, and threshold value (flags, optional)
    """

    parser = CustomCLOptionParser(formatter_class = argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('in_file',
                        metavar = 'input_file'.upper(),
                        help = 'The fully-qualified path to the input file.')
    parser.add_argument('-fq',
                        action = 'store_true',
                        help = 'Set input file type to FASTQ',
                        default = False)
    parser.add_argument('out_dir',
                        metavar = 'output_directory'.upper(),
                        help = 'The fully-qualified path to the desired output directory')
    parser.add_argument('-t',
                        dest = 'trim_length',
                        help = 'Trim sequences to the specified length',
                        required = False,
                        type = int,
                        default = None)
    parser.add_argument('-v',
                        dest = 'threshold',
                        metavar = 'threshold_value'.upper(),
                        help = 'Minimum threshold for calling a \"match\" between a sequence and an OTU',
                        required = False,
                        type = float,
                        default = 0.65)
    parser.add_argument('-w',
                        dest = 'word_size',
                        help = 'Desired word size',
                        required = False,
                        type = int,
                        default = 8)
    return parser


def parse_args(parser):
    """
    Returns a dict of the parsed command-line args; the default behavior would otherwise return
    a Namespace object. The dict seems easier to work with at this point.
    """
    return vars(parser.parse_args())


def parse_fasta(fasta_file):
    header, sequence = None, []
    for line in fasta_file:
        line = line.rstrip()
        if line.startswith(">"):
            if header:
                yield (header, ''.join(sequence))
            header, sequence = line.lstrip('>'), []
        else:
            sequence.append(line)
    if header:
        yield (header, ''.join(sequence))


def parse_fastq(fastq_file):
    """
    Note: assumes a "standard" 4-line fastq formatted file. Results may be unpredictable otherwise.
    """
    header, sequence, score = None, None, None
    for line in fastq_file:
        line = line.rstrip()
        if line.startswith('@'):
            if header:
                yield (header, sequence, score)
            header, sequence, score = line.lstrip('@'), None, None
        elif line.startswith('+'):
            # don't really care about the tag line
            continue
        elif re.match('^[A-Za-z]', line):
            sequence = line
        else:
            score = line
    if header:
        yield (header, sequence, score)


def fully_qualify_output_files(outdir):
    """
    Using the output dir specified on the command line, and the pre-established file names declared
    as constants above, build up the output file names
    """
    so = os.path.abspath('{}/{}'.format(outdir, SEED_FILE))
    fo = os.path.abspath('{}/{}'.format(outdir, FREQ_FILE))
    ao = os.path.abspath('{}/{}'.format(outdir, ASS_FILE))
    wo = os.path.abspath('{}/{}'.format(outdir, WORD_FILE))
    return so, fo, ao, wo


def has_bad_args(*args):
    """
    Ascertains whether the given files or directories exist on disk.
    """
    bad_args = []
    for arg in args:
        if os.path.exists(arg):
            continue
        else:
            bad_args.append(arg)
    return bad_args


def test1(seqs):
    i = 1
    for s in seqs:
        print '{:4}: {} {}'.format(i, s.length, s.get_abundance())
        if i % 100 == 0:
            raw_input("Press enter to continue...")
        i += 1


def read_fasta_file(ifh, trim_to, seqs, word_size):
    for h, s in parse_fasta(ifh):
        if trim_to and len(s) > int(trim_to):
            s = s[:int(trim_to)]
        if s not in seqs:
            seqs[s] = Sequence(h, s, word_size)
        else:
            seqs[s].add_header(h)
            seqs[s].increment_word_count()
    return seqs


def bin_reads(reads, OTUs, threshold):
    i = 1
    first_seq = True
    for read in reads:
        if i % 50 == 0:
            print 'Binning read {}'.format(i)
        i += 1
        if first_seq:
            OTUs.append(OTU(read.sequence, read.words, read.deflines))
            first_seq = False
        else:
            max_score = -999
            best_otu = None
            for curr_otu in OTUs:
                score = score_read(read, curr_otu)
                if score > max_score:
                    max_score = score
                    best_otu = curr_otu
            if max_score >= threshold:
                # print "Found best score {} in OTU {}.\nadd to current otu".format(max_score, best_otu.read_ids)
                best_otu.add_words(read.words)
                best_otu.add_id(read.deflines)
                best_otu.add_score(max_score)
                # print "added to current otu.\nNum OTUs:{}".format(len(OTUs))
                # raw_input("Waiting...")
            else:
                # print "max {} smaller than threshold {}, make new otu".format(max_score, threshold)
                OTUs.append(OTU(read.sequence, read.words, read.deflines))
                # print "new OTU created.\nNum OTUs:{}".format(len(OTUs))
                # raw_input("Waiting...")


def score_read(read, otu):
    # TODO pull this into OTU class, let it take a Seq obj but the logic remains largely the same
    running_total = 0.0
    for word in read.words:
        # print "Looking for {}".format(word)
        # print "{} found {} times".format(word, otu.words.get(word, 0))
        running_total += (otu.words.get(word, 0) / float(otu.tally_words()))
        # print "running total: {}".format(running_total)
    running_total *= (len(otu.seed_seq) / float(len(read.sequence)))
    # print running_total
    return running_total


def printOTUs(otus):
    i = 1
    for o in otus:
        print "OTU {}: {} members".format(i, len(o.read_ids))
        i += 1


def print_seeds(outfile, OTUs):
    ofh = open(outfile, 'w')
    i = 1
    # print "Simulate writing to {}".format(outfile)
    for o in OTUs:
        ofh.write('OTU{}\t{}\n'.format(i, o.seed_seq))
        # print 'OTU{}\t{}'.format(i, o.seed_seq)
        i += 1
    ofh.close()


def print_freqs(outfile, OTUs):
    ofh = open(outfile, 'w')
    i = 1
    # print "Simulate writing to {}".format(outfile)
    for o in OTUs:
        ofh.write('OTU{}\t{}\t{}\n'.format(i, o.get_num_reads(), o.avg_score))
        # print 'OTU{}\t{}\t{}'.format(i, o.get_num_reads(), o.avg_score)
        i += 1
    ofh.close()


def print_words(outfile, OTUs):
    ofh = open(outfile, 'w')
    i = 1
    # print "Simulate writing to {}".format(outfile)
    for o in OTUs:
        total = 0
        for w in o.words:
            # print 'OTU{}\t{}\t{}'.format(i, w, o.words[w])
            ofh.write('OTU{}\t{}\t{}\n'.format(i, w, o.words[w]))
            total += o.words[w]
        # print 'OTU{} total words\t{}'.format(i, total)
        ofh.write('OTU{} total words\t{}\n'.format(i, total))
        i += 1
    ofh.close()


def print_assignment(outfile, OTUs):
    ofh = open(outfile, 'w')
    i = 1
    # print 'Simulate writing to {}'.format(outfile)
    for o in OTUs:
        for r in o.read_ids:
            # print '{} in OTU{}'.format(r, i)
            ofh.write('{}\tOTU{}\t{}\n'.format(r, i))
        i += 1
    ofh.close()


def main():
    # TODO: add FASTQ handler
    # TODO: add paired-end read handler
    args = parse_args(set_up_CL_parser())
    infile = args['in_file']
    outdir = args['out_dir']
    word_size = args['word_size']
    threshold = args['threshold']

    # don't want to proceed if the input source or output target don't exist
    err = has_bad_args(infile, outdir)
    if err:
        for bad_arg in err:
            print "ERROR: target \"{}\" not found".format(bad_arg)
        sys.exit(1)

    seqs = {}
    OTUs = []
    if not args['fq']:
        ifh = open(infile, 'r')
        read_fasta_file(ifh, args['trim_length'], seqs, word_size)
        ifh.close()
    else:
        ifh = open(infile, 'r')
        seqs = parse_fastq(ifh)
        ifh.close()
    sorted_seqs = seqs.values()
    sorted_seqs.sort(reverse = True)
    first_sequence = True
    bin_reads(sorted_seqs, OTUs, threshold)
    # test1(sorted_seqs)
    # printOTUs(OTUs)
    # print len(OTUs)
    seed_out, freq_out, ass_out, word_out = fully_qualify_output_files(outdir)
    print_seeds(seed_out, OTUs)
    print_freqs(freq_out, OTUs)
    print_words(word_out, OTUs)
    print_assignment(ass_out, OTUs)


if __name__ == '__main__':
    main()
