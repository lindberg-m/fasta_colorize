#!/usr/bin/env python
from sys import argv, stdin, exit

usage = """Colorize the nucleotides in a fasta file

    usage: fasta_colorize [-h] [infile]

        -h       Show this help and exit
        infile   Path to fasta file, reads from stdin if ommited
"""

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

ansi_prefix = '\033['

color_map = {'A' : 'yellow', 'a' : 'yellow', 
             'C' : 'blue', 'c' : 'blue', 
             'G' : 'green', 'g' : 'green', 
             'T' : 'red', 't' : 'red'}

nuc_remap = {x : ansi_prefix + ansi_colors_fg[color_map[x]] + 'm' + x for x in "ACTGactg"}

def reset_char(char):
    return ansi_prefix + '0m' + char

def color_char(char):
    try:
        return nuc_remap[char]
    except KeyError:
        return reset_char(char)

def color_string(string):
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
            print(reset_char(line))
        else:
            print(color_string(line))

    close(input_handle)

