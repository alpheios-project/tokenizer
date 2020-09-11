from marshmallow import Schema, fields, validate
from tokenizer.lib.tei.parser import Parser

class TokenizeTeiRequestSchema(Schema):
    segments = fields.Str(
        required=False,
        missing=Parser.DEFAULT_SEGMENT_ELEMS
    )
    ignore= fields.Str(
        required=False,
        missing=Parser.DEFAULT_IGNORE_ELEMS
    )
    linebreaks = fields.Str(
        required=False,
        missing=Parser.DEFAULT_LINEBREAK_ELEMS
    )
    lang = fields.Str(required=True)
    sentencize = fields.Boolean(required=False, missing=False)
    tbseg = fields.Boolean(required=False, missing=False)
    segstart = fields.Integer(required=False, missing=0)

class TokenizeTextRequestSchema(Schema):
    segments = fields.Str(
        required=False,
        missing="singleline",
        validate=validate.OneOf(["singleline","doubline"])
    )
    sentencize = fields.Boolean(
        required=False,
        missing=False
    )
    lang = fields.Str(required=True)
    tbseg = fields.Boolean(required=False, missing=False)
    segstart = fields.Integer(required=False, missing=0)

