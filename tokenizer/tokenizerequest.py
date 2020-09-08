from flask_restful import Resource
from flask import request, abort, jsonify
from marshmallow import Schema, fields
from tokenizer.lib.spacy.processor import Processor
from tokenizer.lib.tei.parser import Parser
import sys

class TokenizeTeiRequestSchema(Schema):
    segments = fields.Str(required=False,default="seg", missing="seg")
    sentencize = fields.Boolean(required=False, default=True, missing=True)
    linebreaks = fields.Str(required=False,default="div,l,p,ab,seg", missing="div,l,p,ab,seg")
    lang = fields.Str(required=True)
    tbseg = fields.Boolean(required=False, default=False, missing=False)
    segstart = fields.Integer(required=False, default=1, missing=1)

class TokenizeTextRequestSchema(Schema):
    segments = fields.Str(required=False,default="newline",missing="newline")
    sentencize = fields.Boolean(required=False, default=False, missing=False)
    linebreaks = fields.Boolean(required=False, default=True, missing=True)
    lang = fields.Str(required=True)
    tbseg = fields.Boolean(required=False, default=False, missing=False)
    segstart = fields.Integer(required=False, default=1, missing=1)

class TokenizeRequest(Resource):
    """ Responds to a request for tokenization """

    def __init__(self, **kwargs):
        """ Constructor
        :param cache: The Cache to be used to store and retrieve results
        :type cache: flask.ext.cache.Cache
        :param config: The Flask App Config
        :type config: dict
        """
        self.cache = kwargs['cache']
        self.config = kwargs['config']

    def post(self):
        """ Respond to a POST request
        :param format: the format of the data (required)
        :param lang: the language of the data (required)
        :return: tokens
        """
        # TODO parse per content-type header
        # this is just plain text

        if (request.content_type == 'text/plain'):
            schema = TokenizeTextRequestSchema()
        elif (request.content_type == 'application/xml'):
            schema = TokenizeTeiRequestSchema()
        else:
            abort(400,"Unsupported content-type")

        text = request.data.decode(encoding="utf-8")
        errors = schema.validate(request.args)
        if errors:
            abort(400,str(errors))

        meta = {}
        if (request.content_type == 'application/xml'):
            parser = Parser(config=None)
            text = parser.parse_text(text)
            meta = parser.parse_meta(text)

        config = schema.load(request.args)
        tokens = self.call_tokenizer(text=text,config=config)

        tokenized = {
            'meta': meta,
            'tokens': tokens
        }

        return tokenized, 201

    def call_tokenizer(self, text=None, config=None):
        """ Execute a tokenization request
        """
        wrapper = Wrapper(config=None)
        tokens = wrapper.tokenize(text=text, config=config)
        return tokens

