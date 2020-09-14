import spacy
from spacy.tokens import Token
import re
import sys
from marshmallow import Schema, fields
from tokenizer.lib.meta.parser import Parser

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


for extension in EXTENSIONS:
    Token.set_extension(extension['name'],default=extension['default'])

class Processor():
    """ Spacy Wrapper Class """

    def __init__(self, config, **kwargs):
        """ Constructor
        :param config: the app config
        :type config: dict
        """
        self.metaParser = Parser()

    def _load_model(self, lang=None):
        nlp = spacy.load("en_core_web_sm")

        # TODO max length from config
        nlp.max_length = 4000000

        return nlp

    def _add_sentencizer(self, nlp=None, lang=None):
        sentencizer = nlp.create_pipe("sentencizer")
        nlp.add_pipe(sentencizer)



    def _new_segment(self, index=0, token=None, metadata=None):
        segment = {'index':index, 'tokens':[], 'metadata': {} }
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
        # if we are automatically calculating the tb sentence reference from the
        # segment number we need to add that to the segment metadata
        return re.sub("{ALPHEIOS_SEGMENT_INDEX}",str(index),template)

    def _segmentize(
        self,
        doc=None,
        sentencize=False,
        segmentOn="singleline",
        segmentStart=0,
        segmentStartMetadata={},
        segmentMetadataTemplate=""):

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
                  'punct': token.is_punct,
                  'metadata': {}
                }
                for extension in EXTENSIONS:
                    if extension['report']:
                        returnTok[extension['name']] = getattr(token._,extension['name'])
                currentSegment['tokens'].append(returnTok)
                tokenIndex = tokenIndex + 1
        return segments

    def tokenize(
        self,
        text=None,
        lang=None,
        sentencize=False,
        segmentOn=None,
        segmentStart=0,
        segmentMetadataTemplate=""):
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
            sentencize=sentencize,
            segmentOn=segmentOn,
            segmentStart=segmentStart,
            segmentStartMetadata=start_meta,
            segmentMetadataTemplate=segmentMetadataTemplate,
        )

