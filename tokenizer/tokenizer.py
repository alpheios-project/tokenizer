# coding=utf8
from flask import Flask,abort,make_response,request
#from flask.ext.cache import Cache
from flask_restful import Resource, Api, reqparse
from flask_marshmallow import Marshmallow
#from marshmallow import Schema, fields, validate
from flask_cors import CORS
from flask_babel import Babel, gettext
from tokenizer.lib.spacy.processor import Processor
from tokenizer.lib.tei.parser import Parser
from tokenizer.schemas import TokenizeTeiRequestSchema, TokenizeTextRequestSchema, TokenizeResponseSchema, SegmentSchema, TokenSchema
from apispec import APISpec
from apispec.ext.marshmallow import MarshmallowPlugin
from apispec_webframeworks.flask import FlaskPlugin
import sys
import json

app = Flask("tokenizer")
ma = Marshmallow(app)
babel = Babel(app)

# Create an APISpec
spec = APISpec(
    title="Alpheios Tokenizer Service",
    version="1.0.0",
    openapi_version="3.0.2",
    plugins=[FlaskPlugin(), MarshmallowPlugin()],
)

def get_app():
    return app

def init_app(app=None, config_file="config.py"):
    app.config.from_pyfile(config_file,silent=False)

@babel.localeselector
def get_locale():
    return request.args['locale']

@app.route("/")
def api():
    return(json.dumps(spec.to_dict(),indent=2))

@app.route('/tokenize/tei', methods=['POST'])
def tokenize_tei():
    """ tokenize tei endpoint
    ---
    post:
      description: tokenize a TEI XML text
      parameters:
        - in: query
          schema: TokenizeTeiRequestSchema
      responses:
        201:
          content:
            application/json:
              schema: TokenizeResponseSchema
    """
    # TODO parse per content-type header
    # this is just plain text

    if (request.content_type != 'application/xml'):
        abort(400,"Unsupported content-type")

    schema = TokenizeTeiRequestSchema()
    text = request.data.decode(encoding="utf-8")
    errors = schema.validate(request.args)
    if errors:
        abort(400,str(errors))

    meta = {}
    config = schema.load(request.args)
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
    segments = _call_tokenizer(text=text,meta=meta,config=config)
    resp_schema = TokenizeResponseSchema()
    return resp_schema.dump({ 'meta': meta, 'segments': segments}), 201


@app.route('/tokenize/text', methods=['POST'])
def tokenize_text():
    """ tokenize endpoint
    ---
    post:
      description: tokenize text
      parameters:
        - in: query
          schema: TokenizeTextRequestSchema
      responses:
        201:
          content:
            application/json:
              schema: TokenizeResponseSchema
    """

    if (request.content_type != 'text/plain'):
        abort(400,f"Unsupported content-type {request.content_type}")

    schema = TokenizeTextRequestSchema()
    text = request.data.decode(encoding="utf-8")
    errors = schema.validate(request.args)
    if errors:
        abort(400,str(errors))

    #TODO parse document level metadata
    meta = {}

    config = schema.load(request.args)
    segments = _call_tokenizer(text=text,meta=meta,config=config)
    resp_schema = TokenizeResponseSchema()
    return resp_schema.dump({ 'meta': meta, 'segments': segments}), 201

def _call_tokenizer(text=None, meta=None, config=None):
    segmentMetadataTemplate = 'META|TB_SENT_{ALPHEIOS_SEGMENT_INDEX}' if config['tbseg'] else ""
    processor = Processor(config=None)
    segments = processor.tokenize(
        text=text,
        lang=config['lang'],
        segmentOn=config['segments'],
        segmentStart=config['segstart'],
        segmentMetadataTemplate=segmentMetadataTemplate
    )
    segmentsSchema = SegmentSchema()
    tokenSchema = TokenSchema()
    segs = []
    for segment in segments:
        tokens = []
        for token in segment['tokens']:
            tokens.append(tokenSchema.dump(token))
        segs.append(segmentsSchema.dump({'tokens': tokens, 'index':segment['index'], 'metadata':segment['metadata']}))
    return segs

with app.test_request_context():
    spec.path(view=tokenize_tei)

with app.test_request_context():
    spec.path(view=tokenize_text)
