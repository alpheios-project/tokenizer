import spacy
from spacy.tokenizer import Tokenizer
from tokenizer.lib.spacy.models.base import Base
import re

class Latin(Base):

    SPLIT_ENCLYTICS = 'split_enclytics'

    #WORDS_ENDING_WITH_QUE = re.compile(r'^((un.{1,3})?[qc]u[aei].*que|qu[ao]que|itaque|atque|ut[er].*que|.*cumque|pler(.{1,2}|[oa]rum)que|denique|undique|usque)$',flags=re.I)
    #WORDS_ENDING_WITH_NE  = re.compile(r'omne|sine|bene|paene|iuvene|siccine)$',flags=re.I)

    SPECIAL_CASES = { }

    LEFT_PUNCTUATION_RE = re.compile(r'''^[{[("'\u201C\u2018<†]''')

    RIGHT_PUNCTUATION = '''\.,;:?\]\)"'\u201D\u2019\u0387\u00b7>†'''
    RIGHT_PUNCTUATION_RE = re.compile(rf"[{RIGHT_PUNCTUATION}]$")
    RIGHT_PUNCTUATION_WITH_ENCLYTICS_RE = re.compile(rf"[{RIGHT_PUNCTUATION}]|que$")

    MIDDLE_PUNCTUATION_RE = re.compile(r'''[\u2010\u2012\u2013\u2014\u2015]''')

    def _tokenizer(self,nlp=None,config=None):
        if Latin.SPLIT_ENCLYTICS in config:
            suffix_search = Latin.RIGHT_PUNCTUATION_WITH_ENCLYTICS_RE.search
        else:
            suffix_search = Latin.RIGHT_PUNCTUATION_RE.search
        nlp.tokenizer = Tokenizer(
            nlp.vocab,
            rules=Latin.SPECIAL_CASES,
            prefix_search=Latin.LEFT_PUNCTUATION_RE.search,
            suffix_search = suffix_search,
            infix_finditer=Latin.MIDDLE_PUNCTUATION_RE.finditer,
            url_match=Base.URL_MATCH.match
        )

    def retokenize(self,doc=doc):
        with doc.retokenize() as retokenizer:
            for token in doc:
                if token.i != 0:
                    p_q = re.compile(r'que$')
                    p_prefix == re.compile(r'^((un.{1,3})?[qc]u[aei].*|qu[ao]|ita|at|ut[er].*|.*cumq|pler(.{1,2}|[oa]rum)|deni|undi|us)$',flags=re.I)
                    q_match = p_q.match(token.text)
                    p_patch = p_prefix.match(doc[token.i-1].text)
                    if q_match and ! p_match:
                        retokenizer.merge(doc[token.i-1:token.i+1])







