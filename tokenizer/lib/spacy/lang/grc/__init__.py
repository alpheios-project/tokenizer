# coding: utf8
from __future__ import unicode_literals

from .punctuation import TOKENIZER_SUFFIXES, TOKENIZER_INFIXES, TOKENIZER_PREFIXES

from spacy.lang.lex_attrs import LEX_ATTRS

from spacy.lang.tokenizer_exceptions import BASE_EXCEPTIONS
from spacy.lang.norm_exceptions import BASE_NORMS
from spacy.language import Language

from spacy.attrs import LANG, NORM
from spacy.util import add_lookups


class AncientGreekDefaults(Language.Defaults):
   
    lex_attr_getters = dict(Language.Defaults.lex_attr_getters)
    lex_attr_getters.update(LEX_ATTRS)
    lex_attr_getters[LANG] = lambda text: "grc"

    tokenizer_exceptions = BASE_EXCEPTIONS
    prefixes = TOKENIZER_PREFIXES
    infixes = TOKENIZER_INFIXES
    suffixes = TOKENIZER_SUFFIXES


class AncientGreek(Language):
    lang = "grc"
    Defaults = AncientGreekDefaults


__all__ = ["AncientGreek"]