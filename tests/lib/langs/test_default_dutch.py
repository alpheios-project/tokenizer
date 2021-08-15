import unittest
from unittest import TestCase
from tokenizer.lib.spacy.models.default import Default
import re
import os

class TestDutchDefault(TestCase):

    def setUp(self):
        model = Default()
        self.nlp = model.load_model(lang="nld",config={})

    def tearDown(self):
        pass

    def readFixture(self, type=None, name=None):
        fixture = os.path.join('tests', 'fixtures', type, name)
        with open(fixture, 'r', encoding="utf-8") as (stream):
            text = stream.read()
        return text

    def testCatalanTokens(self):
        text = self.readFixture(type='langs', name='dutch.txt')
        doc = self.nlp(text)
        # Hallo Marsel, Wat leuk om jou eindelijk weer eens te schrijven. Ik heb je lang niet gezien.

        self.assertEqual(doc[0].text,"Hallo")
        self.assertEqual(doc[1].text,"Marsel")
        self.assertEqual(doc[2].text,",")

        self.assertEqual(doc[3].text,"Wat")
        self.assertEqual(doc[4].text,"leuk")
        self.assertEqual(doc[5].text,"om")
        self.assertEqual(doc[6].text,"jou")
        self.assertEqual(doc[7].text,"eindelijk")
        self.assertEqual(doc[8].text,"weer")
        self.assertEqual(doc[9].text,"eens")
        self.assertEqual(doc[10].text,"te")
        self.assertEqual(doc[11].text,"schrijven")
        self.assertEqual(doc[12].text,".")

        self.assertEqual(doc[13].text,"Ik")
        self.assertEqual(doc[14].text,"heb")
        self.assertEqual(doc[15].text,"je")
        self.assertEqual(doc[16].text,"lang")
        self.assertEqual(doc[17].text,"niet")
        self.assertEqual(doc[18].text,"gezien")
        self.assertEqual(doc[19].text,".")

        self.assertEqual(len(doc),20)


