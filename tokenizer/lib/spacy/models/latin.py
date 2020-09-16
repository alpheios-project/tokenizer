import spacy
from spacy.tokenizer import Tokenizer
from tokenizer.lib.spacy.models.base import Base
import re

class Latin(Base):

    # CONFIG
    SPLIT_ENCLYTICS = 'split_enclytics'

    SPECIAL_CASES = {
    }

    #TODO accented es
    SPECIAL_CASES_ENCLYTICS = dict(
        {
            'nec': [{"ORTH":"ne"},{"ORTH":"c"}],
            'Nec': [{"ORTH":"ne"},{"ORTH":"c"}],
            'nese': [{"ORTH":"ne"},{"ORTH":"se"}],
            'Nese': [{"ORTH":"ne"},{"ORTH":"se"}],
            'nisi': [{"ORTH":"ni"},{"ORTH":"si"}],
            'Nisi': [{"ORTH":"ni"},{"ORTH":"si"}],
        },
        **SPECIAL_CASES
    )

    LOWER_A = '''a\u00e0\u00e1\u00e2\u00e3\u00e4\u0101\u0103'''
    LOWER_E = '''e\u00e8\u00e9\u00ea\u00eb\u0113\u0115'''
    LOWER_U = '''u\u00ec\u00ed\u00ee\u00ef\u012b\u012d\u0129'''
    LOWER_I = '''i\u00f9\u00fa\u00fb\u00fc\u016b\u016d'''

    LEFT_PUNCTUATION_RE = re.compile(r'''^[{[("'\u201C\u2018<†]''')

    RIGHT_PUNCTUATION = '''\.,;:?\]\)"'\u201D\u2019\u0387\u00b7>†'''
    RIGHT_PUNCTUATION_RE = re.compile(rf"[{RIGHT_PUNCTUATION}]$")
    QUE_ENCLITIC = f"qu[{LOWER_E}]"
    QUE_ENCLITIC_RE = re.compile(rf"^{QUE_ENCLITIC}$")
    RIGHT_PUNCTUATION_WITH_ENCLYTICS_RE = re.compile(rf"[{RIGHT_PUNCTUATION}]|{QUE_ENCLITIC}$",flags=re.I)

    MIDDLE_PUNCTUATION_RE = re.compile(r'''[\u2010\u2012\u2013\u2014\u2015]''')

    # these are taken from the llt tokenizer https://github.com/perseids-project/llt-tokenizer/blob/master/lib/llt/tokenizer.rb
    ## TODO INCLUDE ACCENTS
    WORDS_ENDING_WITH_QUE_RE = re.compile(r'^((un.{1,3})?[qc]u[aei].*|qu[ao]|ita|at|ut[er].*|.*cum|pler(.{1,2}|[oa]rum)|deni|undi|us)$',flags=re.I)


    def _tokenizer(self,nlp=None,config=None):
        if Latin.SPLIT_ENCLYTICS in config:
            suffix_search = Latin.RIGHT_PUNCTUATION_WITH_ENCLYTICS_RE.search
            special_cases = Latin.SPECIAL_CASES_ENCLYTICS
        else:
            suffix_search = Latin.RIGHT_PUNCTUATION_RE.search
            special_cases = Latin.SPECIAL_CASES
        nlp.tokenizer = Tokenizer(
            nlp.vocab,
            rules=special_cases,
            prefix_search=Latin.LEFT_PUNCTUATION_RE.search,
            suffix_search = suffix_search,
            infix_finditer=Latin.MIDDLE_PUNCTUATION_RE.finditer,
            url_match=Base.URL_MATCH.match
        )

    def retokenize(self,doc=None,config=None):
        if Latin.SPLIT_ENCLYTICS in config:
            with doc.retokenize() as retokenizer:
                for token in doc:
                    if token.i != 0 and Latin.QUE_ENCLITIC_RE.match(token.text):
                        if Latin.WORDS_ENDING_WITH_QUE_RE.match(doc[token.i-1].text):
                            retokenizer.merge(doc[token.i-1:token.i+1])







