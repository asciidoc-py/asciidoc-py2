<?xml version="1.0" encoding="iso-8859-1"?>
<!--
dblatex(1) XSL user stylesheet for asciidoc(1).
See dblatex(1) -p option.
-->
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform" version="1.0">

  <!-- TOC links in the titles, and in blue. -->
  <xsl:param name="latex.hyperparam">colorlinks,linkcolor=blue,pdfstartview=FitH</xsl:param>
  <xsl:param name="doc.publisher.show">1</xsl:param>
  <xsl:param name="doc.lot.show"></xsl:param>
  <xsl:param name="term.breakline">1</xsl:param>
  <xsl:param name="doc.collab.show">0</xsl:param>
  <xsl:param name="doc.section.depth">3</xsl:param>
  <xsl:param name="table.in.float">0</xsl:param>
  <xsl:param name="monoseq.hyphenation">0</xsl:param>

  <!--
    TODO: Does not work on  multiple verses (blank lines are
          replaced by a single space.

    Override dblatex address and literallayout processing.
    dblatex (as of version 0.2.8) doesn't seem to process the
    DocBook <literallayout> element correctly: it is rendered in
    a monospaced font and no nested elements are processed. By
    default the normal font should be used and almost all
    DocBook inline elements should be processed.
    See http://www.docbook.org/tdg/en/html/literallayout.html
  -->
  <xsl:template match="address|literallayout[@class!='monospaced']">
    <xsl:text>\begin{alltt}</xsl:text>
    <xsl:text>&#10;\normalfont{}&#10;</xsl:text>
    <xsl:apply-templates/>
  <!--
    <xsl:apply-templates mode="latex.verbatim"/>
  -->
    <xsl:text>&#10;\end{alltt}</xsl:text>
  </xsl:template>

</xsl:stylesheet>

