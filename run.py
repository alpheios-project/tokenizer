#!/usr/bin/env python
from flask import Flask
import click
import time
from tokenizer.tokenizer import init_app, get_app
from tokenizer.lib.tei.parser import Parser
from tokenizer.lib.spacy.processor import Processor

# Input Profiles
# TEI, Line Breaks preserved  => Single Segment
# TEI, Line Breaks preserved, word-level treebank refs => Single Segment
# TEI, Line Breaks preserved, word-level treebank refs, Segments preserved => Multiple Segments
# TEI, Line Breaks preserved, sentence-level treebank refs  => Single Segment
# Plain text, Line Breaks for Display preserved => Single Segment
# Plain text, Line Brekas for Segments, no mid-segment Line Break => Multiple Segments
# Plain text, Line Breaks preserved, Special tagged Segments  preserved => Multiple Segments
# Plain text, Sentencized for treebank, start sentence configurable, Line breaks for Display => Single Segment

# Output
# metadata
#   cite
#   title
#   author
#   work
#   edition
#   part
# segments
#   index
#   type
#   beadType [ optional ]
#   cite [ optional]
#   tokens
#     index
#     text
#     cite [ optional ]
#   line break after
#   tbrefs { sent, word }
#   is sentence start

tei = '<TEI xmlns="http://www.tei-c.org/ns/1.0"><teiHeader></teiHeader><text><body><l>θεοὺς μὲν αἰτῶ τῶνδ᾽ ἀπαλλαγὴν πόνων φρουρᾶς ἐτείας μῆκος,</l> <l>ἣν κοιμώμενος στέγαις Ἀτρειδῶν ἄγκαθεν, κυνὸς δίκην,</l><l>ἄστρων κάτοιδα νυκτέρων ὁμήγυριν, καὶ τοὺς φέροντας χεῖμα καὶ θέρος βροτοῖς λαμπροὺς δυνάστας, ἐμπρέποντας αἰθέρι [ἀστέρας, ὅταν φθίνωσιν, ἀντολάς τε τῶν].  καὶ νῦν φυλάσσω λαμπάδος τό σύμβολον, αὐγὴν πυρὸς φέρουσαν ἐκ Τροίας φάτιν ἁλώσιμόν τε βάξιν : ὧδε γὰρ κρατεῖ γυναικὸς ἀνδρόβουλον ἐλπίζον κέαρ.  εὖτ᾽ ἂν δὲ νυκτίπλαγκτον ἔνδροσόν τ᾽ ἔχω εὐνὴν ὀνείροις οὐκ ἐπισκοπουμένην ἐμήν : φόβος γὰρ ἀνθ᾽ ὕπνου παραστατεῖ, τὸ μὴ βεβαίως βλέφαρα συμβαλεῖν ὕπνῳ:</l></body></text></TEI>'

with open("tests/fixtures/tei/ovidmet.xml", "r", encoding="utf-8") as myfile:
  tei = myfile.read()

# we could use metadata the top of the file to supply
# - starting sentence number for treebank integration
plaintext = "the quick brown fox\n\njumped over the lazy dog."

@click.group()
def cli():
    pass

@cli.command("server")
def server():
    app = get_app()
    init_app(app,"config.cfg")
    app.run(debug=True, host="0.0.0.0", port=5000)

@cli.command("run")
@click.option("--xsl", default="tokenizer/plaintext.xsl", help="XSL")
def run(xsl=None):

    parser = Parser(config=None)
    text = parser.parse_text(tei)
    print(text)
    processor = Processor(config=None)
    tokens = processor.tokenize(text=text, lang='en',sentencize=False, segon='seg')

    for token in tokens:
        print(token)



if __name__ == "__main__":
    cli()

