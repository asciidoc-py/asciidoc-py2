#!/bin/sh
#
# AsciiDoc canonical installer/uninstaller.
# Definative packager's guide.
# Documented in INSTALL file.
#
# NOTE: If you change the CONFDIR (the global asciidoc(1) configuration file
# directory) then you will also need to change the CONF_DIR constant definition
# values in both a2x and asciiidoc.py scripts.

CONFDIR=/etc/asciidoc
BINDIR=/usr/local/bin
MANDIR=/usr/local/man
VIM_CONFDIR=/etc/vim

if [ `basename $0` = uninstall.sh ]; then
    rm $BINDIR/asciidoc
    rm $BINDIR/a2x
    rm $MANDIR/man1/asciidoc.1
    rm $MANDIR/man1/a2x.1
    rm -rf $CONFDIR
    rm -f $VIM_CONFDIR/syntax/asciidoc.vim
    rm -f $VIM_CONFDIR/ftdetect/asciidoc_filetype.vim
else
    install asciidoc.py $BINDIR/asciidoc
    install a2x $BINDIR/a2x
    install -d $MANDIR/man1
    install doc/*.1 $MANDIR/man1
    install -d $CONFDIR/filters \
               $CONFDIR/docbook-xsl \
               $CONFDIR/stylesheets \
               $CONFDIR/javascripts \
               $CONFDIR/images/icons/callouts
    install -m 644 *.conf $CONFDIR
    install filters/*.py $CONFDIR/filters
    install -m 644 filters/*.conf $CONFDIR/filters
    install -m 644 docbook-xsl/*.xsl $CONFDIR/docbook-xsl
    install -m 644 stylesheets/*.css $CONFDIR/stylesheets
    install -m 644 javascripts/*.js $CONFDIR/javascripts
    install -m 644 images/icons/callouts/* $CONFDIR/images/icons/callouts
    install -m 644 images/icons/README images/icons/*.png $CONFDIR/images/icons
    if [ -d $VIM_CONFDIR ]; then
        install -d $VIM_CONFDIR/syntax
        install -m 644 vim/syntax/asciidoc.vim \
                       $VIM_CONFDIR/syntax/asciidoc.vim
        install -d $VIM_CONFDIR/ftdetect
        install -m 644 vim/ftdetect/asciidoc_filetype.vim \
                       $VIM_CONFDIR/ftdetect/asciidoc_filetype.vim
    fi
fi

# vim: set et ts=4 sw=4 sts=4:
