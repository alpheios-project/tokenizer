from spacy.lang.punctuation import TOKENIZER_PREFIXES, TOKENIZER_INFIXES, TOKENIZER_SUFFIXES
from spacy.lang.char_classes import LIST_PUNCT, LIST_ELLIPSES, LIST_QUOTES, CURRENCY
from spacy.lang.char_classes import CONCAT_QUOTES, UNITS, ALPHA, ALPHA_LOWER, ALPHA_UPPER, group_chars, LATIN_LOWER
from .normalizations import N_A, N_a, N_E, N_e, N_O, N_o, N_I, N_i, N_u, N_U, N_AE, N_ae, N_OE, N_oe

#LEFT_PUNCTUATION_RE = re.compile(r'''^[{[("'\u201C\u2018<†]''')

#RIGHT_PUNCTUATION = '''\.,;:?\]\)"'\u201D\u2019\u0387\u00b7>†'''
#RIGHT_PUNCTUATION_RE = re.compile(rf"[{RIGHT_PUNCTUATION}]$")
#QUE_ENCLITIC = f"qu[{LOWER_E}]"
#QUE_ENCLITIC_RE = re.compile(rf"^{QUE_ENCLITIC}$")
#RIGHT_PUNCTUATION_WITH_ENCLYTICS_RE = re.compile(rf"[{RIGHT_PUNCTUATION}]|{QUE_ENCLITIC}$",flags=re.I)

#MIDDLE_PUNCTUATION_RE = re.compile(r'''[\u2010\u2012\u2013\u2014\u2015]''')


_suffixes = TOKENIZER_SUFFIXES + [
    r"(?<=[Nn][{E}{e}])c".format(E=group_chars(N_E),e=group_chars(N_e)),
    r"(?<=[Nn][{E}{e}])se".format(E=group_chars(N_E),e=group_chars(N_e)),
    r"(?<=[Nn][{I}{i}])si".format(I=group_chars(N_I),i=group_chars(N_i)),
    r"(?i)(?<=[{la}])que".format(la=LATIN_LOWER)
]

TOKENIZER_SUFFIXES = _suffixes
