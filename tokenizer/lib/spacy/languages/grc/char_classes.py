# taken from https://github.com/perseids-project/llt-tokenizer/blob/master/lib/llt/tokenizer/greek.rb
# TODO we need to add capital letters

PLAIN_VOWELS = "α ε ι η ο υ ω"
VOWELS_WITH_ACUTE = "ά έ ή ί ó ύ ώ"
VOWELS_WITH_GRAVE = "ὰ ὲ ὴ ì ò ὺ ὼ"
VOWELS_WITH_CIRCUMFLEX = "ᾶ ῆ ῖ ῦ ῶ"
VOWELS_WITH_IOTA = "ᾲ ᾳ ᾴ ᾷ ῂ ῃ ῄ ῇ ῲ ῳ ῴ ῷ"
CONSONANTS = "β γ δ ζ θ κ λ μ ν ξ π ρ ῥ ῤ σ ς τ φ χ ψ"
VOWELS = " ".join([
    PLAIN_VOWELS,
    VOWELS_WITH_ACUTE,
    VOWELS_WITH_GRAVE,
    VOWELS_WITH_CIRCUMFLEX,
    VOWELS_WITH_IOTA
])

SPIRITUS_LENIS = "ἀ ἐ ἠ ἰ ὀ ὐ ὠ"
SPIRITUS_LENIS_WITH_GRAVE = "ἂ ἒ ἲ ἢ ὂ ὒ ὢ"
SPIRITUS_LENIS_WITH_ACUTE = "ἄ ἔ ἴ ἤ ὄ ὔ ὤ"
SPIRITUS_LENIS_WITH_CIRCUMFLEX = "ἆ ἶ ἦ ὖ ὦ"

SPIRITUS_ASPER = "ἁ ἑ ἡ ἱ ὁ ὑ ὡ"
SPIRITUS_ASPER_WITH_GRAVE = "ἃ ἣ ἓ ἳ ὃ ὓ ὣ"
SPIRITUS_ASPER_WITH_ACUTE = "ἅ ἥ ἕ ἵ ὅ ὕ ὥ"
SPIRITUS_ASPER_WITH_CIRCUMFLEX = "ἇ ἷ ἧ ὗ ὧ"
SPIRITUS_WITH_IOTA = "ᾀ ᾁ ᾂ ᾃ ᾄ ᾅ ᾆ ᾇ ᾐ ᾑ ᾒ ᾓ ᾔ ᾕ ᾖ ᾗ ᾠ ᾡ ᾢ ᾣ ᾤ ᾥ ᾦ ᾧ"

VOWELS_WITH_SPIRITUS = " ".join([
    SPIRITUS_LENIS,
    SPIRITUS_LENIS_WITH_ACUTE,
    SPIRITUS_LENIS_WITH_GRAVE,
    SPIRITUS_LENIS_WITH_CIRCUMFLEX,
    SPIRITUS_ASPER,
    SPIRITUS_ASPER_WITH_ACUTE,
    SPIRITUS_ASPER_WITH_GRAVE,
    SPIRITUS_ASPER_WITH_CIRCUMFLEX,
    SPIRITUS_WITH_IOTA,
])

ALL = " ".join([
    CONSONANTS,
    VOWELS,
    VOWELS_WITH_SPIRITUS
])
