import spacy
from spacy.tokenizer import Tokenizer
from tokenizer.lib.spacy.models.base import BaseModel
import re

class LatinModel(BaseModel):

    SPECIAL_CASES = { }
    LEFT_PUNCTUATION = re.compile(r'''^[[("']''')
    RIGHT_PUNCTUATION = re.compile(r'''[])"']$''')
    MIDDLE_PUNCTUATION = re.compile(r'''[-~]''')

    def load_model(self):
        nlp = spacy.load(self.model())
        nlp.tokenizer.url_match = BaseModel.URL_MATCH.match
        return nlp

    def tokenizer(self,nlp):
        return Tokenizer(
            nlp.vocab,
            rules=SPECIAL_CASES,
            prefix_search=LEFT_PUNCTUATION.search,
            suffix_search=RIGHT_PUNCTUATION.search,
            infix_finditer=MIDDLE_PUNCTUATION.finditer,
            url_match=BaseModel.URL_MATCH.match
        )



