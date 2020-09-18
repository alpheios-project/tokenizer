from spacy.lang.char_classes import CONCAT_QUOTES, UNITS, ALPHA, ALPHA_LOWER, ALPHA_UPPER, group_chars
import re

TOKEN_MATCH = re.compile(
    "(?iu)" + "|".join("(?:{})".format(m) for m in [])
).match

