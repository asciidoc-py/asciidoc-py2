#!/usr/bin/env python
import os, sys
from optparse import *

__AUTHOR__ = "Gouichi Iisaka <iisaka51@gmail.com>"
__VERSION__ = '1.1'

class EApp(Exception):
    '''Application specific exception.'''
    pass

class Struct:
    '''variable contenor as C `struct'.'''
    pass

class Application():
    '''
NAME
    graphviz2png - Converts textual graphviz notation to PNG file

SYNOPSIS
    graphviz2png [options] INFILE

DESCRIPTION
    This filter reads Graphviz notation text from the input file
    INFILE (or stdin if INFILE is -), converts it to a PNG image file.


OPTIONS
    -o OUTFILE
        The file name of the output file. If not specified the output file is
        named like INFILE but with a .png file name extension.

    -v
        Verbosely print processing information to stderr.

    --help, -h
        Print this documentation.

    --version
        Print program version number.

SEE ALSO
    graphviz(1)

AUTHOR
    Written by Gouichi Iisaka, <iisaka51@gmail.com>

THANKS
    Stuart Rackham, <srackham@gmail.com>
    This script was inspired by his music2png.py and AsciiDoc

LICENSE
    Copyright (C) 2008 Gouichi Iisaka.
    Free use of this software is granted under the terms of
    the GNU General Public License (GPL).
    '''

    def __init__(self, argv=None):
        if not argv:
            argv = sys.argv
        self.attrs = Struct()
        self.usage_msg = '%prog [options] inputfile\n'
        self.usage_msg += 'Version: %s\n' % __VERSION__
        self.usage_msg += 'Copyright(c) 2008: %s' % __AUTHOR__

        self.option_list = [
            Option("-o", "--outfile", action="store",
		    dest="outfile",
		    help="Output file"),
            Option("-L", "--layout", action="store",
		    dest="layout", default="dot",
		    help="Output file"),
            Option("--debug", action="store_true",
		    dest="do_debug",
		    help=SUPPRESS_HELP),
            Option("-v", "--verbose", action="store_true",
		    dest="do_verbose", default=False,
		    help="verbose output"),
            Option("-V", "--version", action="store_true",
		    dest="do_version",
		    help="Print version"),
	    ]

        self.parser = OptionParser(option_list=self.option_list)
        self.parser.set_usage(self.usage_msg)
        (self.options, self.args) = self.parser.parse_args()

	if self.options.do_version:
            self.parser.print_usage()
            sys.exit(1)

	if len(self.args) != 1:
            self.parser.print_help()
            sys.exit(1)

        self.options.infile = self.args[0]

    def systemcmd(self, cmd):
        if self.options.do_verbose:
            msg = 'Execute: %s' % cmd
            sys.stderr.write(msg + os.linesep)
        else:
            cmd += ' 2>/dev/null'
        if os.system(cmd):
            raise EApp, 'failed command: %s' % cmd

    def graphviz2png(self, infile, outfile):
        '''Convert Graphviz notation in file infile to
           PNG file named outfile.'''

        outfile = os.path.abspath(outfile)
        outdir = os.path.dirname(outfile)

        if not os.path.isdir(outdir):
            raise EApp, 'directory does not exist: %s' % outdir

        basefile = os.path.splitext(outfile)[0]
        saved_cwd = os.getcwd()
        os.chdir(outdir)
        try:
            cmd = '%s -Tpng "%s" > "%s"' % (
                        self.options.layout, infile, outfile)
            self.systemcmd(cmd)
            os.unlink(infile)
        finally:
            os.chdir(saved_cwd)

    def run(self):
        if self.options.infile == '-':
            if self.options.outfile is None:
                sys.stderr.write('OUTFILE must be specified')
                sys.exit(1)
            infile = os.path.splitext(self.options.outfile)[0] + '.txt'
            lines = sys.stdin.readlines()
            open(infile, 'w').writelines(lines)

        if not os.path.isfile(infile):
            raise EApp, 'input file does not exist: %s' % infile

        if self.options.outfile is None:
            outfile = os.path.splitext(infile)[0] + '.png'
        else:
            outfile = self.options.outfile

        self.graphviz2png(infile, outfile)

        # To suppress asciidoc 'no output from filter' warnings.
        if self.options.infile == '-':
            sys.stdout.write(' ')

if __name__ == "__main__":
    app = Application()
    app.run()
