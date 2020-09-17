from spacy.lang.char_classes import CONCAT_QUOTES, UNITS, ALPHA, ALPHA_LOWER, ALPHA_UPPER, group_chars
from .normalizations import N_A, N_a, N_E, N_e, N_O, N_o, N_I, N_i, N_u, N_U, N_AE, N_ae, N_OE, N_oe
import re

# these are taken from the llt tokenizer https://github.com/perseids-project/llt-tokenizer/blob/master/lib/llt/tokenizer.rb

WORDS_ENDING_WITH_QUE = [
    r"^([{u}]n.{{1,3}})?[qc][{u}][{a}{e}{i}].*que$".format(u=group_chars(N_u+N_U), a=group_chars(N_a+N_A), e=group_chars(N_e+N_E), o=group_chars(N_o+N_O), i=group_chars(N_i+N_I)),
    r"^q[{u}][{a}{o}]que$".format(u=group_chars(N_u+N_U), a=group_chars(N_a+N_A), o=group_chars(N_o+N_O)),
    r"^it[{a}]que$".format(a=group_chars(N_a + N_A)),
    r"^[{a}]tque$".format(a=group_chars(N_a + N_A)),
    r"^[{u}]t[{e}r].*que$".format(u=group_chars(N_u+N_U),e=group_chars(N_e+N_E)),
    r"^.*c[{u}]mque$".format(u=group_chars(N_u+N_U),e=group_chars(N_e+N_E)),
    r"^pl[{e}]r(.{{1,2}}|[{o}{a}]r[{u}]m)que$".format(u=group_chars(N_u+N_U), a=group_chars(N_a+N_A), o=group_chars(N_o+N_O), e=group_chars(N_E+N_e)),
    r"^d[{e}]n[{i}]que$".format(i=group_chars(N_i+N_I), e=group_chars(N_e+N_E)),
    r"^[{u}]nd[{i}]que$".format(i=group_chars(N_i+N_I), u=group_chars(N_u+N_U)),
    r"^[{u}]sque$".format(u=group_chars(N_u+N_U))
]

_regular_exp = WORDS_ENDING_WITH_QUE


TOKEN_MATCH = re.compile(
    "(?iu)" + "|".join("(?:{})".format(m) for m in _regular_exp)
).match

