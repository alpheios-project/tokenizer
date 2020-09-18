import importlib

LANGUAGE = {
    'af': { "name": "Afrikaans" },
    'ar': { "name": "Arabic" },
    'bg': { "name": "Bulgarian"},
    'bn': { "name": "Bengali"},
    'ca': { "name": "Catalan"},
    'cs': { "name": "Czech"},
    'de': { "name": "German"},
    'el': { "name": "Greek"},
    'en': { "name": "English" },
    'es': { "name": "Spanish" },
    'et': { "name": "Estonian" },
    'eu': { "name": "Basque" },
    'fa': { "name": "Persian" },
    'fi': { "name": "Finnish" },
    'fr': { "name": "French" },
    'ga': { "name": "Irish" },
    'grc': { "path": "tokenizer.lib.spacy.languages.grc", "name": "AncientGreek"},
    'gu': { "name": "Gujarati" },
    'he': { "name": "Hebrew" },
    'hi': { "name": "Hindi" },
    'hr': { "name": "Croatian" },
    'hu': { "name": "Hungarian" },
    'hy': { "name": "Armenian" },
    'id': { "name": "Indonesian" },
    'is': { "name": "Icelandic" },
    'it': { "name": "Italian" },
    'ja': { "name": "Japanese" },
    'kn': { "name": "Kannada" },
    'ko': { "name": "Korean" },
    'la': { "path": "tokenizer.lib.spacy.languages.la", "name": "Latin"},
    'lb': { "name": "Luxembourgish" },
    'lij': { "name": "Ligurian" },
    'lt': { "name": "Lithuanian" },
    'lv': { "name": "Latvian" },
    'ml': { "name": "Malayalam" },
    'mr': { "name": "Marathi" },
    'nb': { "name": "Norwegian" },
    'ne': { "name": "Nepali" },
    'nl': { "name": "Dutch" },
    'pl': { "name": "Polish" },
    'pt': { "name": "Portuguese" },
    'ro': { "name": "Romanian" },
    'ru': { "name": "Russian" },
    'sa': { "name": "Sanskrit" },
    'si': { "name": "Sinhala" },
    'sk': { "name": "Slovak" },
    'sl': { "name": "Slovenian" },
    'sq': { "name": "Albanian" },
    'sr': { "name": "Serbian" },
    'sv': { "name": "Swedish" },
    'ta': { "name": "Tamil" },
    'te': { "name": "Telegu" },
    'th': { "name": "Thai" },
    'tl': { "name": "Tagalog" },
    'tr': { "name": "Turkish" },
    'tt': { "name": "Tatar" },
    'uk': { "name": "Ukranian" },
    'ur': { "name": "Urdu" },
    'vi': { "name": "Vietnamese" },
    'xx': { "name": "MultiLanguage"},
    'yo': { "name": "Yoruba" },
    'zh': { "name": "Chinese" }
}

# Alpheios has traditionally used 3 character codes
# need to map to the ones used by Spacy
CODES = {
    'afr': 'af',
    'ara': 'ar',
    'blu': 'bg',
    'chu': 'bg',
    'ben': 'bn',
    'cat': 'ca',
    'ces': 'cs',
    'deu': 'de',
    'ell': 'el',
    'eng': 'en',
    'spa': 'es',
    'est': 'et',
    'eus': 'eu',
    'fas': 'fa',
    'fin': 'fi',
    'fra': 'fr',
    'gle': 'ga',
    'guj': 'gu',
    'heb': 'he',
    'hin': 'hi',
    'hrv': 'hr',
    'hye': 'hy',
    'hun': 'hu',
    'ind': 'id',
    'isl': 'is',
    'ita': 'it',
    'jpn': 'ja',
    'kan': 'kn',
    'kor': 'ko',
    'lat': 'la',
    'lit': 'lt',
    'msa': 'ml',
    'mar': 'mr',
    'nor': 'nb',
    'nep': 'ne',
    'nld': 'nl',
    'pol': 'pl',
    'por': 'pt',
    'ron': 'ro',
    'rus': 'ru',
    'san': 'sa',
    'sin': 'si',
    'slk': 'sk',
    'slv': 'sl',
    'sqi': 'sq',
    'srp': 'sr',
    'swe': 'sv',
    'tam': 'ta',
    'tel': 'te',
    'tha': 'th',
    'tgl': 'tl',
    'tur': 'tr',
    'tat': 'tt',
    'ukr': 'uk',
    'urd': 'ur',
    'vie': 'vi',
    'zhu': 'zh',
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
        if lang not in LANGUAGE:
            # use the MultiLanguage class if we don't have the right one
            lang = 'xx'
        load_info = LANGUAGE[lang]
        try:
            path = load_info['path'] if 'path' in load_info else f"spacy.lang.{lang}"
            mod = importlib.import_module(path)
            langC = getattr(mod, load_info['name'])
            return langC
        except:
            return null




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


