import unittest
from unittest import TestCase
from tokenizer.lib.spacy.models.default import Default
import re
import os

class TestVietnameseDefault(TestCase):

    def setUp(self):
        model = Default()
        self.nlp = model.load_model(lang="vie",config={})

    def tearDown(self):
        pass

    def readFixture(self, type=None, name=None):
        fixture = os.path.join('tests', 'fixtures', type, name)
        with open(fixture, 'r', encoding="utf-8") as (stream):
            text = stream.read()
        return text

    def testCatalanTokens(self):
        text = self.readFixture(type='langs', name='vietnamese.txt')
        doc = self.nlp(text)
        # Kỳ nghỉ tuyệt vời, khách sạn, bãi biển và nhà hàng gần biển tiện ích và sạch sẽ,

        self.assertEqual(doc[0].text,"Kỳ")
        self.assertEqual(doc[1].text,"nghỉ")
        self.assertEqual(doc[2].text,"tuyệt vời")
        self.assertEqual(doc[3].text,",")

        self.assertEqual(doc[4].text,"khách sạn")
        self.assertEqual(doc[5].text,",")
        self.assertEqual(doc[6].text,"bãi")

        self.assertEqual(doc[7].text,"biển")
        self.assertEqual(doc[8].text,"và")
        self.assertEqual(doc[9].text,"nhà hàng")

        self.assertEqual(doc[10].text,"gần")
        self.assertEqual(doc[11].text,"biển")
        self.assertEqual(doc[12].text,"tiện ích")
        self.assertEqual(doc[13].text,"và")

        self.assertEqual(doc[14].text,"sạch sẽ")

        self.assertEqual(doc[15].text,",")

        self.assertEqual(len(doc),16)


