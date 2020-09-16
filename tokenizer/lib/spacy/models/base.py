import spacy
from spacy.tokenizer import Tokenizer
import re

class Base():

    URL_MATCH = re.compile(r'''^(CITE_)?(urn:)|(https?:\/\/)''')
    SPECIAL_CASES = {}

    ENTITIES = [
      "&apos;",
      "&quot;",
      "&amp;",
      "&gt;",
      "&lt;"
    ]

    def load_model(self,config):
        nlp = spacy.load(self._model())
        self._tokenizer(nlp=nlp,config=config)
        self._entities(nlp)
        return nlp

    def _entities(self,nlp):
        # we add these individually after the tokenizer is constructed because
        # the xml entity match should apply to all languages but
        # not override any other special cases for the language that were
        # added in the language model
        for entity in Base.ENTITIES:
            nlp.tokenizer.add_special_case(entity, [{"ORTH":entity}])

    def _model(self):
        return "en_core_web_sm"

    def _tokenizer(self,nlp=None,config=None):
        nlp.tokenizer.url_match = Base.URL_MATCH.match


