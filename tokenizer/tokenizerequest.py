from flask_restful import Resource
from flask import request, abort, jsonify
from marshmallow import Schema, fields
from tokenizer.lib.spacy.wrapper import Wrapper
import sys

class TokenizeRequestSchema(Schema):
    # TODO could take from content-type header
    format = fields.Str(required=True)
    lang = fields.Str(required=True)


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
        schema = TokenizeRequestSchema()
        errors = schema.validate(request.args)
        if errors:
            abort(400,str(errors))
        print(">>>>>>>>>>>>Text",request.data,file=sys.stdout)
        text = request.data.decode(encoding="utf-8")
        print(">>>>>>>>>>>>Text",text,file=sys.stdout)
        return { 'data': self.call_tokenizer(text)}, 201

    def call_tokenizer(self, text=None):
        """ Execute a tokenization request
        """
        wrapper = Wrapper(config=None)
        tokens = wrapper.tokenize(lang='en',text=text, sentences=False)
        return tokens

