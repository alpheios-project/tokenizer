from spacy.lang.punctuation import TOKENIZER_PREFIXES, TOKENIZER_INFIXES, TOKENIZER_SUFFIXES
from spacy.lang.char_classes import LIST_PUNCT, LIST_ELLIPSES, LIST_QUOTES, CURRENCY, LIST_ICONS, PUNCT
from spacy.lang.char_classes import CONCAT_QUOTES, UNITS, ALPHA, ALPHA_LOWER, ALPHA_UPPER, group_chars, LATIN_LOWER
from .normalizations import N_A, N_a, N_E, N_e, N_O, N_o, N_I, N_i, N_u, N_U, N_AE, N_ae, N_OE, N_oe

#LEFT_PUNCTUATION_RE = re.compile(r'''^[{[("'\u201C\u2018<†]''')

#RIGHT_PUNCTUATION = '''\.,;:?\]\)"'\u201D\u2019\u0387\u00b7>†'''
#RIGHT_PUNCTUATION_RE = re.compile(rf"[{RIGHT_PUNCTUATION}]$")
#QUE_ENCLITIC = f"qu[{LOWER_E}]"
#QUE_ENCLITIC_RE = re.compile(rf"^{QUE_ENCLITIC}$")
#RIGHT_PUNCTUATION_WITH_ENCLYTICS_RE = re.compile(rf"[{RIGHT_PUNCTUATION}]|{QUE_ENCLITIC}$",flags=re.I)

#MIDDLE_PUNCTUATION_RE = re.compile(r'''[\u2010\u2012\u2013\u2014\u2015]''')

ENCLYTICS = [
    r"(?<=^[Nn][{e}])c".format(e=group_chars(N_e)),
    r"(?<=^[Nn][{i}])si".format(i=group_chars(N_i)),
    r"(?<=^[NnSs][{e}])[{u}]".format(e=group_chars(N_e),u=group_chars(N_u)),
    r"(?<=[{la}])que".format(la=LATIN_LOWER)
]

EXTRA_PUNC = [
  "†"
]

_suffixes = (
    LIST_PUNCT
    + EXTRA_PUNC
    + LIST_ELLIPSES
    + LIST_QUOTES
    + LIST_ICONS
    + ["'s", "'S", "’s", "’S", "—", "–"]
    + ENCLYTICS
    + [
        r"(?<=[0-9])\+",
        r"(?<=°[FfCcKk])\.",
        r"(?<=[0-9])(?:{c})".format(c=CURRENCY),
        r"(?<=[0-9])(?:{u})".format(u=UNITS),
        r"(?<=[0-9{al}{e}{p}(?:{q})])\.".format(
            al=ALPHA_LOWER, e=r"%²\-\+", q=CONCAT_QUOTES, p=PUNCT
        ),
        r"(?<=[{au}][{au}])\.".format(au=ALPHA_UPPER),
    ]
)


TOKENIZER_PREFIXES = TOKENIZER_PREFIXES + EXTRA_PUNC
TOKENIZER_SUFFIXES = _suffixes
TOKENIZER_INFIXES = TOKENIZER_INFIXES
