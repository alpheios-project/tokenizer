# coding=utf8
from flask import Flask,make_response,request
from flask_marshmallow import Marshmallow
from flask_cors import CORS
from flask_babel import Babel, gettext
from tokenizer.lib.spacy.processor import Processor
from tokenizer.lib.tei.parser import Parser, InvalidContentError, ParserError
from tokenizer.schemas import TokenizeTeiRequestSchema, TokenizeTextRequestSchema, TokenizeResponseSchema, SegmentSchema, TokenSchema, TokenizeErrorSchema
from apispec import APISpec
from apispec.ext.marshmallow import MarshmallowPlugin
from apispec_webframeworks.flask import FlaskPlugin
import sys
import json

app = Flask("tokenizer")
# CORS(app)
ma = Marshmallow(app)
babel = Babel(app)

# Create an OpenAPI Specification for the service
spec = APISpec(
    title="Alpheios Tokenizer Service",
    version="1.0.0",
    openapi_version="3.0.2",
    plugins=[FlaskPlugin(), MarshmallowPlugin()],
)

def get_app():
    """ Returns the Flask application
    """
    return app

def init_app(app=None, config_file="config.py"):
    """ Initializes the Flask application

    :param app: the Flask app
    :param config_file: path to a configuration file
    """
    app.config.from_pyfile(config_file,silent=False)

@babel.localeselector
def get_locale():
    """ Get the locale for schema descriptions

        :return: locale per request
        :rtype: string
    """
    return request.args['locale']

@app.route("/")
def api():
    """ Base endpoint - returns the OpenAPI schema for the service
    """
    if request.accept_mimetypes['text/html'] or 'application/json' not in request.accept_mimetypes:
        return(json.dumps(spec.to_dict(),indent=2))
    else:
        return(spec.to_dict())


@app.route('/tokenize/tei', methods=['POST'])
def tokenize_tei():
    """ Endpoint for tokenize TEI XML request
    ---
    post:
      description: Tokenize a TEI XML text
      parameters:
        - in: query
          schema: TokenizeTeiRequestSchema
      responses:
        201:
          description: tokenized text
          content:
            application/json:
              schema: TokenizeResponseSchema
        400:
          description: invalid request
          content:
            application/json:
              schema: TokenizeErrorSchema
    """
    # TODO parse per content-type header
    # this is just plain text

    if (request.content_type != 'application/xml'):
        return _make_error(400,"Unsupported content-type")

    schema = TokenizeTeiRequestSchema()
    text = request.data.decode(encoding="utf-8")
    errors = schema.validate(request.args)
    if errors:
        return _make_error(400,str(errors))

    meta = {}
    config = schema.load(request.args)
    # TODO we should maybe report an error if the lang of the text
    # differs from what was sent in the request arg
    parser = Parser(config=None)
    try:
        text = parser.parse_text(text,
            segmentElems=config['segments'],
            ignoreElems=config['ignore'],
            linebreakElems=config['linebreaks'])
        meta = parser.parse_meta(text)
    except InvalidContentError as exc:
        return _make_error(400,str(exc))

    # segments have been parsed from xml element to doubleline
    config['segments'] = 'doubleline'
    segments = _call_tokenizer(text=text,config=config)
    resp_schema = TokenizeResponseSchema()
    return resp_schema.dump({ 'meta': meta, 'segments': segments}), 201


@app.route('/tokenize/text', methods=['POST'])
def tokenize_text():
    """ Endpoint for tokenize plain text request
    ---
    post:
      description: Tokenize a plain text document.
      parameters:
        - in: query
          schema: TokenizeTextRequestSchema
      responses:
        201:
          description: tokenized text
          content:
            application/json:
              schema: TokenizeResponseSchema
        400:
          description: invalid request
          content:
            application/json:
              schema: TokenizeErrorSchema
    """

    if (request.content_type != 'text/plain'):
        return _make_error(400,f"Unsupported content-type {request.content_type}")

    schema = TokenizeTextRequestSchema()
    text = request.data.decode(encoding="utf-8")
    errors = schema.validate(request.args)
    if errors:
        _make_error(400,str(errors))

    #TODO parse document level metadata
    meta = {}

    config = schema.load(request.args)
    segments = _call_tokenizer(text=text,config=config)
    resp_schema = TokenizeResponseSchema()
    return resp_schema.dump({ 'meta': meta, 'segments': segments}), 201

def _call_tokenizer(text=None, config=None):
    """ private method - executes the tokenization request

        :param text: Text to be tokenized
        :param config: request arguments

        :return: segmented token
        :rtype: SegmentSchema[]
    """
    segmentMetadataTemplate = 'META|TB_SENT_{ALPHEIOS_SEGMENT_INDEX}' if 'tbsegstart' in config else ""
    processor = Processor()
    segments = processor.tokenize(
        text=text,
        lang=config['lang'],
        segmentOn=config['segments'],
        segmentStart= config['tbsegstart'] if 'tbsegstart' in config else 1,
        segmentMetadataTemplate=segmentMetadataTemplate
    )
    segmentsSchema = SegmentSchema()
    tokenSchema = TokenSchema()
    segs = []
    for segment in segments:
        tokens = []
        for token in segment['tokens']:
            tokens.append(tokenSchema.dump(token))
        segdata = {
            'tokens': tokens,
            'index':segment['index']
        }
        for metadata in ('alpheios_data_tb_sent', 'alpheios_data_cite'):
            if metadata in segment:
                segdata[metadata] = segment[metadata]
        segs.append(segmentsSchema.dump(segdata))
    return segs

def _make_error(status_code, message):
    errorSchema = TokenizeErrorSchema()
    response = {
        'status': status_code,
        'message': message
    }
    return errorSchema.dump(response), status_code

## Add tokenize_tei operation to the OpenApi doc
with app.test_request_context():
    spec.path(view=tokenize_tei)

# Add tokenize_text operation to the OpenApi doc
with app.test_request_context():
    spec.path(view=tokenize_text)
