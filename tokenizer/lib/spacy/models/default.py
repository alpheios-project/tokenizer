import spacy
from spacy.tokenizer import Tokenizer
from tokenizer.lib.spacy.lang.mapper import Mapper
import re

class Default():
    """ The Default Model is one which uses the Spacy Language class
        for tokenization, with non-language-specific overrides for
        URL_MATCH and XML ENTITIES. This class can be subclassed if alternate
        tokenization models are needed (e.g. to include configurable options, to
        include retokenization, etc. )
    """

    URL_MATCH = re.compile(r'''^(CITE_)?(urn:)|(https?:\/\/)''')
    SPECIAL_CASES = {}

    ENTITIES = [
      "&apos;",
      "&quot;",
      "&amp;",
      "&gt;",
      "&lt;"
    ]

    def __init__(self):
        """ Constructor """
        self.mapper = Mapper()

    def load_model(self,lang=None,config=None):
        """ loads and configures the spacy language model

            :param lang: the language of the text
            :type: string
            :param config: optional dict of config options
            :type: dict

            :return: the spacy language model
            :rtype: spacy.language.Language
        """
        nlp = self._model(lang)
        self._tokenizer(nlp=nlp,config=config)
        self._entities(nlp)
        return nlp

    def _entities(self,nlp):
        """ adds additional entities applicable to all languages """
        # we add these individually after the tokenizer is constructed because
        # the xml entity match should apply to all languages but
        # not override any other special cases for the language that were
        # added in the language model
        for entity in Default.ENTITIES:
            try:
                nlp.tokenizer.add_special_case(entity, [{"ORTH":entity}])
            except:
                # it seems that some tokenizers don't implement this (chinese eg)
                pass

    def _model(self,lang):
        """ loads the right model for the language """
        language = self.mapper.get_language(lang)
        if language:
            return language()
        else:
            raise(f"Unable to load Language class for {lang}")

    def _tokenizer(self,nlp=None,config=None):
        """ adds tokenizer overrides that apply to all languages """
        nlp.tokenizer.url_match = Default.URL_MATCH.match


