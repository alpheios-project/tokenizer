import spacy
from spacy.tokens import Token
import re
import sys
from marshmallow import Schema, fields
from tokenizer.lib.meta.parser import Parser

EXTENSIONS = [
    { 'name': 'alpheios_segment_break_before',
      'default': False,
      'forward': True,
      'segment_level': False,
      'source': None

    },
    { 'name': 'alpheios_line_break_before',
      'default': False,
      'forward': True,
      'segment_level': False,
      'source': None
    },
    { 'name': 'alpheios_is_meta',
      'default': False,
      'forward': False,
      'segment_level': False,
      'source': None
    }
]

for extension in Parser.METADATA_EXTENSIONS:
    EXTENSIONS.append(
        {
            'name': 'alpheios_data_' + extension['name'].lower(),
            'default': extension['default'],
            'segment_level': extension['segment_level'],
            'forward': True,
            'source': extension['name']
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
        segment = {'index':index, 'tokens':[] }
        for extension in EXTENSIONS:
            if (
                token is not None
                and getattr(token._,extension['name'])
                and extension['forward']
                and extension['segment_level']
            ):
                segment[extension['name']] = getattr(token._,extension['name'])
            if extension['source'] in metadata:
                segment[extension['name']] = metadata[extension['source']]
        return segment

    def _segment_metadata_override(self,tbseg,segNum):
        # if we are automatically calculating the tb sentence reference from the
        # segment number we need to add that to the segment metadata
        return f"META|TB_SENT_{segNum}" if tbseg else ""


    def tokenize(self, text=None, lang=None, segon=None, sentencize=False, segstart=0, tbseg=False):
        nlp = self._load_model(lang)


        # TODO we should have an option to either run the regular sentencizer or to
        # interpret line breaks as sentences for segmentation
        if (sentencize):
            self._add_sentencizer(nlp=nlp)

        match_lines = re.compile(r'^\n+$')

        def set_custom_boundaries(doc):
            def set_meta(key=None,value=None,fromToken=None,toToken=None,advanceBreaks=True):
                fromToken._.set('alpheios_is_meta',True)
                toToken._.set(key,value)
                for extension in EXTENSIONS:
                    if getattr(fromToken._,extension['name']) and extension['forward']:
                        toToken._.set(extension['name'],getattr(fromToken._,extension['name']))

            for token in doc[:-1]:
                metadata = self.metaParser.parseToken(token.text)
                if match_lines.match(token.text):
                    doc[token.i+1]._.set('alpheios_line_break_before',True)
                    if token.text == '\n\n':
                        doc[token.i+1]._.set('alpheios_segment_break_before',True)
                for item in metadata:
                    key = 'alpheios_data_' + item.lower()
                    set_meta(key=key,value=metadata[item],fromToken=token,toToken=doc[token.i+1],advanceBreaks=True)
            return doc
        nlp.add_pipe(set_custom_boundaries)


        segNum = segstart

        start_meta, text = self.metaParser.parseLine(line=text,extra=self._segment_metadata_override(tbseg,segNum),replace=True)
        doc = nlp(text, disable=['parser','tagger', 'ner'])
        currentSegment = self._new_segment(index=segNum,token=None,metadata=start_meta)
        segments = [currentSegment]
        tokenIndex = 0
        for token in doc:
            if ( not token.is_space and not token._.alpheios_is_meta ):
                if (
                    (segon == 'singleline' and token._.alpheios_line_break_before)
                    or (segon == 'doubleline' and token._.alpheios_segment_break_before)
                ):
                    segNum = segNum + 1
                    metadata, null = self.metaParser.parseLine(extra=self._segment_metadata_override(tbseg,segNum))
                    currentSegment = self._new_segment(index=segNum,token=token,metadata=metadata)
                    segments.append(currentSegment)
                    tokenIndex = 0
                returnTok = {
                  'index': tokenIndex,
                  'docIndex': token.i,
                  'text': token.text,
                  'is_punct': token.is_punct,
                  'start_sent': token.is_sent_start if sentencize and token.is_sent_start is not None else False,
                  'lb_before': token._.alpheios_line_break_before,
                  'alpheios_data_tb_word': token._.alpheios_data_tb_word
                }
                currentSegment['tokens'].append(returnTok)
                tokenIndex = tokenIndex + 1

        return segments

