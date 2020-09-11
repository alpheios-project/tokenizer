# coding=utf8
from flask import Flask,abort,make_response,request
#from flask.ext.cache import Cache
from flask_restful import Resource, Api, reqparse
from flask_marshmallow import Marshmallow
#from marshmallow import Schema, fields, validate
from flask_cors import CORS
from tokenizer.lib.spacy.processor import Processor
from tokenizer.lib.tei.parser import Parser
from tokenizer.schemas import TokenizeTeiRequestSchema, TokenizeTextRequestSchema
import sys

app = Flask("tokenizer")
#api = Api(app=app, default_mediatype='application/json')
ma = Marshmallow(app)
#cache = Cache(app,config={'CACHE_TYPE':'simple'})

def get_app():
    return app

def init_app(app=None, config_file="config.cfg",cache_config=None):
    app.config.from_pyfile(config_file,silent=False)
    if cache_config is not None:
        cache.init_app(app,config=cache_config)

@app.route('/tokenize', methods=['POST'])
def tokenize():
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

