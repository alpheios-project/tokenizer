from tokenizer.lib.spacy.languages.la import Latin
from spacy.lang.en import English
from spacy.lang.fr import French

LANGUAGE = {
    'en': English,
    'fr': French,
    'la': Latin
}

CODES = {
    'lat': 'la',
}

class Mapper():
    
    def get_language(self,lang='en'):
        """ get the spacy language processor for the requested language

            :param lang: the requested language
            :type: string

            :return: the language processor class
            :rtype: spacy.language.Language
        """
        lang = self.map_code(lang)
        if lang in LANGUAGE:
            return LANGUAGE[lang]
        else:
            return None

    def map_code(self,lang):
        """ maps a language code to the lookup key
            :param lang: the language code

            :return: the language lookup key
            :rtype: string
        """
        if lang in CODES:
            return CODES[lang]
        else:
            return lang


