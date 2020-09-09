import spacy
from spacy.tokens import Token
import re
import sys
from marshmallow import Schema, fields
from tokenizer.lib.meta.parser import Parser

Token.set_extension('alpheios_segment_break_before',default=False)
Token.set_extension('alpheios_line_break_before',default=False)
Token.set_extension('alpheios_data_tb_word',default=None)
Token.set_extension('alpheios_data_tb_sent',default=None)
Token.set_extension('alpheios_data_cite',default=None)
Token.set_extension('alpheios_is_meta',default=False)

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



    def _new_segment(self, index=0, metadata={}):
        segment = {'index':index, 'tokens':[] }
        if metadata:
            for item in metadata:
               key = 'data_' + item.lower()
               segment[key] = metadata[item]
        return segment

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
                if advanceBreaks:
                    toToken._.set('alpheios_line_break_before',fromToken._.alpheios_line_break_before)
                    toToken._.set('alpheios_segment_break_before',fromToken._.alpheios_segment_break_before)

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

        start_meta, text = self.metaParser.parseLine(line=text,replace=True)
        if not 'TB_SENT' in start_meta:
            start_meta['TB_SENT'] = str(segNum) if tbseg else ''
        doc = nlp(text, disable=['parser','tagger', 'ner'])
        currentSegment = self._new_segment(index=segNum,metadata=start_meta)
        segments = [currentSegment]
        tokenIndex = 0
        for token in doc:
            if ( not token.is_space and not token._.alpheios_is_meta ):
                if (
                    (segon == 'singleline' and token._.alpheios_line_break_before)
                    or (segon == 'doubleline' and token._.alpheios_segment_break_before)
                ):
                    segNum = segNum + 1
                    if tbseg:
                        tbSeg = str(segNum)
                    elif token._.alpheios_data_tb_sent is not None:
                        tbSeg = token._.alpheios_data_tb_sent
                    else:
                        tbSeg = ''
                    metadata = { 'TB_SENT': tbSeg }
                    metadata['CITE'] = token._.alpheios_data_cite
                    currentSegment = self._new_segment(index=segNum,metadata = metadata)
                    segments.append(currentSegment)
                    tokenIndex = 0
                returnTok = {
                  'index': tokenIndex,
                  'docIndex': token.i,
                  'text': token.text,
                  'is_punct': token.is_punct,
                  'start_sent': token.is_sent_start if sentencize and token.is_sent_start is not None else False,
                  'lb_before': token._.alpheios_line_break_before,
                  'data_tb_word': token._.alpheios_data_tb_word if token._.alpheios_data_tb_word is not None else ''
                }
                currentSegment['tokens'].append(returnTok)
                tokenIndex = tokenIndex + 1

        return segments

