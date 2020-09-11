import lxml.etree as etree
import pkg_resources
import re

class Parser():
    DEFAULT_SEGMENT_ELEMS = "body"
    DEFAULT_IGNORE_ELEMS = "label,ref,milestone,orig,abbr,head,title,teiHeader,del,g,bibl,front,back,speaker"
    DEFAULT_LINEBREAK_ELEMS = "p,div,seg,l,ab"

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

    def parse_text(self, tei=None,
        segmentElems=DEFAULT_SEGMENT_ELEMS,
        segmentAtts="",
        ignoreElems=DEFAULT_IGNORE_ELEMS,
        linebreakElems=DEFAULT_LINEBREAK_ELEMS
    ):
        segmentList = "".join(map(lambda i: f" {i} ",segmentElems.split(",")))
        ignoreList = "".join(map(lambda i: f" {i} ",ignoreElems.split(",")))
        linebreakList = "".join(map(lambda i: f" {i} ",linebreakElems.split(",")))
        segmentOn = etree.XSLT.strparam(segmentList)
        ignore = etree.XSLT.strparam(ignoreList)
        linebreakOn = etree.XSLT.strparam(linebreakList)
        text = self.text_xslt_transformer(etree.fromstring(tei),
            e_segmentOn = segmentOn,
            e_linebreakOn = linebreakOn,
            e_ignore = ignore,
        )
        return self.clean_text(str(text))

    def clean_text(self,text):
        p = re.compile(r'\s+',re.DOTALL)
        text = p.sub(' ',text)
        p = re.compile(r'(ALPHEIOS_LINE_BREAK\s*)+',re.DOTALL)
        text = p.sub("\n",text)
        p = re.compile(r'(ALPHEIOS_SEGMENT_BREAK\s*)+',re.DOTALL)
        text = p.sub("\n\n",text)
        p = re.compile(r'^\s+',re.DOTALL)
        text = p.sub('',text)
        return text
