import unittest
from unittest import TestCase
from tokenizer.lib.spacy.models.default import Default
import re
import os

class TestJapaneseDefault(TestCase):

    def setUp(self):
        model = Default()
        self.nlp = model.load_model(lang="jpn",config={})

    def tearDown(self):
        pass

    def readFixture(self, type=None, name=None):
        fixture = os.path.join('tests', 'fixtures', type, name)
        print(fixture)
        with open(fixture, 'r', encoding="utf-8") as (stream):
            text = stream.read()
        return text

    def testCatalanTokens(self):
        text = self.readFixture(type='langs', name='japanese.txt')
        doc = self.nlp(text)
        # 日本人で、新型コロナウイルス感染症の。

        self.assertEqual(doc[0].text,"日本")
        self.assertEqual(doc[1].text,"人")
        self.assertEqual(doc[2].text,"で")
        self.assertEqual(doc[3].text,"、")

        self.assertEqual(doc[4].text,"新型")
        self.assertEqual(doc[5].text,"コロナ")
        self.assertEqual(doc[6].text,"ウイルス")
        self.assertEqual(doc[7].text,"感染")
        self.assertEqual(doc[8].text,"症")
        self.assertEqual(doc[9].text,"の")

        self.assertEqual(doc[10].text,"。")

        self.assertEqual(len(doc),11)


