from tokenizer.lib.spacy.models.base import BaseModel

MODEL = {
    'default': BaseModel
}

CODES = {
    'la': 'lat',
}

class Languages():

    def map_language(self,lang):
        if lang in CODES:
            return CODES[lang]
        else:
            return lang

    def model(self,lang):
        langmodel = self._get_by_lang(MODEL,lang)()
        return langmodel.load_model()

    def _get_by_lang(self,rules=None,lang=None):
        lang = self.map_language(lang)
        if lang in rules:
            return rules[lang]
        else:
            return rules['default']


