#!/usr/bin/env python
usage = """Colorize the nucleotides in a fasta file

    usage: fasta_colorize [-h] [infile]

        -h       Show this help and exit
        infile   Path to fasta file, reads from stdin if ommited
"""

"""
Colorize fastasequences

"""
from sys import argv, stdin, exit
from termcolor import colored

ansi_color_prefix = '\033['
ansi_color_suffix = 'm'
ansi_colors_fg = {
        'black' : '30',
        'red' : '31',
        'green' : '32',
        'yellow' : '33',
        'blue' : '34',
        'magenta' : '35',
        'cyan' : '36',
        'white' : '37'
        }

color_map = {'A' : 'yellow', 'a' : 'yellow', 
             'C' : 'blue', 'c' : 'blue', 
             'G' : 'green', 'g' : 'green', 
             'T' : 'red', 't' : 'red'}

nuc_remap = {x : ansi_color_prefix + ansi_colors_fg[color_map[x]] + ansi_color_suffix + x for x in "ACTGactg"}

def color_char(char):
    try:
        return nuc_remap[char]
    except KeyError:
        return char

def color_string(string):
    """foo"""
    return ''.join(list(map(color_char, string)))

if __name__ == '__main__':
    try:
        cliarg = argv[1]
        if cliarg == '-h' or cliarg == "--help":
            print(usage)
            exit()
        input_handle = open(argv[1], 'r')

        close = lambda x: x.close()
    
    except IndexError:
        input_handle = stdin
        close = lambda x: None

    for line in input_handle:
        line = line.strip()
        if line.startswith('>'):
            print(line)
        else:
            print(color_string(line))

    close(input_handle)

