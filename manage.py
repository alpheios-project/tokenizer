#!/usr/bin/env python
from flask import Flask
from flask.cli import FlaskGroup
from tokenizer.tokenizer import init_app, get_app

print ('hello, world!')
app = get_app()
init_app(app)
cli = FlaskGroup(app)


if __name__ == "__main__":
    cli()

