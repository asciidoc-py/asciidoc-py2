<!--
  Generates EPUB XHTML documents from DocBook XML source using DocBook XSL
  stylesheets.

  NOTE: The URL reference to the current DocBook XSL stylesheets is
  rewritten to point to the copy on the local disk drive by the XML catalog
  rewrite directives so it doesn't need to go out to the Internet for the
  stylesheets. This means you don't need to edit the <xsl:import> elements on
  a machine by machine basis.
-->
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform" version="1.0">
  <xsl:import href="http://docbook.sourceforge.net/release/xsl/current/epub/docbook.xsl"/>
<xsl:import href="common.xsl"/>

<!-- Separate the first chapter from preceding content. -->
<xsl:param name="chunk.first.sections" select="1"/>

<!-- Chunk on a chapter by chapter basis (no sub-section chunks. -->
<xsl:param name="chunk.section.depth" select="0"/>

<!--
DocBook XSL 1.75.2: Nav headers are invalid XHTML (table width element)
-->
<xsl:param name="suppress.navigation" select="1"/>

<!--
DocBook XSL 1.75.2 doesn't handle admonition icons
-->
<xsl:param name="admon.graphics" select="0"/>

<!--
DocBook XLS 1.75.2 doesn't handle TOCs
-->
<xsl:param name="generate.toc">
  <xsl:choose>
    <xsl:when test="/article">
/article  nop
    </xsl:when>
    <xsl:when test="/book">
/book  nop
    </xsl:when>
  </xsl:choose>
</xsl:param>

</xsl:stylesheet>
