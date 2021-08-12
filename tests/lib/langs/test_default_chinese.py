import unittest
from unittest import TestCase
from tokenizer.lib.spacy.models.default import Default
import re
import os

class TestChineseDefault(TestCase):

    def setUp(self):
        model = Default()
        self.nlp = model.load_model(lang="zho",config={})

    def tearDown(self):
        pass

    def readFixture(self, type=None, name=None):
        fixture = os.path.join('tests', 'fixtures', type, name)
        with open(fixture, 'r', encoding="utf-8") as (stream):
            text = stream.read()
        return text

    def testCatalanTokens(self):
        text = self.readFixture(type='langs', name='chinese.txt')
        doc = self.nlp(text)
        # 先晉獻之卒，齊桓為葵丘之會，

        self.assertEqual(doc[0].text,"先")
        self.assertEqual(doc[1].text,"晉")
        self.assertEqual(doc[2].text,"獻")
        self.assertEqual(doc[3].text,"之")
        self.assertEqual(doc[4].text,"卒")
        self.assertEqual(doc[5].text,"，")

        self.assertEqual(doc[6].text,"齊")
        self.assertEqual(doc[7].text,"桓")
        self.assertEqual(doc[8].text,"為")
        self.assertEqual(doc[9].text,"葵")
        self.assertEqual(doc[10].text,"丘")
        self.assertEqual(doc[11].text,"之")
        self.assertEqual(doc[12].text,"會")
        self.assertEqual(doc[13].text,"，")

        self.assertEqual(len(doc),14)


