import spacy
from spacy.tokenizer import Tokenizer
import re

class BaseModel():

    URL_MATCH = re.compile(r'''^(CITE_)?(urn:)|(https?:\/\/)''')

    def load_model(self):
        nlp = spacy.load(self.model())
        nlp.tokenizer.url_match = BaseModel.URL_MATCH.match
        return nlp

    def model(self):
        return "en_core_web_sm"

