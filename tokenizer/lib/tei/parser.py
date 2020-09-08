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

        text_xslt_path = '/' .join(('xslt','plaintext.xsl'))
        text_xslt = pkg_resources.resource_string(resource_package,text_xslt_path)
        self.text_xslt_transformer = etree.XSLT(etree.XML(text_xslt))

    def parse_meta(self, tei):
        # TODO we should try to parse the metadata from the TEI header
        meta = {
            'title': 'dummy title',
            'author': 'dummy author'
        }
        return meta

    def parse_text(self, tei):
        text = str(self.text_xslt_transformer(etree.fromstring(tei)))
        p = re.compile(r'\s+',re.DOTALL)
        text = p.sub(' ',text)
        p = re.compile(r'__ALPHEIOS_LINE_BREAK__',re.DOTALL)
        text = p.sub("\n\n",text)
        p = re.compile(r'__ALPHEIOS_SENTENCE_BREAK__',re.DOTALL)
        text = p.sub("\n",text)
        p = re.compile(r'^\s+',re.DOTALL)
        text = p.sub('',text)
        return text
