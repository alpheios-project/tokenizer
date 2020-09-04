import lxml.etree as etree
import pkg_resources
import re

class Parser():

    def __init__(self, config, **kwargs):
        """ Constructor
        :param config: the app config
        :type config: dict
        """
        resource_package = __name__
        xslt_path = '/' .join(('xslt','plaintext.xsl'))
        xslt = pkg_resources.resource_string(resource_package,xslt_path)
        self.xslt_transformer = etree.XSLT(etree.XML(xslt))

    def parse(self, tei=None):
        text = str(self.xslt_transformer(etree.fromstring(tei)))
        p = re.compile(r'\s+',re.DOTALL)
        text = p.sub(' ',text)
        p = re.compile(r'__ALPHEIOS_LINE_BREAK__',re.DOTALL)
        text = p.sub("\n\n",text)
        p = re.compile(r'__ALPHEIOS_SENTENCE_BREAK__',re.DOTALL)
        text = p.sub("\n",text)
        p = re.compile(r'^\s+',re.DOTALL)
        text = p.sub('',text)
        return text
