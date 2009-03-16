#!/usr/bin/env python

USAGE = '''Usage: testasciidoc.py [OPTIONS] COMMAND

Run AsciiDoc conformance tests specified in configuration FILE.

Commands:
  list                          List tests
  run [NUMBER] [BACKEND]        Execute tests
  update [NUMBER] [BACKEND]     Regenerate and update test data

Options:
  -f, --conf-file=CONF_FILE
        Use configuration file CONF_FILE (default configuration file is
        testasciidoc.conf in testasciidoc.py directory)
  --force
        Update all test data overwriting existing data'''


__version__ = '0.1.0'
__copyright__ = 'Copyright (C) 2009 Stuart Rackham'


import os, sys, re, StringIO, difflib
import asciidocapi


BACKENDS = ('html4','xhtml11','docbook')
BACKEND_EXT = {'html4':'.html', 'xhtml11':'.html', 'docbook':'.xml'}


def message(msg=''):
    print >>sys.stderr, msg

def strip_end(lines):
    """
    Strip blank strings from the end of list of strings.
    """
    for i in range(len(lines)-1,-1,-1):
        if not lines[i]:
            del lines[i]
        else:
            break

def normalize_data(lines):
    """
    Strip comments and trailing blank strings from lines.
    """
    result = [ s for s in lines if not s.startswith('#') ]
    strip_end(result)
    return result


class AsciiDocTest(object):

    def __init__(self):
        self.number = None      # Test number (1..).
        self.title = ''         # Optional title.
        self.description = []   # List of lines followoing title.
        self.filename = None    # AsciiDoc test source file.
        self.options = []
        self.attributes = {}
        self.backends = BACKENDS
        self.datadir = None     # Where output files are stored.

    def backend_filename(self, backend):
        """
        Return the path name of the backend  output file that is generated from
        the AsciiDoc sourcefile.
        """
        return '%s-%s%s' % (
                os.path.normpath(
                    os.path.join(self.datadir,
                        os.path.basename(os.path.splitext(self.filename)[0]))),
                backend,
                BACKEND_EXT[backend])

    def parse(self, lines, confdir, datadir):
        """
        Parse conf file test section from list of text lines.
        """
        self.__init__()
        self.confdir = confdir
        self.datadir = datadir
        lines = Lines(lines)
        while not lines.eol():
            l = lines.read_until(r'^%')
            if l:
                if not l[0].startswith('%'):
                    self.description = l
                    self.title = l[0]
                    continue
                reo = re.match(r'^%\s*(?P<directive>[\w_-]+)', l[0])
                if not reo:
                    raise Exception
                directive = reo.groupdict()['directive']
                data = normalize_data(l[1:])
                if directive == 'asciidoc':
                    self.filename = os.path.normpath(os.path.join(
                            self.confdir, os.path.normpath(l[1])))
                elif directive == 'options':
                    self.options = eval(' '.join(data))
                    for i,v in enumerate(self.options):
                        if isinstance(v, basestring):
                            self.options[i] = (v,None)
                elif directive == 'attributes':
                    self.attributes = eval(' '.join(data))
                elif directive == 'backends':
                    self.backends = eval(' '.join(data))
                else:
                    raise (ValueError,
                           'illegal configuration directive: %s' % directive)
        if not self.title:
            self.title = self.filename

    def is_missing(self, backend):
        """
        Returns True if there is not output test data file for backend.
        """
        return not os.path.isfile(self.backend_filename(backend))

    def is_missing_or_outdated(self, backend):
        """
        Returns True if the output test data file is missing or out of date.
        """
        return self.is_missing(backend) or (
               os.path.getmtime(self.filename)
               > os.path.getmtime(self.backend_filename(backend)))

    def get_expected(self, backend):
        """
        Return expected test data output for backend.
        """
        f = open(self.backend_filename(backend))
        try:
            result = f.readlines()
            # Strip line terminators.
            result = [ s.rstrip() for s in result ]
        finally:
            f.close()
        return result

    def generate_expected(self, backend):
        """
        Generate and return test data output for backend.
        """
        asciidoc = asciidocapi.AsciiDocAPI()
        asciidoc.options.values = self.options
        asciidoc.attributes = self.attributes
        infile = self.filename
        outfile = StringIO.StringIO()
        asciidoc.execute(infile, outfile, backend)
        return outfile.getvalue().splitlines()

    def update_expected(self, backend):
        """
        Generate and write backend data.
        """
        lines = self.generate_expected(backend)
        if not os.path.isdir(self.datadir):
            message('CREATING: %s' % self.datadir)
            os.mkdir(self.datadir)
        f = open(self.backend_filename(backend),'w+')
        try:
            message('WRITING: %s' % f.name)
            f.writelines([ s + os.linesep for s in lines])
        finally:
            f.close()

    def update(self, backend=None, force=False):
        """
        Regenerate and update expected test data outputs.
        """
        if backend is None:
            backends = self.backends
        else:
            backends = [backend]
        for backend in backends:
            if force or self.is_missing_or_outdated(backend):
                self.update_expected(backend)

    def run(self, backend=None):
        """
        Execute test.
        Return True if test passes.
        """
        result = True   # Assume success.
        self.passed = self.failed = self.skipped = 0
        message('%d: %s' % (self.number, self.title))
        if os.path.isfile(self.filename):
            message(self.filename)
        else:
            message('MISSING: %s' % self.filename)
        if backend is None:
            backends = self.backends
        else:
            backends = [backend]
        for backend in backends:
            fromfile = self.backend_filename(backend)
            if not self.is_missing(backend):
                expected = self.get_expected(backend)
                strip_end(expected)
                got = self.generate_expected(backend)
                strip_end(got)
                lines = []
                for line in difflib.unified_diff(got, expected, n=0):
                    lines.append(line)
                if lines:
                    result = False
                    self.failed +=1
                    lines = lines[3:]
                    message('FAILED: %s' % backend)
                    message('+++ %s' % fromfile)
                    message('--- got')
                    for line in lines:
                        message(line)
                    message()
                else:
                    self.passed += 1
                    message('PASSED: %s' % backend)
            else:
                self.skipped += 1
                message('SKIPPED: %s' % backend)
        message()
        return result


class AsciiDocTests(object):

    def __init__(self, conffile):
        """
        Parse configuration file.
        """
        self.conffile = os.path.normpath(conffile)
        # All file names are relative to configuration file directory.
        self.confdir = os.path.dirname(self.conffile)
        self.datadir = self.confdir # Default expected files directory.
        self.tests = []             # List of parsed AsciiDocTest objects.
        self.globals = {}
        f = open(self.conffile)
        try:
            lines = Lines(f.readlines())
        finally:
            f.close()
        first = True
        while not lines.eol():
            s = lines.read_until(r'^%+$')
            if s:
                # Optional globals precede all tests.
                if first and re.match(r'^%\s*globals$',s[0]):
                    self.globals = eval(' '.join(normalize_data(s[1:])))
                    if 'datadir' in self.globals:
                        self.datadir = os.path.join(
                                self.confdir,
                                os.path.normpath(self.globals['datadir']))
                else:
                    test = AsciiDocTest()
                    test.parse(s[1:], self.confdir, self.datadir)
                    self.tests.append(test)
                    test.number = len(self.tests)
                first = False

    def run(self, number=None, backend=None):
        """
        Run all tests.
        If number is specified run test number (1..).
        """
        self.passed = self.failed = self.skipped = 0
        for test in self.tests:
            if not number or number == test.number:
                test.run(backend)
                self.passed += test.passed
                self.failed += test.failed
                self.skipped += test.skipped
        if self.passed > 0:
            message('TOTAL PASSED:  %s' % self.passed)
        if self.failed > 0:
            message('TOTAL FAILED:  %s' % self.failed)
        if self.skipped > 0:
            message('TOTAL SKIPPED: %s' % self.skipped)

    def update(self, number=None, backend=None, force=False):
        """
        Regenerate expected test data and update configuratio file.
        """
        for test in self.tests:
            if not number or number == test.number:
                test.update(backend, force=force)

    def list(self):
        """
        Lists tests to stdout.
        """
        for test in self.tests:
            print '%d: %s' % (test.number, test.title)


class Lines(list):
    """
    A list of strings.
    Adds eol() and read_until() to list type.
    """

    def __init__(self, lines):
        super(Lines, self).__init__()
        self.extend([s.rstrip() for s in lines])
        self.pos = 0

    def eol(self):
        return self.pos >= len(self)

    def read_until(self, regexp):
        """
        Return a list of lines from current position up until the next line
        matching regexp.
        Advance position to matching line.
        """
        result = []
        if not self.eol():
            result.append(self[self.pos])
            self.pos += 1
        while not self.eol():
            if re.match(regexp, self[self.pos]):
                break
            result.append(self[self.pos])
            self.pos += 1
        return result


def usage(msg=None):
    if msg:
        message(msg + '\n')
    message(USAGE)


if __name__ == '__main__':
    # Process command line options.
    import getopt
    try:
        opts,args = getopt.getopt(sys.argv[1:], 'f:', ['force'])
    except getopt.GetoptError:
        usage('illegal command options')
        sys.exit(1)
    if len(args) == 0:
        usage()
        sys.exit(1)
    conffile = os.path.join(os.path.dirname(sys.argv[0]), 'testasciidoc.conf')
    force = False
    for o,v in opts:
        if o == '--force':
            force = True
        if o in ('-f','--conf-file'):
            conffile = v
    cmd = args[0]
    number = None
    backend = None
    for arg in args[1:3]:
        try:
            number = int(arg)
        except ValueError:
            backend = arg
    tests = AsciiDocTests(conffile)
    if cmd == 'run':
        tests.run(number, backend)
        if tests.failed:
            exit(1)
    elif cmd == 'update':
        tests.update(number, backend, force=force)
    elif cmd == 'list':
        tests.list()
    else:
        usage('illegal COMMAND: %s' % cmd)
