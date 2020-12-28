import spacy
from spacy.tokens import Token
import re
import sys
from marshmallow import Schema, fields
from tokenizer.lib.meta.parser import Parser
from tokenizer.lib.spacy.models.default import Default

# extensions to the Spacy Token API for processing segment and line information
EXTENSIONS = [
    { 'name': 'segment_break_before',
      'default': False,
      'forward': True,
      'source': None,
      'report': False

    },
    { 'name': 'line_break_before',
      'default': False,
      'forward': True,
      'source': None,
      'report': True,
    },
    { 'name': 'is_meta',
      'default': False,
      'forward': False,
      'source': None,
      'report': False
    }
]

# extensions to the Spacy Token API for Alpheios Metadata
for field in Parser.METADATA_FIELDS:
    EXTENSIONS.append(
        {
            'name': Parser.metadata_field_name(field['name']),
            'default': field['default'],
            'forward': True,
            'source': field['name'],
            'report': True,
        }
    )

# adds the Token extensions to the Spacy processor
for extension in EXTENSIONS:
    Token.set_extension(extension['name'],default=extension['default'])

class Processor():
    """ Wraps the Spacy Tokenizer to process text into segments and tokens """

    def __init__(self,config={}):
        """ Constructor

        :param config: app level configuration
        :type config: dict
        """
        self.metaParser = Parser()
        self.model = Default()

    def _load_model(self, lang=None):
        """ private method to load the correct tokenizer model for the language
            of the text.

            :param lang: the language of the text
            :type lang: string
        """

        nlp = self.model.load_model(lang=lang,config={})

        # TODO we should get the max length from the app configuration
        # need to find out if this can be unlimited
        nlp.max_length = 4000000

        return nlp

    def _custom_tokenizer(self,nlp=None,lang=None):
         return Tokenizer(
            nlp.vocab,
            rules=self.rules.special_cases(lang),
            prefix_search=self.rules.prefix(lang),
            suffix_search=self.rules.suffix(lang),
            infix_finditer=self.rules.infix(lang),
            url_match=self.rules.url_match(lang)
        )

    def _add_sentencizer(self, nlp=None, lang=None):
        """ private method to add a sentencizer to the pipeline

            :param nlp: the spacy pipeline object
            :type nlp: pipeline:
            :param lang: the language of the text
            :type lang: string
        """
        sentencizer = nlp.create_pipe("sentencizer")
        nlp.add_pipe(sentencizer)

    def _new_segment(self, index=0, token=None, metadata=None):
        """ private method to create a new segment container

            :param index: index of the segment
            :type index: int
            :param token: token which creates the segment break
            :type token: Token
            :param metadata: additional segment level metadata
            :type metadata: dict

            :return: the segment object
            :rtype: dict
        """
        segment = {'index':index, 'tokens':[] }
        for extension in EXTENSIONS:
            if (
                token is not None
                and getattr(token._,extension['name'])
                and extension['forward']
            ):
                segment[extension['name']] = getattr(token._,extension['name'])
            if extension['source'] in metadata:
                segment[extension['name']] = metadata[extension['source']]
        return segment

    def _insert_metadata(self,template="",index=None):
        """ private method to insert metadata into text to be tokenized

            :param template: the template for the metadata
            :type template: string
            :param index: the index number to replace in the template
            :type index: int

            :return: the updated text
            :rtype: string
        """
        return re.sub("{ALPHEIOS_SEGMENT_INDEX}",str(index),template)

    def _segmentize(
        self,
        doc=None,
        segmentOn="singleline",
        segmentStart=0,
        segmentStartMetadata={},
        segmentMetadataTemplate=""):
        """ private method to apply segmentation to the results of the spacy tokenization

            :param doc: the from the tokenizer
            :type doc: Document
            :param segmentOn: what indicates a segment (singleline or doubleline)
            :type segmentOn: string
            :param segmentStart: starting index for the segments
            :type segmentStart: int
            :param segmentStartMetadata: metadata to add to the first segment
            :type segmentStartMetadata: dict
            :param segmentMetadataTemplate: a template to use for segment metadata to be added to the text
            :type segmentMetadataTemplate: string

            :return: list of segments containing tokens
            :rtype: dict[]
        """

        # create the first segment
        currentSegment = self._new_segment(
            index=segmentStart,
            token=None,
            metadata=segmentStartMetadata
        )
        segments = [currentSegment]
        tokenIndex = 0
        segmentIndex=segmentStart
        for token in doc:
            if ( not token.is_space and not token._.is_meta ):
                if (
                    (segmentOn == 'singleline' and token._.line_break_before)
                    or (segmentOn == 'doubleline' and token._.segment_break_before)
                ):
                    segmentIndex = segmentIndex + 1
                    segmeta, null = self.metaParser.parseLine(
                        extra=self._insert_metadata(template=segmentMetadataTemplate,index=segmentIndex)
                    )
                    currentSegment = self._new_segment(
                        index=segmentIndex,
                        token=token,
                        metadata=segmeta
                    )
                    segments.append(currentSegment)

                    # reset the token index
                    tokenIndex = 0

                returnTok = {
                  'index': tokenIndex,
                  'docIndex': token.i,
                  'text': token.text,
                  'punct': token.is_punct
                }
                for extension in EXTENSIONS:
                    if extension['report']:
                        returnTok[extension['name']] = getattr(token._,extension['name'])
                currentSegment['tokens'].append(returnTok)
                tokenIndex = tokenIndex + 1
        return segments

    def _normalize(self,text=None):
        """ normalize text prior to tokenization
            :param text: the text to be tokenized
            :type text string

            :return: normalized text
            :rtype: string
        """
        # normalize linebreaks to \n
        text = text.replace('\r\n', '\n').replace('\r', '\n')
        p = re.compile(r'\n\n\n+',re.DOTALL)
        text = p.sub('\n\n',text)
        return text

    def tokenize(
        self,
        text=None,
        lang=None,
        sentencize=False,
        segmentOn=None,
        segmentStart=0,
        segmentMetadataTemplate=""):
        """ tokenize text

            :param text: the text to be tokenized
            :type text string
            :param lang: the language of the text
            :type text: string
            :param sentencize: whether or not to apply a sentencizing algorithm (not currently used)
            :type sentencize: boolean
            :param segmentOn: separator which indicates a new segment ("singleline" or "doubleline")
            :type segmentOn: string
            :param segmentStart: index for starting segment
            :type segmentStart: int
            :param segmentMetadataTemplate: a template for segment metadata to be added to the text
            :type segmentMetadata: string

            :return: results of tokenization and segmentation
            :rtype: list of segments, each containint a list of tokens
        """
        text = self._normalize(text=text)
        nlp = self._load_model(lang)
        if (sentencize):
            self._add_sentencizer(nlp=nlp)

        match_lines = re.compile(r'^\n+$')

        def set_custom_boundaries(doc):
            def set_meta(key=None,value=None,fromToken=None,toToken=None):
                fromToken._.set('is_meta',True)
                toToken._.set(key,value)
                for extension in EXTENSIONS:
                    if getattr(fromToken._,extension['name']) and extension['forward']:
                        toToken._.set(extension['name'],getattr(fromToken._,extension['name']))

            for token in doc[:-1]:
                metadata = self.metaParser.parseToken(token.text)
                if match_lines.match(token.text):
                    doc[token.i+1]._.set('line_break_before',True)
                    if token.text == '\n\n':
                        doc[token.i+1]._.set('segment_break_before',True)
                for item in metadata:
                    key = Parser.metadata_field_name(item)
                    set_meta(key=key,value=metadata[item],fromToken=token,toToken=doc[token.i+1])
            return doc

        nlp.add_pipe(set_custom_boundaries)
        start_meta, text = self.metaParser.parseLine(
            line=text,
            extra=self._insert_metadata(template=segmentMetadataTemplate,index=segmentStart),
            replace=True
        )
        doc = nlp(text, disable=['parser','tagger', 'ner'])
        return self._segmentize(
            doc=doc,
            segmentOn=segmentOn,
            segmentStart=segmentStart,
            segmentStartMetadata=start_meta,
            segmentMetadataTemplate=segmentMetadataTemplate,
        )

