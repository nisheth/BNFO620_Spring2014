#! /usr/bin/env python

import argparse
import os.path
import sys


SEED_FILE = 'OTU_seed.txt'
FREQ_FILE = 'OTU_frequency.txt'
ASS_FILE = 'OTU_Assignment.txt'
WORD_FILE = 'OTU_word.txt'
freqs = {}


class Sequence:
    """
    Holds data for a particular sequence. Implemented comparison functions lt, gt, eq based on length of sequence first,
    then based on abundance of sequence. Implemented len based on length of sequence. Implemented string representation
    as standard FASTA record.

    Python doesn't have static variables, so the module-level global dict freqs{} will be used to fake it.
    """
    # TODO: Add list of IDs that correspond with a given sequence
    # TODO: Add list of words in the sequence, window size = 8

    def __init__(self, defline = None, sequence = None):
        self.defline = defline
        self.sequence = sequence
        if sequence:
            self.length = len(sequence)
        else:
            self.length = None
        # can probably remove this if, and keep the code in the else; this logic is more or less
        # handled by the de-dup strategy in main(), I think
        if sequence in freqs:
            freqs[sequence] += 1
        else:
            freqs[sequence] = 1

    def __str__(self):
        """
        Assumes that the input sequence defline will be stripped of the leading '>' elsewhere, otherwise output will
        feature two of them.
        """

        return '>{}\n{}'.format(self.defline, self.sequence)

    def __len__(self):
        return self.length

    def __lt__(self, other):
        if self.length == other.length:
            return freqs[self.sequence] < freqs[other.sequence]
        else:
            return self.length < other.length

    def __gt__(self, other):
        if self.length == other.length:
            return freqs[self.sequence] > freqs[other.sequence]
        else:
            return self.length > other.length

    def __eq__(self, other):
        if self.length == other.length:
            return freqs[self.sequence] == freqs[other.sequence]
        else:
            return self.length == other.length


class CustomParser(argparse.ArgumentParser):
    # pass
    def error(self, message):
        sys.stderr.write('error: {}\n'.format(message))
        self.print_help()
        sys.exit(2)


def set_up_parser():
    """
    A simple argv parser, looks for one input file and one output directory (positional, mandatory); desired trim
    length and threshold value (flags, optional)
    """

    # parser = argparse.ArgumentParser()
    parser = CustomParser(formatter_class = argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('in_file',
                        metavar = 'input_file'.upper(),
                        help = 'The fully-qualified path to the FASTA input file')
    parser.add_argument('out_dir',
                        metavar = 'output_directory'.upper(),
                        help = 'The fully-qualified path to the desired output directory')
    parser.add_argument('-t',
                        dest = 'trim_length',
                        help = 'Trim sequences to the specified length',
                        required = False,
                        default = None)
    parser.add_argument('-v',
                        dest = 'threshold',
                        metavar = 'threshold_value'.upper(),
                        help = 'help',
                        required = False,
                        default = 0.65)
    return parser


def parse_args(parser):
    """
    Returns a dict of the parsed command-line args; the default behavior would otherwise return
    a Namespace object. The dict seems easier to work with at this point.
    """
    return vars(parser.parse_args())


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
        print '{:4}: {} {}'.format(i, s.length, freqs[s.sequence])
        if i % 100 == 0:
            raw_input("Press enter to continue...")
        i += 1


def main():
    # TODO: add FASTQ handler
    args = parse_args(set_up_parser())
    infile = args['in_file']
    outdir = args['out_dir']

    # don't want to proceed if the input source or output target don't exist
    err = has_bad_args(infile, outdir)
    if err:
        for bad_arg in err:
            print "ERROR: target \"{}\" not found".format(bad_arg)
        sys.exit(1)

    seqs = []
    ifh = open(infile, 'r')
    while True:
        header = ifh.readline()
        sequence = ifh.readline()
        if not sequence:
            break
        header = header.rstrip()
        header = header.lstrip('>')
        sequence = sequence.rstrip()
        # print 'lenght = {}'.format(len(sequence))
        if args['trim_length'] and len(sequence) > int(args['trim_length']):
            # print 'Trimming to {}'.format(args['trim_length'])
            sequence = sequence[:int(args['trim_length'])]
        # print 'lenght = {}'.format(len(sequence))
        # roughing in a de-duplication strategy with this if-else
        if sequence not in freqs:
            seqs.append(Sequence(header, sequence))
        else:
            freqs[sequence] += 1
    ifh.close()
    seqs.sort(reverse = True)
    test1(seqs)
    seed_out, freq_out, ass_out, word_out = fully_qualify_output_files(outdir)


if __name__ == '__main__':
    main()