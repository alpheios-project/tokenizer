<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
    xmlns:dts="https://w3id.org/dts/api#"
    xmlns:xs="http://www.w3.org/2001/XMLSchema"
    exclude-result-prefixes="xs" xmlns:tei="http://www.tei-c.org/ns/1.0"
    version="1.0">
    <xsl:output method="text" encoding="UTF-8"/>
    <xsl:param name="e_segmentOn" select="' body '"></xsl:param>
    <xsl:param name="e_linebreakOn" select="' p div seg l ab '"/>
    <xsl:param name="e_ignore" select="' label ref milestone orig abbr head title teiHeader del g bibl front back foreign speaker '"/>

    <xsl:template match="/">
      <xsl:choose>
          <xsl:when test="//dts:fragment">
              <xsl:apply-templates select="//dts:fragment"/>
          </xsl:when>
          <xsl:when test="//tei:text">
               <xsl:apply-templates select="//tei:text"></xsl:apply-templates>
          </xsl:when>
          <xsl:otherwise>
              <xsl:apply-templates select="//text"></xsl:apply-templates>
          </xsl:otherwise>
      </xsl:choose>
       
    </xsl:template>

    <xsl:template match="tei:w|w">
        <xsl:text> </xsl:text><xsl:apply-templates />
    </xsl:template>

    <xsl:template match="*">
        <xsl:choose>
          <xsl:when test="contains($e_segmentOn, concat(' ', local-name(.), ' '))">
              <xsl:apply-templates></xsl:apply-templates>
              <xsl:text>ALPHEIOS_SEGMENT_BREAK</xsl:text>
          </xsl:when>
          <xsl:when test="contains($e_linebreakOn,concat(' ',local-name(.),' '))">
              <xsl:text>ALPHEIOS_LINE_BREAK</xsl:text>
              <xsl:apply-templates />
          </xsl:when>
          <xsl:when test="contains($e_ignore, concat(' ', local-name(.), ' '))">
              <xsl:text> </xsl:text>
          </xsl:when>
          <xsl:otherwise>
              <xsl:apply-templates />
          </xsl:otherwise>
        </xsl:choose>
    </xsl:template>
</xsl:stylesheet>
