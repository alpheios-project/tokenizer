# lower case and groupings taken from
# llt-tokenizer https://github.com/perseids-project/llt-tokenizer/blob/master/lib/llt/tokenizer/greek.rb

CONSONANTS = "β γ δ ζ θ κ λ μ ν ξ π ρ ῥ ῤ σ ς τ φ χ ψ ϝ Β Γ Δ Ζ Θ Κ Λ Μ Ν Ξ Π Ρ Ῥ Σ Τ Φ Χ Ψ Ϝ"

PLAIN_VOWELS = "α ε ι η ο υ ω Α Ε Ι Η Ο Υ Ω"
VOWELS_WITH_ACUTE = "ά έ ή ί ó ύ ώ Ά Έ Ή Ί Ό Ύ Ώ"
VOWELS_WITH_GRAVE = "ὰ ὲ ὴ ì ò ὺ ὼ Ὰ Ὲ Ὴ Ὶ Ὸ Ὺ Ὼ"
VOWELS_WITH_CIRCUMFLEX = "ᾶ ῆ ῖ ῦ ῶ"
VOWELS_WITH_IOTA = "ᾲ ᾳ ᾴ ᾷ ῂ ῃ ῄ ῇ ῲ ῳ ῴ ῷ ᾼ ῌ ῼ"
OTHER_VOWELS = "Ᾱ Ᾰ Ϊ Ῑ Ῐ Ϋ Ῡ Ῠ"

VOWELS = " ".join([
    PLAIN_VOWELS,
    VOWELS_WITH_ACUTE,
    VOWELS_WITH_GRAVE,
    VOWELS_WITH_CIRCUMFLEX,
    VOWELS_WITH_IOTA,
    OTHER_VOWELS
])

SPIRITUS_LENIS = "ἀ ἐ ἠ ἰ ὀ ὐ ὠ Ἀ Ἐ Ἰ Ἠ Ὀ Ὠ"
SPIRITUS_LENIS_WITH_GRAVE = "ἂ ἒ ἲ ἢ ὂ ὒ ὢ Ἂ Ἒ Ἲ Ἢ Ὂ Ὢ"
SPIRITUS_LENIS_WITH_ACUTE = "ἄ ἔ ἴ ἤ ὄ ὔ ὤ Ἄ Ἔ Ἴ Ἤ Ὄ Ὤ"
SPIRITUS_LENIS_WITH_CIRCUMFLEX = "ἆ ἶ ἦ ὖ ὦ Ἆ Ἶ Ἦ Ὦ"

SPIRITUS_ASPER = "ἁ ἑ ἡ ἱ ὁ ὑ ὡ Ἁ Ἑ Ἱ Ἡ Ὁ Ὑ Ὡ"
SPIRITUS_ASPER_WITH_GRAVE = "ἃ ἣ ἓ ἳ ὃ ὓ ὣ Ἃ Ἓ Ἳ Ἣ Ὃ Ὓ Ὣ"
SPIRITUS_ASPER_WITH_ACUTE = "ἅ ἥ ἕ ἵ ὅ ὕ ὥ Ἅ Ἕ Ἵ Ἥ Ὅ Ὕ Ὥ"
SPIRITUS_ASPER_WITH_CIRCUMFLEX = "ἇ ἷ ἧ ὗ ὧ Ἇ Ἷ Ἧ Ὗ Ὧ"
SPIRITUS_WITH_IOTA = "ᾀ ᾁ ᾂ ᾃ ᾄ ᾅ ᾆ ᾇ ᾐ ᾑ ᾒ ᾓ ᾔ ᾕ ᾖ ᾗ ᾠ ᾡ ᾢ ᾣ ᾤ ᾥ ᾦ ᾧ ᾈ ᾉ ᾊ ᾋ ᾌ ᾍ ᾏ ᾎ ᾘ ᾙ ᾜ ᾝ ᾚ ᾛ ᾞ ᾟ ᾬ ᾭ ᾪ ᾫ ᾮ ᾯ ᾨ ᾩ"

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
