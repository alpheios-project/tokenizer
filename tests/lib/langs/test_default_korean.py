import unittest
from unittest import TestCase
from tokenizer.lib.spacy.models.default import Default
import re
import os

class TestKoreanDefault(TestCase):

    def setUp(self):
        model = Default()
        self.nlp = model.load_model(lang="kor",config={})

    def tearDown(self):
        pass

    def readFixture(self, type=None, name=None):
        fixture = os.path.join('tests', 'fixtures', type, name)
        with open(fixture, 'r', encoding="utf-8") as (stream):
            text = stream.read()
        return text
"""
    def testCatalanTokens(self):
        text = self.readFixture(type='langs', name='korean.txt')
        doc = self.nlp(text)
        # 모든 사람은 교육을 받을 권리를 가진다.

        self.assertEqual(doc[0].text,"모든")
        self.assertEqual(doc[1].text,"사람은")
        self.assertEqual(doc[2].text,"교육을")
        self.assertEqual(doc[3].text,"받을")

        self.assertEqual(doc[4].text,"권리를")
        self.assertEqual(doc[5].text,"가진다")
        self.assertEqual(doc[6].text,".")

        self.assertEqual(len(doc),7)
"""

