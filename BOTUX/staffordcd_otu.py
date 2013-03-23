#! /usr/bin/env python

import argparse
import os.path


SEED_FILE = 'OTU_seed.txt'
FREQ_FILE = 'OTU_frequency.txt'
ASS_FILE = 'OTU_Assignment.txt'
WORD_FILE = 'OTU_word.txt'


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


def main():
    args = parse_args(set_up_parser())
    infile = args['in_file']
    outdir = args['out_dir']
    seed_out, freq_out, ass_out, word_out = fully_qualify_output_files(outdir)
    # don't want to process anything if the input source or output target don't exist
    # with open(infile, 'r') as ifh,


if __name__ == '__main__':
    main()