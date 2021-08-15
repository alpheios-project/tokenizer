import unittest
from unittest import TestCase
from tokenizer.lib.spacy.models.default import Default
import re
import os

class TestRussianDefault(TestCase):

    def setUp(self):
        model = Default()
        self.nlp = model.load_model(lang="rus",config={})

    def tearDown(self):
        pass

    def readFixture(self, type=None, name=None):
        fixture = os.path.join('tests', 'fixtures', type, name)
        with open(fixture, 'r', encoding="utf-8") as (stream):
            text = stream.read()
        return text

    def testCatalanTokens(self):
        text = self.readFixture(type='langs', name='russian.txt')
        doc = self.nlp(text)
        # В Минобрнауки могут изменить рекомендации какие-нибудь по вакцинации российских студентов от COVID-19.

        self.assertEqual(doc[0].text,"В")
        self.assertEqual(doc[1].text,"Минобрнауки")
        self.assertEqual(doc[2].text,"могут")
        self.assertEqual(doc[3].text,"изменить")

        self.assertEqual(doc[4].text,"рекомендации")
        self.assertEqual(doc[5].text,"какие")
        self.assertEqual(doc[6].text,"-")
        self.assertEqual(doc[7].text,"нибудь")
        self.assertEqual(doc[8].text,"по")
        self.assertEqual(doc[9].text,"вакцинации")
        self.assertEqual(doc[10].text,"российских")
        self.assertEqual(doc[11].text,"студентов")

        self.assertEqual(doc[12].text,"от")
        self.assertEqual(doc[13].text,"COVID-19")
        self.assertEqual(doc[14].text,".")

        self.assertEqual(len(doc),15)


