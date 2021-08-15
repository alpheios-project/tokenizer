import unittest
from unittest import TestCase
from tokenizer.lib.spacy.models.default import Default
import re
import os

class TestLatinDefault(TestCase):

    def setUp(self):
        model = Default()
        self.nlp = model.load_model(lang="lat",config={})

    def tearDown(self):
        pass

    def readFixture(self, type=None, name=None):
        fixture = os.path.join('tests', 'fixtures', type, name)
        with open(fixture, 'r', encoding="utf-8") as (stream):
            text = stream.read()
        return text

    def testCatalanTokens(self):
        text = self.readFixture(type='langs', name='latin.txt')
        doc = self.nlp(text)
        # Suave, mari magno turbantibus aequora ventis
        # e terra magnum alterius spectare laborem;

        self.assertEqual(doc[0].text,"Suave")
        self.assertEqual(doc[1].text,",")
        self.assertEqual(doc[2].text,"mari")
        self.assertEqual(doc[3].text,"magno")

        self.assertEqual(doc[4].text,"turbantibus")
        self.assertEqual(doc[5].text,"aequora")
        self.assertEqual(doc[6].text,"ventis")
        self.assertEqual(doc[7].text,"e")
        self.assertEqual(doc[8].text,"terra")
        self.assertEqual(doc[9].text,"magnum")

        self.assertEqual(doc[10].text,"alterius")
        self.assertEqual(doc[11].text,"spectare")
        self.assertEqual(doc[12].text,"laborem")
        self.assertEqual(doc[13].text,";")

        self.assertEqual(len(doc),14)


