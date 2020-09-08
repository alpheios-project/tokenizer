from flask_restful import Resource
from flask import request, abort, jsonify
from marshmallow import Schema, fields
from tokenizer.lib.spacy.wrapper import Wrapper
from tokenizer.lib.tei.parser import Parser
import sys

class TokenSchema(Schema):
    index = fields.Integer(required=True)
    docIndex = fields.Integer(required=True)
    text = fields.Str(required=True)
    is_punct = fields.Boolean(required=True)
    start_sent = fields.Boolean(required=True)
    tb_word = fields.Str(required=True)
    lb_before = fields.Boolean(required=True)

class SegmentSchema(Schema):
    tokens = fields.List(fields.Nested(TokenSchema),required=True)
    index = fields.Integer(required=True)
    tb_sent = fields.Str(required=True)

class TokenizeResponseSchema(Schema):
    segments: fields.List(fields.Nested(SegmentSchema))

class TokenizeResponse(Resource):
    """ Response to a request for tokenization """

    def __init__(self, **kwargs):
        """ Constructor
        """

