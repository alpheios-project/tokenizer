import spacy
from spacy.tokens import Token
import re
import sys
from marshmallow import Schema, fields

Token.set_extension('alpheios_line_break_before',default=False)
Token.set_extension('alpheios_tbref',default=None)

class Processor():
    """ Spacy Wrapper Class """

    def __init__(self, config, **kwargs):
        """ Constructor
        :param config: the app config
        :type config: dict
        """

    def _load_model(self, lang=None):
        nlp = spacy.load("en_core_web_sm")

        # TODO max length from config
        nlp.max_length = 4000000

        return nlp

    def _add_sentencizer(self, nlp=None, lang=None):
        sentencizer = nlp.create_pipe("sentencizer")
        nlp.add_pipe(sentencizer)



    def _new_segment(self, index=0, tbSeg=False):
        return {'index':index, 'tokens':[], 'tb_sent': index if tbSeg else ''}

    def tokenize(self, text=None, lang=None, segon=None, sentencize=False, segstart=0, tbseg=False):
        nlp = self._load_model(lang)


        # TODO we should have an option to either run the regular sentencizer or to
        # interpret line breaks as sentences for segmentation
        if (sentencize):
            self._add_sentencizer(nlp=nlp)

        match_ref = re.compile(r'^TBREF_.+$')

        def set_custom_boundaries(doc):
            for token in doc[:-1]:
                if token.text == '\n':
                    doc[token.i+1]._.set('alpheios_line_break_before',True)
                if match_ref.match(token.text):
                    doc[token.i+1]._.set('alpheios_tbref',token.text)
            return doc
        nlp.add_pipe(set_custom_boundaries)

        doc = nlp(text, disable=['parser','tagger', 'ner'])
        num = len(doc)
        segNum = segstart
        tbFromSeg = tbseg
        currentSegment = self._new_segment(index=segNum,tbSeg=tbFromSeg)
        segments = [currentSegment]
        tokenIndex = 0
        for token in doc:
            if (not token.is_space) and not (match_ref.match(token.text)):
                if (segon == 'newline' and token._.alpheios_line_break_before):
                    segNum = segNum + 1
                    currentSegment = self._new_segment(index=segNum,tbSeg=tbFromSeg)
                    segments.append(currentSegment)
                    tokenIndex = 0
                returnTok = {
                  'index': tokenIndex,
                  'docIndex': token.i,
                  'text': token.text,
                  'is_punct': token.is_punct,
                  'start_sent': token.is_sent_start if sentencize and token.is_sent_start is not None else False,
                  'lb_before': token._.alpheios_line_break_before,
                  'tb_word': token._.alpheios_tbref if token._.alpheios_tbref is not None else ''
                }
                currentSegment['tokens'].append(returnTok)
                tokenIndex = tokenIndex + 1

        return segments

