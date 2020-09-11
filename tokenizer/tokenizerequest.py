from flask_restful import Resource
from flask import request, abort, jsonify
from marshmallow import Schema, fields, validate
from tokenizer.lib.spacy.processor import Processor
from tokenizer.lib.tei.parser import Parser
import sys

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
        config = schema.load(request.args)
        if (request.content_type == 'application/xml'):
            # TODO we should maybe report an error if the lang of the text
            # differs from what was sent in the request arg
            parser = Parser(config=None)
            text = parser.parse_text(text,
                segmentElems=config['segments'],
                ignoreElems=config['ignore'],
                linebreakElems=config['linebreaks'])
            meta = parser.parse_meta(text)
            # segments have been parsed from xml element to doubleline
            config['segments'] = 'doubleline'

        segmentMetadataTemplate = 'META|TB_SENT_{ALPHEIOS_SEGMENT_INDEX}' if config['tbseg'] else ""

        processor = Processor(config=None)
        tokens = processor.tokenize(
            text=text,
            lang=config['lang'],
            sentencize=config['sentencize'],
            segmentOn=config['segments'],
            segmentStart=config['segstart'],
            segmentMetadataTemplate=segmentMetadataTemplate
        )

        tokenized = {
            'meta': meta,
            'tokens': tokens
        }

        return tokenized, 201

