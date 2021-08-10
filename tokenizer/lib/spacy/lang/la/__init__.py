# coding: utf8
from __future__ import unicode_literals

from .punctuation import TOKENIZER_SUFFIXES, TOKENIZER_INFIXES, TOKENIZER_PREFIXES
from .tokenizer_exceptions import TOKEN_MATCH

from spacy.lang.lex_attrs import LEX_ATTRS

from spacy.lang.tokenizer_exceptions import BASE_EXCEPTIONS, URL_MATCH
from spacy.lang.norm_exceptions import BASE_NORMS
from spacy.language import Language
from spacy.lookups import Lookups
from spacy.attrs import LANG, NORM
from spacy.util import update_exc, add_lookups


class LatinDefaults(Language.Defaults):
    lex_attr_getters = dict(Language.Defaults.lex_attr_getters)
    lex_attr_getters.update(LEX_ATTRS)
    lex_attr_getters[LANG] = lambda text: "la"

    tokenizer_exceptions = BASE_EXCEPTIONS
    prefixes = TOKENIZER_PREFIXES
    infixes = TOKENIZER_INFIXES
    suffixes = TOKENIZER_SUFFIXES
    token_match = TOKEN_MATCH
    syntax_iterators = {}


class Latin(Language):
    lang = "la"
    Defaults = LatinDefaults


__all__ = ["Latin"]