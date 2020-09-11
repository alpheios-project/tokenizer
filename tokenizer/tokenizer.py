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
from apispec import APISpec
from apispec.ext.marshmallow import MarshmallowPlugin
from apispec_webframeworks.flask import FlaskPlugin
import sys
import json

app = Flask("tokenizer")
#api = Api(app=app, default_mediatype='application/json')
ma = Marshmallow(app)
#cache = Cache(app,config={'CACHE_TYPE':'simple'})

# Create an APISpec
spec = APISpec(
    title="Alpheios Tokenizer Service",
    version="1.0.0",
    openapi_version="3.0.2",
    plugins=[FlaskPlugin(), MarshmallowPlugin()],
)

def get_app():
    return app

def init_app(app=None, config_file="config.cfg",cache_config=None):
    app.config.from_pyfile(config_file,silent=False)
    if cache_config is not None:
        cache.init_app(app,config=cache_config)

@app.route('/tokenize', methods=['POST'])
def tokenize():
    """ tokenize endpoint
    ---
    post:
      description: tokenize text
      parameters:
        - in: query
          schema: TokenizeTeiRequestSchema
      responses:
        201:
          content:
            application/json:
              schema: TokenizeTextRequestSchema
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

@app.route("/")
def api():
    return(json.dumps(spec.to_dict(),indent=2))


with app.test_request_context():
    spec.path(view=tokenize)
