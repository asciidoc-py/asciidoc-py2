#!/usr/bin/env python
"""
asciidocapi - AsciiDoc API wrapper class.

The AsciiDoc class provides an API for executing asciidoc. Minimal example:

  import asciidocapi
  asciidoc = asciidocapi.AsciiDoc()
  asciidoc.execute('mydoc.txt')

See the doctests below for more examples.

AsciiDoc instance attributes
----------------------------
options: TODO
attributes: TODO
messages: TODO
cmd: TODO
asciidoc: TODO

AsciiDoc instance methods
-------------------------
execute(self, infile, outfile=None, backend=None): TODO

Asciidoc exceptions
-------------------
AsciiDocError: TODO

Doctests
--------
>>> import StringIO
>>> infile = StringIO.StringIO('Hello *{author}*')
>>> outfile = StringIO.StringIO()
>>> asciidoc = AsciiDoc()
>>> asciidoc.options.append('--no-header-footer')
>>> asciidoc.attributes['author'] = 'Joe Bloggs'
>>> asciidoc.execute(infile, outfile, backend='html4')
>>> print outfile.getvalue()
<p>Hello <strong>Joe Bloggs</strong></p>

>>>

Copyright (C) 2009 Stuart Rackham. Free use of this software is granted
under the terms of the GNU General Public License (GPL).

"""

API_VERSION = '0.1.0'
MIN_ASCIIDOC_VERSION = '8.3.6'  # Minimum acceptable AsciiDoc version.

import sys,os,re


def find_in_path(fname, path=None):
    """
    Find file fname in shell PATH. Return None if not found.
    """
    if path is None:
        path = os.environ.get('PATH', '')
    for dir in path.split(os.pathsep):
        fpath = os.path.join(dir, fname)
        if os.path.exists(fpath):
            return fpath
    else:
        return None


class AsciiDocError(Exception):
    pass


class Options(object):
    """
    List of (key,value) command option tuples.

    The following examples append ('--verbose',None) and
    ('--conf-file','blog.conf') to the options.values list (you can
    optionally omit append):

    options.append('--verbose')
    options.append('--conf-file', 'blog.conf')
    """
    def __init__(self, values=[]):
        self.values = values[:]
    def append(self, name, value=None):
        self.values.append((name,value))
    def __call__(self, name, value=None):
        """Shortcut for append()."""
        self.values.append((name,value))


class Version(object):
    """
    Compare AsciiDoc version numbers. Example:

    >>> Version('8.2.5') < Version('8.3')
    True

    string: String version number '<major>.<minor>[.<micro>]'.
    major: Integer major version number.
    minor: Integer minor version number.
    micro: Integer micro version number.
    """
    def __init__(self, version):
        self.string = version
        reo = re.match(r'^(\d+)\.(\d+)(\.(\d+))?.*$', self.string)
        if not reo:
            raise AsciiDocError('invalid version number: %s' % self.string)
        groups = reo.groups()
        self.major = int(groups[0])
        self.minor = int(groups[1])
        self.micro = int(groups[3] or '0')
    def __cmp__(self, other):
        return cmp(self.major*10000 + self.minor*100 + self.micro,
                   other.major*10000 + other.minor*100 + other.micro)

class AsciiDoc(object):
    """
    The following options are invalid in API context: help,  version.
    """
    def __init__(self, asciidoc_py=None):
        self.options = Options()
        self.attributes = {}
        self.messages = []
        # Search for the asciidoc command file.
        # Try ASCIIDOC_PY environment variable first.
        cmd = os.environ.get('ASCIIDOC_PY')
        if cmd:
            if not os.path.exists(cmd):
                raise AsciiDocError('missing ASCIIDOC_PY file: %s' % cmd)
        elif asciidoc_py:
            # Next try path specified by caller.
            cmd = asciidoc_py
            if not os.path.exists(cmd):
                raise AsciiDocError('missing file: %s' % cmd)
        else:
            # Try shell search paths.
            for fname in ['asciidoc', 'asciidoc.py', 'asciidoc.pyc']:
                cmd = find_in_path(fname)
                if cmd: break
            else:
                # Finally try current working directory.
                cmd = 'asciidoc.py'
                if not os.path.exists(cmd):
                    raise AsciiDocError('failed to locate asciidoc')
        cmd = os.path.realpath(cmd)
        sys.path.insert(0, os.path.dirname(cmd))
        try:
            try:
                import asciidoc
            except ImportError:
                raise AsciiDocError('failed to import asciidoc')
        finally:
            del sys.path[0]
        if Version(asciidoc.VERSION) < Version(MIN_ASCIIDOC_VERSION):
            raise AsciiDocError('requires asciidoc version %s or better'
                                % MIN_ASCIIDOC_VERSION)
        self.asciidoc = asciidoc
        self.cmd = cmd

    def execute(self, infile, outfile=None, backend=None):
        self.messages = []
        opts = Options(self.options.values)
        if outfile is not None:
            opts('--out-file', outfile)
        if backend is not None:
            opts('--backend', backend)
        for k,v in self.attributes.items():
            if v == '' or k[-1] in '!@':
                s = k
            else:
                s = '%s=%s' % (k,v)
            opts('--attribute', s)
        args = [infile]
        sys.path.insert(0, os.path.dirname(self.cmd))
        try:
            reload(self.asciidoc)   # Reinitialize globals and class attributes.
        finally:
            del sys.path[0]
        try:
            try:
                self.asciidoc.execute(self.cmd, opts.values, args)
            finally:
                self.messages = self.asciidoc.messages[:]
        except SystemExit, e:
            if e.code:
                raise AsciiDocError(self.messages[-1])

if __name__ == "__main__":
    import doctest
    options = doctest.ELLIPSIS
    doctest.testmod(optionflags=options)
