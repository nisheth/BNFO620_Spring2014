#! /usr/bin/env python

import argparse
import os.path
import sys


SEED_FILE = 'OTU_seed.txt'
FREQ_FILE = 'OTU_frequency.txt'
ASS_FILE = 'OTU_Assignment.txt'
WORD_FILE = 'OTU_word.txt'


class Sequence:
    """
    Holds data for a particular sequence
    """
    def __init__(self, defline = None, length = None, sequence = None):
        self.defline = defline
        self.sequence = sequence
        if sequence:
            self.length = len(sequence)

    def __str__(self):
        return '>{}\n{}'.format(self.defline, self.sequence)

    def __lt__(self, other):
        pass

    def __gt__(self, other):
        pass

    def __eq__(self, other):
        pass



def set_up_parser():
    """
    A simple argv parser, looks for one input file and one output directory
    """
    parser = argparse.ArgumentParser()
    parser.add_argument('-i',
                        dest = 'in_file',
                        metavar = 'input_file',
                        help = 'The fully-qualified path to the FASTA input file',
                        required = True)
    parser.add_argument('-o',
                        dest = 'out_dir',
                        metavar = 'output_directory',
                        help = 'The fully-qualified path to the desired output directory',
                        required = True)
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


def main():
    args = parse_args(set_up_parser())
    infile = args['in_file']
    outdir = args['out_dir']

    # don't want to proceed if the input source or output target don't exist
    err = has_bad_args(infile, outdir)
    if err:
        for bad_arg in err:
            print "ERROR: path \"{}\" not found".format(bad_arg)
        sys.exit(1)

    seed_out, freq_out, ass_out, word_out = fully_qualify_output_files(outdir)


if __name__ == '__main__':
    main()