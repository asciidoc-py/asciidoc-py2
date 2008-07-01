#!/usr/bin/env python
'''
NAME
    music2png - Converts textual music notation to classically notated PNG file

SYNOPSIS
    music2png [options] INFILE

DESCRIPTION
    This filter reads LilyPond or ABC music notation text from the input file
    INFILE (or stdin if INFILE is -), converts it to classical music notation
    and writes it to a trimmed PNG image file.

    This script is a wrapper for LilyPond and ImageMagick commands.

OPTIONS
    -f FORMAT
        The INFILE music format. 'abc' for ABC notation, 'ly' for LilyPond
        notation.

    -o OUTFILE
        The file name of the output file. If not specified the output file is
        named like INFILE but with a .png file name extension.

    -m
        Skip if the PNG output file is newer that than the INFILE. When
        INFILE is - (stdin) previously retained input is compared.

    -v
        Verbosely print processing information to stderr.

    --help, -h
        Print this documentation.

    --version
        Print program version number.

SEE ALSO
    lilypond(1), abc2ly(1), convert(1)

AUTHOR
    Written by Stuart Rackham, <srackham@gmail.com>

COPYING
    Copyright (C) 2006 Stuart Rackham. Free use of this software is
    granted under the terms of the GNU General Public License (GPL).
'''

import os, sys

VERSION = '0.1.0'

# Globals.
verbose = False

class EApp(Exception): pass     # Application specific exception.

def print_stderr(line):
    sys.stderr.write(line + os.linesep)

def print_verbose(line):
    if verbose:
        print_stderr(line)

def run(cmd):
    global verbose
    if not verbose:
        cmd += ' 2>/dev/null'
    print_verbose('executing: %s' % cmd)
    if os.system(cmd):
        raise EApp, 'failed command: %s' % cmd

def music2png(format, infile, outfile, modified):
    '''Convert ABC notation in file infile to cropped PNG file named outfile.'''
    outfile = os.path.abspath(outfile)
    outdir = os.path.dirname(outfile)
    if not os.path.isdir(outdir):
        raise EApp, 'directory does not exist: %s' % outdir
    basefile = os.path.splitext(outfile)[0]
    abc = basefile + '.abc'
    ly = basefile + '.ly'
    temps = [ basefile + ext for ext in ('.abc', '.ly', '.ps', '.midi') ]
    # Don't delete files that already exist.
    temps = [ f for f in temps if not os.path.exists(f) ]
    skip = False
    if infile == '-':
        lines = sys.stdin.readlines()
        if format == 'abc':
            f = abc
        else:
            f = ly
        if modified:
            if f in temps:
                del temps[temps.index(f)]   # Don't delete previous source.
            if os.path.isfile(outfile) and os.path.isfile(f):
                old = open(f, 'r').readlines()
                skip = lines == old
        if not skip:
            open(f, 'w').writelines(lines)
    else:
        if not os.path.isfile(infile):
            raise EApp, 'input file does not exist: %s' % infile
        if modified and os.path.isfile(outfile):
            skip = os.path.getmtime(infile) <= os.path.getmtime(outfile)
    if skip:
        print_verbose('skipped: no change: %s' % outfile)
        return
    saved_pwd = os.getcwd()
    os.chdir(outdir)
    try:
        if format == 'abc':
            run('abc2ly --beams=None "%s"' % abc)
        run('lilypond --png "%s"' % ly)
    finally:
        os.chdir(saved_pwd)
    # Chop the bottom 75 pixels off to get rid of the page footer.
    run('convert "%s" -gravity South -crop 1000x10000+0+75 "%s"' % (outfile, outfile))
    # Trim all blank areas from sides, top and bottom.
    run('convert "%s" -trim "%s"' % (outfile, outfile))
    for f in temps:
        if os.path.isfile(f):
            print_verbose('deleting: %s' % f)
            os.remove(f)

def usage(msg=''):
    if msg:
        print_stderr(msg)
    print_stderr('\n'
                 'usage:\n'
                 '    music2png [options] INFILE\n'
                 '\n'
                 'options:\n'
                 '    -f FORMAT\n'
                 '    -o OUTFILE\n'
                 '    -m\n'
                 '    -v\n'
                 '    --help\n'
                 '    --version')

def main():
    # Process command line options.
    global verbose
    format = None
    outfile = None
    modified = False
    import getopt
    opts,args = getopt.getopt(sys.argv[1:], 'f:o:mhv', ['help','version'])
    for o,v in opts:
        if o in ('--help','-h'):
            print __doc__
            sys.exit(0)
        if o =='--version':
            print('music2png version %s' % (VERSION,))
            sys.exit(0)
        if o == '-f': format = v
        if o == '-o': outfile = v
        if o == '-m': modified = True
        if o == '-v': verbose = True
    if len(args) != 1:
        usage()
        sys.exit(1)
    infile = args[0]
    if format is None:
        usage('FORMAT must be specified')
        sys.exit(1)
    if format not in ('abc', 'ly'):
        usage('invalid FORMAT')
        sys.exit(1)
    if outfile is None:
        if infile == '-':
            usage('OUTFILE must be specified')
            sys.exit(1)
        outfile = os.path.splitext(infile)[0] + '.png'
    # Do the work.
    music2png(format, infile, outfile, modified)
    # Print something to suppress asciidoc 'no output from filter' warnings.
    if infile == '-':
        sys.stdout.write(' ')

if __name__ == "__main__":
    try:
        main()
    except SystemExit:
        raise
    except KeyboardInterrupt:
        sys.exit(1)
    except Exception, e:
        print_stderr("%s: %s" % (os.path.basename(sys.argv[0]), str(e)))
        sys.exit(1)
