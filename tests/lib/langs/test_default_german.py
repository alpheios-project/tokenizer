import unittest
from unittest import TestCase
from tokenizer.lib.spacy.models.default import Default
import re
import os

class TestGermanDefault(TestCase):

    def setUp(self):
        model = Default()
        self.nlp = model.load_model(lang="deu",config={})

    def tearDown(self):
        pass

    def readFixture(self, type=None, name=None):
        fixture = os.path.join('tests', 'fixtures', type, name)
        with open(fixture, 'r', encoding="utf-8") as (stream):
            text = stream.read()
        return text

    def testCatalanTokens(self):
        text = self.readFixture(type='langs', name='german.txt')
        doc = self.nlp(text)
        # Mein Name ist Anna. Ich komme aus Österreich und lebe seit drei Jahren in Deutschland.

        self.assertEqual(doc[0].text,"Mein")
        self.assertEqual(doc[1].text,"Name")
        self.assertEqual(doc[2].text,"ist")
        self.assertEqual(doc[3].text,"Anna")
        self.assertEqual(doc[4].text,".")

        self.assertEqual(doc[5].text,"Ich")
        self.assertEqual(doc[6].text,"komme")
        self.assertEqual(doc[7].text,"aus")
        self.assertEqual(doc[8].text,"Österreich")
        self.assertEqual(doc[9].text,"und")
        self.assertEqual(doc[10].text,"lebe")
        self.assertEqual(doc[11].text,"seit")
        self.assertEqual(doc[12].text,"drei")

        self.assertEqual(doc[13].text,"Jahren")
        self.assertEqual(doc[14].text,"in")
        self.assertEqual(doc[15].text,"Deutschland")
        self.assertEqual(doc[16].text,".")

        self.assertEqual(len(doc),17)


