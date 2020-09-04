import spacy
from spacy.tokens import Token
import re

class Wrapper():
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



    def tokenize(self, lang=None, text=None, sentences=False):
        nlp = self._load_model(lang)

        Token.set_extension('alpheios_line_break_before',default=False)
        Token.set_extension('alpheios_tbref',default=None)

        # TODO we should have an option to either run the regular sentencizer or to
        # interpret line breaks as sentences for segmentation
        if (sentences):
            self._add_sentencizer

        match_ref = re.compile(r'^TBREF_.+$')

        def set_custom_boundaries(doc):
            for token in doc[:-1]:
                if token.text == "\n\n":
                    doc[token.i+1]._.set('alpheios_line_break_before',True)
                elif match_ref.match(token.text):
                    doc[token.i+1]._.set('alpheios_tbref',token.text)

                return doc
        nlp.add_pipe(set_custom_boundaries)

        doc = nlp(text, disable=['parser','tagger', 'ner'])
        num = len(doc)
        tokens = []
        for token in doc:
            if (not token.is_space) and not (match_ref.match(token.text)):
                returnTok = {
                  'index': token.i,
                  'text': token.text,
                  'sent_start': token.is_sent_start,
                  'lb_before': token._.alpheios_line_break_before,
                  'tb_ref': token._.alpheios_tbref
                }
                tokens.append(returnTok)
        return tokens

