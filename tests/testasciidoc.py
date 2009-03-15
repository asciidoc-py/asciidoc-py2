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
        self.options = []
        self.attributes = {}
        self.backends = BACKENDS
        self.asciidoc = None    # AsciiDoc input (list of strings or file name).
        self.inline = True  # True if asciidoc input is not in external file.
        self.header = []    # List of lines from conf file test (excludes inline outputs).
        self.expected = {}      # Expected inline outputs keyed by backend.
        self.datadir = None     # Where output files are stored.

    def backend_filename(self, backend):
        """
        Return the path name of the backend  output file that is generated from
        the AsciiDoc sourcefile.
        """
        assert not self.inline
        return '%s-%s%s' % (
                os.path.normpath(
                    os.path.join(self.datadir,
                        os.path.basename(os.path.splitext(self.asciidoc)[0]))),
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
        self.header = []
        while not lines.eol():
            l = lines.read_until(r'^%')
            if l:
                if not l[0].startswith('%'):
                    self.header += l
                    self.description = l
                    self.title = l[0]
                    continue
                reo = re.match(r'^%\s*(?P<directive>[\w_-]+)', l[0])
                if not reo:
                    raise Exception
                directive = reo.groupdict()['directive']
                data = normalize_data(l[1:])
                if directive == 'asciidoc':
                    self.header += l
                    reo = re.match(r'%\s*asciidoc(:\s*(?P<fname>.*?)\s*)?$', l[0])
                    fname = reo.groupdict()['fname']
                    if fname:
                        self.inline = False
                        self.asciidoc = os.path.normpath(os.path.join(
                                self.confdir, os.path.normpath(fname)))
                    else:
                        self.inline = True
                        self.asciidoc = data
                elif directive == 'options':
                    self.header += l
                    self.options = eval(' '.join(data))
                    for i,v in enumerate(self.options):
                        if isinstance(v, basestring):
                            self.options[i] = (v,None)
                elif directive == 'attributes':
                    self.header += l
                    self.attributes = eval(' '.join(data))
                elif directive == 'backends':
                    self.header += l
                    self.backends = eval(' '.join(data))
                elif directive in BACKENDS:
                    assert self.inline
                    self.expected[directive] = data
                else:
                    raise Exception
        if not self.title:
            if self.inline:
                self.title = self.asciidoc[0]
            else:
                self.title = self.asciidoc
        if self.inline and not self.options:
            self.options = [('--no-header-footer',None)]

    def has_expected(self, backend):
        """
        Returns True if there is output test data for backend.
        """
        if self.inline:
            return  self.expected.has_key(backend)
        else:
            return os.path.isfile(self.backend_filename(backend))

    def get_expected(self, backend):
        """
        Return expected test data output for backend.
        """
        if self.inline:
            result = self.expected.get(backend)
        else:
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
        if self.inline:
            infile = StringIO.StringIO(os.linesep.join(self.asciidoc))
        else:
            infile = self.asciidoc
        outfile = StringIO.StringIO()
        asciidoc.execute(infile, outfile, backend)
        return outfile.getvalue().splitlines()

    def update_expected(self, backend):
        """
        Generate and write backend data.
        """
        lines = self.generate_expected(backend)
        if self.inline:
            self.expected[backend] = lines
        else:
            if not os.path.isdir(self.datadir):
                message('CREATING: %s' % self.datadir)
                os.mkdir(self.datadir)
            f = open(self.backend_filename(backend),'w+')
            try:
                message('WRITING: %s' % f.name)
                f.writelines([ s + os.linesep for s in lines])
            finally:
                f.close()

    def spec(self):
        """
        Return test specification.
        """
        result = self.header
        if self.inline:
            for backend in self.expected.keys():
                result.append('%% %s' % backend)
                result.extend(self.expected[backend])
                result.append('')
        return result

    def update(self, backend=None, force=False):
        """
        Regenerate and update expected test data outputs.
        Returns list of strings containing test configuration file section.
        """
        if backend is None:
            backends = self.backends
        else:
            backends = [backend]
        for backend in backends:
            if force or not self.has_expected(backend):
                self.update_expected(backend)
        return self.spec()

    def run(self, backend=None):
        """
        Execute test.
        Return True if test passes.
        """
        result = True   # Assume success.
        self.passed = self.failed = self.skipped = 0
        message('%d: %s' % (self.number, self.title))
        if not self.inline:
            if os.path.isfile(self.asciidoc):
                message(self.asciidoc)
            else:
                message('MISSING: %s' % self.asciidoc)
        if backend is None:
            backends = self.backends
        else:
            backends = [backend]
        for backend in backends:
            if not self.inline:
                fromfile = self.backend_filename(backend)
            if self.has_expected(backend):
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
                    if self.inline:
                        message('+++ expected')
                    else:
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
        self.header = []    # %globals lines.
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
                    self.header = s
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
        result = self.header
        for test in self.tests:
            result.append('%' * 72)
            if not number or number == test.number:
                result.extend(test.update(backend, force=force))
            else:
                result.extend(test.spec())
        os.rename(self.conffile, self.conffile + '.orig')
        message('WRITING: %s' % self.conffile)
        f = open(self.conffile, 'w')
        try:
            f.write(os.linesep.join(result))
        finally:
            f.close()

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
