# coding=utf8
from flask import Flask,abort,make_response
#from flask.ext.cache import Cache
from flask_restful import Resource, Api, reqparse
from flask_cors import CORS
from tokenizer.tokenizerequest import TokenizeRequest

app = Flask("tokenizer")
api = Api(app=app, default_mediatype='application/json')
#cache = Cache(app,config={'CACHE_TYPE':'simple'})

def get_app():
    return app

def init_app(app=None, config_file="config.cfg",cache_config=None):
    app.config.from_pyfile(config_file,silent=False)
    if cache_config is not None:
        cache.init_app(app,config=cache_config)

api.add_resource(
    TokenizeRequest,
    '/tokenize',
    resource_class_kwargs={ 'config':app.config, 'cache': None }
)

