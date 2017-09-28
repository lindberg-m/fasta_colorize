#!/usr/bin/env python
from sys import argv, stdin, exit

usage = """Colorize the nucleotides in a fasta file

    usage: fasta_colorize [-h] [infile]

        -h       Show this help and exit
        infile   Path to fasta file, reads from stdin if ommited
"""

class SeqColor(object):
   ansi_prefix = '\033['
   reset_code = '0m'

   BLACK = '30'
   RED = '31'
   GREEN = '32'
   YELLOW = '33'
   BLUE = '34'
   MAGENTA = '35'
   CYAN = '36'
   WHITE = '37'
   
   ADENINE = (['a', 'A'], YELLOW)
   CYTOSINE = (['c', 'C'], GREEN)
   GUANINE = (['g', 'G'], MAGENTA)
   THYMINE = (['t', 'T'], RED)

   nuc_map = {}
   for nuc_codes, color in [ADENINE, CYTOSINE, GUANINE, THYMINE]:
       for code in nuc_codes:
           nuc_map[code] = color

   def __init__(self):
       self.color_code = self.ansi_prefix + self.reset_code
       self.on_reset = True

   def colorize_char(self, char):
       return self.color_code + char

   def set_color_code(self, char):
       try:
           self.color_code = self.ansi_prefix + self.nuc_map[char] + 'm'
           self.on_reset = False
       except KeyError:
           if self.on_reset:
               self.color_code = ''
           else:
               self.color_code = self.ansi_prefix + self.reset_code
               self.on_reset = True

   def colorize_string(self, string):
       ret = []
       for char in string:
           self.set_color_code(char)
           ret.append(self.colorize_char(char))

       return ''.join(ret)

   def reset_color(self, char):
       self.color_code = self.ansi_prefix + self.reset_code
       self.on_reset = True
       return self.ansi_prefix + self.reset_code + char
   

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

    colorizer = SeqColor()
    for line in input_handle:
        line = line.strip()
        if line.startswith('>'):
            print(colorizer.reset_color(line))
        else:
            print(colorizer.colorize_string(line))

    close(input_handle)

