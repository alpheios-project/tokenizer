import lxml.etree as etree
import pkg_resources
import re

class Parser():
    """ a TEI XML Parser
    """
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
        """ Parses metadata from the TEI XML Document

            :param tei: TEI XML Document
            :type tei: string

            :return: metadata
            :rtype: dict
        """
        # TODO Still needs to be implemented - we will parse the metadata
        # from the TEI header
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
        """ Parses the text from the TEI XML Document

            :param tei: TEI XML Document
            :type tei: string
            :param segmentElems: comma separated list of elements which indicate segments
            :type segmentElems: string
            :param ignoreElems: comma separated list of elements to ignore
            :type ignoreElems: string
            :param linebreakElems: comma separated list of elements which should retain linebreaks after
            :type linebreakElems: string

            :return: plain text ready for tokenization
            :rtype: string
        """
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
        """ convert the results of XSLT conversion to format expected by the tokenizer

            :param text: the text
            :type text: string

            :return: clean text as string
            :rtype: string
        """
        p = re.compile(r'\s+',re.DOTALL)
        text = p.sub(' ',text)
        p = re.compile(r'(ALPHEIOS_LINE_BREAK\s*)+',re.DOTALL)
        text = p.sub("\n",text)
        p = re.compile(r'(ALPHEIOS_SEGMENT_BREAK\s*)+',re.DOTALL)
        text = p.sub("\n\n",text)
        p = re.compile(r'^\s+',re.DOTALL)
        text = p.sub('',text)
        return text
