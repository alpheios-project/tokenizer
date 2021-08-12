import unittest
from unittest import TestCase
from tokenizer.lib.spacy.models.default import Default
import re
import os

class TestFrenchDefault(TestCase):

    def setUp(self):
        model = Default()
        self.nlp = model.load_model(lang="fra",config={})

    def tearDown(self):
        pass

    def readFixture(self, type=None, name=None):
        fixture = os.path.join('tests', 'fixtures', type, name)
        with open(fixture, 'r', encoding="utf-8") as (stream):
            text = stream.read()
        return text

    def testCatalanTokens(self):
        text = self.readFixture(type='langs', name='french.txt')
        doc = self.nlp(text)
        # Je m’appelle Jessica. Je suis une fille, je suis française et j’ai treize ans.

        self.assertEqual(doc[0].text,"Je")
        self.assertEqual(doc[1].text,"m’")
        self.assertEqual(doc[2].text,"appelle")
        self.assertEqual(doc[3].text,"Jessica")
        self.assertEqual(doc[4].text,".")

        self.assertEqual(doc[5].text,"Je")
        self.assertEqual(doc[6].text,"suis")
        self.assertEqual(doc[7].text,"une")
        self.assertEqual(doc[8].text,"fille")
        self.assertEqual(doc[9].text,",")

        self.assertEqual(doc[10].text,"je")
        self.assertEqual(doc[11].text,"suis")
        self.assertEqual(doc[12].text,"française")
        self.assertEqual(doc[13].text,"et")
        self.assertEqual(doc[14].text,"j’")
        self.assertEqual(doc[15].text,"ai")
        self.assertEqual(doc[16].text,"treize")
        self.assertEqual(doc[17].text,"ans")
        self.assertEqual(doc[18].text,".")

        self.assertEqual(len(doc),19)


