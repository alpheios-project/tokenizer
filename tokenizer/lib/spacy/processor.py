import spacy
from spacy.tokens import Token
import re
import sys
from marshmallow import Schema, fields

Token.set_extension('alpheios_segment_break_before',default=False)
Token.set_extension('alpheios_line_break_before',default=False)
Token.set_extension('alpheios_tbword',default=None)
Token.set_extension('alpheios_tbsent',default=None)

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



    def _new_segment(self, index=0, tbSeg=''):
        return {'index':index, 'tokens':[], 'tb_sent': tbSeg}

    def tokenize(self, text=None, lang=None, segon=None, sentencize=False, segstart=0, tbseg=False):
        nlp = self._load_model(lang)


        # TODO we should have an option to either run the regular sentencizer or to
        # interpret line breaks as sentences for segmentation
        if (sentencize):
            self._add_sentencizer(nlp=nlp)

        match_tbword = re.compile(r'^TBWORD_.+$')
        match_tbsent = re.compile(r'^TBSENT_.+$')
        match_lines = re.compile(r'^\n+$')

        def set_custom_boundaries(doc):
            for token in doc[:-1]:
                if match_lines.match(token.text):
                    doc[token.i+1]._.set('alpheios_line_break_before',True)
                    if token.text == '\n\n':
                        doc[token.i+1]._.set('alpheios_segment_break_before',True)
                if match_tbword.match(token.text):
                    doc[token.i+1]._.set('alpheios_tbword',token.text)
                    doc[token.i+1]._.set('alpheios_line_break_before',token._.alpheios_line_break_before)
                    doc[token.i+1]._.set('alpheios_segment_break_before',token._.alpheios_segment_break_before)
                elif match_tbsent.match(token.text):
                    doc[token.i+1]._.set('alpheios_tbsent',token.text)
                    doc[token.i+1]._.set('alpheios_line_break_before',token._.alpheios_line_break_before)
                    doc[token.i+1]._.set('alpheios_segment_break_before',token._.alpheios_segment_break_before)
                    pass
            return doc
        nlp.add_pipe(set_custom_boundaries)


        segNum = segstart

        match_seg = re.compile(r'^(TBSENT_[\S]+)')
        matched_seg = match_seg.match(text)
        if (matched_seg):
            tbStart = matched_seg.group(0)
            text = match_seg.sub('',text,1)
        elif tbseg:
            tbStart = segNum
        else:
            tbStart = ''
        doc = nlp(text, disable=['parser','tagger', 'ner'])
        currentSegment = self._new_segment(index=segNum,tbSeg=tbStart)
        segments = [currentSegment]
        tokenIndex = 0
        for token in doc:
            if (
                not token.is_space
                and not match_tbword.match(token.text)
                and not match_tbsent.match(token.text)
            ):
                if (
                    (segon == 'singleline' and token._.alpheios_line_break_before)
                    or (segon == 'doubleline' and token._.alpheios_segment_break_before)
                ):
                    segNum = segNum + 1
                    tbSeg = segNum if tbseg else token._.alpheios_tbsent
                    currentSegment = self._new_segment(index=segNum,tbSeg=tbSeg)
                    segments.append(currentSegment)
                    tokenIndex = 0
                returnTok = {
                  'index': tokenIndex,
                  'docIndex': token.i,
                  'text': token.text,
                  'is_punct': token.is_punct,
                  'start_sent': token.is_sent_start if sentencize and token.is_sent_start is not None else False,
                  'lb_before': token._.alpheios_line_break_before,
                  'tb_word': token._.alpheios_tbword if token._.alpheios_tbword is not None else ''
                }
                currentSegment['tokens'].append(returnTok)
                tokenIndex = tokenIndex + 1

        return segments

