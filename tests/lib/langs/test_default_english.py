import unittest
from unittest import TestCase
from tokenizer.lib.spacy.models.default import Default
import re
import os

class TestEnglishDefault(TestCase):

    def setUp(self):
        model = Default()
        self.nlp = model.load_model(lang="eng",config={})

    def tearDown(self):
        pass

    def readFixture(self, type=None, name=None):
        fixture = os.path.join('tests', 'fixtures', type, name)
        with open(fixture, 'r', encoding="utf-8") as (stream):
            text = stream.read()
        return text

    def testCatalanTokens(self):
        text = self.readFixture(type='langs', name='english.txt')
        doc = self.nlp(text)
        # I live in a house near the mountains. I have two brothers and one sister, and I was born last. I don't know.

        self.assertEqual(doc[0].text,"I")
        self.assertEqual(doc[1].text,"live")
        self.assertEqual(doc[2].text,"in")
        self.assertEqual(doc[3].text,"a")
        self.assertEqual(doc[4].text,"house")
        self.assertEqual(doc[5].text,"near")
        self.assertEqual(doc[6].text,"the")
        self.assertEqual(doc[7].text,"mountains")
        self.assertEqual(doc[8].text,".")

        self.assertEqual(doc[9].text,"I")
        self.assertEqual(doc[10].text,"have")
        self.assertEqual(doc[11].text,"two")
        self.assertEqual(doc[12].text,"brothers")
        self.assertEqual(doc[13].text,"and")
        self.assertEqual(doc[14].text,"one")
        self.assertEqual(doc[15].text,"sister")
        self.assertEqual(doc[16].text,",")

        self.assertEqual(doc[17].text,"and")
        self.assertEqual(doc[18].text,"I")
        self.assertEqual(doc[19].text,"was")
        self.assertEqual(doc[20].text,"born")
        self.assertEqual(doc[21].text,"last")
        self.assertEqual(doc[22].text,".")

        self.assertEqual(doc[23].text,"I")
        self.assertEqual(doc[24].text,"do")
        self.assertEqual(doc[25].text,"n't")
        self.assertEqual(doc[26].text,"know")
        self.assertEqual(doc[27].text,".")

        self.assertEqual(len(doc),28)


