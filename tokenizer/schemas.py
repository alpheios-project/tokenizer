from marshmallow import Schema, fields, validate
from tokenizer.lib.tei.parser import Parser
from flask_babel import Babel, gettext

class TokenizeTeiRequestSchema(Schema):
    segments = fields.Str(
        required=False,
        missing=Parser.DEFAULT_SEGMENT_ELEMS,
        description=gettext("Supply a comma-separated list of TEI elements in the text which group segments of tokens."),
    )
    ignore= fields.Str(
        required=False,
        missing=Parser.DEFAULT_IGNORE_ELEMS,
        description=gettext("Supply a comma-separated list of TEI elements in the text whose contents should be ignored for tokenization.")
    )
    linebreaks = fields.Str(
        required=False,
        missing=Parser.DEFAULT_LINEBREAK_ELEMS,
        description=gettext("Supply a comma-separated list of elements in the text that represent visual blocks."),
    )
    lang = fields.Str(
        required=True,
        description=gettext("Supply the iso language code of the text.")
    )
    direction = fields.Str(
        required=False,
        description=gettext("Supply the display direction of the text."),
        missing = "ltr",
        validate = validate.OneOf(["ltr","rtl"])
    )
    tbsegstart = fields.Integer(
        required=False,
        description=gettext("If this text is aligned with a treebank, specify the starting segment index")
    )

class TokenizeTextRequestSchema(Schema):
    segments = fields.Str(
        required=False,
        missing="onesegment",
        description=gettext("Identify how segments are separated in the text."),
        validate=validate.OneOf(["singleline","doubleline", "onesegment"])
    )
    lang = fields.Str(
        required=True,
        description=gettext("Supply the iso language code of the text.")
    )
    direction = fields.Str(
        required=False,
        description=gettext("Supply the display direction of the text."),
        missing = "ltr",
        validate = validate.OneOf(["ltr","rtl"])
    )
    tbsegstart = fields.Integer(
        required=False,
        description=gettext("If this text is aligned with a treebank, specify the starting segment index")
    )

class TokenSchema(Schema):
    index = fields.Integer(
        required=True,
        description=gettext("Index of the Token in the parent Segment.")
    )
    docIndex = fields.Integer(
        required=True,
        description = gettext("Index of the Token in the Document.")
    )
    text = fields.Str(
        required=True,
        description = gettext("Text contents of the Token.")
    )
    punct = fields.Boolean(
        required=True,
        description = gettext("Indicates if the Token is Punctuation.")
    )
    line_break_before = fields.Boolean(
        required=True,
        description = gettext("Indicates if the Token should have a Line Break displayed before it.")
    )
    alpheios_data_tb_word = fields.Str(
        required=False,
        description = gettext("Metadata field for Alpheios Reading Tools - provides Treebank Word Identifier.")
    )
    alpheios_data_cite = fields.Str(
        required=False,
        description = gettext("Metadata field for Alpheios Reading Tools - provides Citatable Identifier.")
    )

class SegmentSchema(Schema):
    tokens = fields.List(
        fields.Nested(TokenSchema),
        required=True,
        description = gettext("List of Tokens in the Segment.")
    )
    index = fields.Integer(
        required=True,
        description=gettext("Index of Segment in the Document.")
    )
    alpheios_data_tb_sent = fields.Str(
        required=False,
        description = gettext("Metadata field for Alpheios Reading Tools - provides Treebank Sentence Identifier.")
    )
    alpheios_data_cite = fields.Str(
        required=False,
        description = gettext("Metadata field for Alpheios Reading Tools - provides Citatable Identifier.")
    )

class TokenizeResponseSchema(Schema):
    segments = fields.List(
        fields.Nested(SegmentSchema),
        required=True,
        description = gettext("List of Segments.")
    )
    metadata = fields.Dict(
        required = True,
        description = gettext("Text-level metadata dictionary.")
    )

class TokenizeErrorSchema(Schema):
    message = fields.Str(
        required = True,
        description = gettext("Error message")
    )
    status = fields.Str(
        required = True,
        description = gettext("Status code")
    )

