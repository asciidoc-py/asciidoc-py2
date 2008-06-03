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
</xsl:stylesheet>

