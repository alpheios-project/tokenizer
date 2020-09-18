from spacy.lang.punctuation import TOKENIZER_PREFIXES, TOKENIZER_INFIXES, TOKENIZER_SUFFIXES
from spacy.lang.char_classes import LIST_PUNCT, LIST_ELLIPSES, LIST_QUOTES, CURRENCY, LIST_ICONS, PUNCT
from spacy.lang.char_classes import CONCAT_QUOTES, UNITS, ALPHA, ALPHA_LOWER, ALPHA_UPPER, group_chars

from .char_classes import CONSONANTS, PLAIN_VOWELS, VOWELS_WITH_SPIRITUS, ALL


EXTRA_PUNC = [
    "†"
]

DASHES = [
    "—",
    "–"
]

# KRASIS and ELISION taken from https://github.com/perseids-project/llt-tokenizer/blob/master/lib/llt/tokenizer/greek.rb
KRASIS = [
    r"^([{C}])(?=[{PV}]?[{VS}][{A}])".format(
        C=group_chars(CONSONANTS),
        PV=group_chars(PLAIN_VOWELS),
        VS=group_chars(VOWELS_WITH_SPIRITUS),
        A=group_chars(ALL)
    )
]
ELISION = [ r"^([{C}][᾽'])(?=[{a}])".format(a=group_chars(ALL), C=group_chars(CONSONANTS)) ]

_prefixes = TOKENIZER_PREFIXES + ELISION + KRASIS + EXTRA_PUNC


# this is the same as the spacy defaults except where noted
_suffixes = (
    LIST_PUNCT
    + EXTRA_PUNC # added the extra punctuation (dagger)
    + LIST_ELLIPSES
    + LIST_QUOTES
    + LIST_ICONS
    + DASHES # removed apostrophe s
    + [
        r"(?<=[0-9])\+",
        r"(?<=°[FfCcKk])\.",
        r"(?<=[0-9])(?:{c})".format(c=CURRENCY),
        r"(?<=[0-9])(?:{u})".format(u=UNITS),
        r"(?<=[0-9{al}{e}{p}(?:{q})])\.".format(
            al=ALPHA_LOWER, e=r"%²\-\+", q=CONCAT_QUOTES, p=PUNCT
        ),
        r"(?<=[{au}][{au}])\.".format(au=ALPHA),
    ]
)


TOKENIZER_PREFIXES = _prefixes
TOKENIZER_SUFFIXES = _suffixes
TOKENIZER_INFIXES = TOKENIZER_INFIXES
