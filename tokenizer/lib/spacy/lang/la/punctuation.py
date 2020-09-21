from spacy.lang.punctuation import TOKENIZER_PREFIXES, TOKENIZER_INFIXES, TOKENIZER_SUFFIXES
from spacy.lang.char_classes import LIST_PUNCT, LIST_ELLIPSES, LIST_QUOTES, CURRENCY, LIST_ICONS, PUNCT
from spacy.lang.char_classes import CONCAT_QUOTES, UNITS, ALPHA, ALPHA_LOWER, ALPHA_UPPER, group_chars, LATIN_LOWER
from .normalizations import N_A, N_a, N_E, N_e, N_O, N_o, N_I, N_i, N_u, N_U, N_AE, N_ae, N_OE, N_oe


ENCLYTICS = [
    r"(?<=^[Nn][{e}])c".format(e=group_chars(N_e)),
    r"(?<=^[Nn][{i}])si".format(i=group_chars(N_i)),
    r"(?<=^[NnSs][{e}])[{u}]".format(e=group_chars(N_e),u=group_chars(N_u)),
    r"(?<=[{la}])que".format(la=LATIN_LOWER)
]

EXTRA_PUNC = [
    "†"
]

DASHES = [
    "—",
    "–"
]

# this is the same as the spacy defaults except where noted
_suffixes = (
    LIST_PUNCT
    + EXTRA_PUNC # added the extra punctuation (dagger)
    + LIST_ELLIPSES
    + LIST_QUOTES
    + LIST_ICONS
    + DASHES # removed apostrophe s
    + ENCLYTICS # added enclytics
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
