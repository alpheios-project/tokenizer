from spacy.lang.char_classes import CONCAT_QUOTES, UNITS, ALPHA, ALPHA_LOWER, ALPHA_UPPER

#TODO accented vowels
SPECIAL_CASES_ENCLYTICS = dict(
    {
        'nec': [{"ORTH":"ne"},{"ORTH":"c"}],
        'Nec': [{"ORTH":"ne"},{"ORTH":"c"}],
        'nese': [{"ORTH":"ne"},{"ORTH":"se"}],
        'Nese': [{"ORTH":"ne"},{"ORTH":"se"}],
        'nisi': [{"ORTH":"ni"},{"ORTH":"si"}],
        'Nisi': [{"ORTH":"ni"},{"ORTH":"si"}],
    },
)

LOWER_A = '''a\u00e0\u00e1\u00e2\u00e3\u00e4\u0101\u0103'''
LOWER_E = '''e\u00e8\u00e9\u00ea\u00eb\u0113\u0115'''
LOWER_U = '''u\u00ec\u00ed\u00ee\u00ef\u012b\u012d\u0129'''
LOWER_I = '''i\u00f9\u00fa\u00fb\u00fc\u016b\u016d'''







