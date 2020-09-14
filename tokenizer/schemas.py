from marshmallow import Schema, fields, validate
from tokenizer.lib.tei.parser import Parser
from flask_babel import Babel, gettext

class TokenizeTeiRequestSchema(Schema):
    segments = fields.Str(
        required=False,
        missing=Parser.DEFAULT_SEGMENT_ELEMS,
        description=gettext("Comma-separated list of elements which identify segments."),
    )
    ignore= fields.Str(
        required=False,
        missing=Parser.DEFAULT_IGNORE_ELEMS,
        description=gettext("Comma-separated list of elements whose contents should be ignored.")
    )
    linebreaks = fields.Str(
        required=False,
        missing=Parser.DEFAULT_LINEBREAK_ELEMS,
        description=gettext("Comma-separated list of elements to line-break after for display."),
    )
    lang = fields.Str(
        required=True,
        description=gettext("Language code of text to be tokenized.")
    )
    tbseg = fields.Boolean(
        required=False,
        missing=False,
        description=gettext("True means 'alpheios_data_tb_sent' metadata to be set from segment index")
    )
    segstart = fields.Integer(
        required=False,
        missing=0,
        description=gettext("Starting segment index.")
    )

class TokenizeTextRequestSchema(Schema):
    segments = fields.Str(
        required=False,
        missing="singleline",
        description=gettext("Segment indicator."),
        validate=validate.OneOf(["singleline","doubline"])
    )
    lang = fields.Str(
        required=True,
        description=gettext("Language code of text to be tokenized.")
    )
    tbseg = fields.Boolean(
        required=False,
        missing=False,
        description=gettext("True means 'alpheios_data_tb_sent' metadata to be set from segment index.")
    )
    segstart = fields.Integer(
        required=False,
        missing=0,
        description=gettext("Starting segment index.")
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


