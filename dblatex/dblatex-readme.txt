AsciiDoc dblatex README
=======================

Customization
-------------
The `./dblatex` directory contains:

`./dblatex/asciidoc-dblatex.xsl`:: Optional dblatex XSL parameter
customization.

`./dblatex/asciidoc-dblatex.sty`:: Optional customized LaTeX styles.

Use these files with dblatex(1) `-p` and `-s` options, for example:

  dblatex -p ../dblatex/asciidoc-dblatex.xsl \
          -s ../dblatex/asciidoc-dblatex.sty article.xml


Limitations
-----------
- As of 'dblatex' version 0.2.8 callouts are limited to images and
  program listings and therefore aren't useful in AsciiDoc documents.
