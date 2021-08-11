import unittest
from unittest import TestCase
from tokenizer.lib.spacy.models.default import Default
import re
import os

class TestDanishDefault(TestCase):

    def setUp(self):
        model = Default()
        self.nlp = model.load_model(lang="dan",config={})

    def tearDown(self):
        pass

    def readFixture(self, type=None, name=None):
        fixture = os.path.join('tests', 'fixtures', type, name)
        print(fixture)
        with open(fixture, 'r', encoding="utf-8") as (stream):
            text = stream.read()
        return text

    def testCatalanTokens(self):
        text = self.readFixture(type='langs', name='danish.txt')
        doc = self.nlp(text)
        # Maria er 20 år og bor i København. Maria har en hund. Hunden hedder Siko.

        self.assertEqual(doc[0].text,"Maria")
        self.assertEqual(doc[1].text,"er")
        self.assertEqual(doc[2].text,"20")
        self.assertEqual(doc[3].text,"år")
        self.assertEqual(doc[4].text,"og")
        self.assertEqual(doc[5].text,"bor")

        self.assertEqual(doc[6].text,"i")
        self.assertEqual(doc[7].text,"København")
        self.assertEqual(doc[8].text,".")
        self.assertEqual(doc[9].text,"Maria")
        self.assertEqual(doc[10].text,"har")
        self.assertEqual(doc[11].text,"en")
        self.assertEqual(doc[12].text,"hund")
        self.assertEqual(doc[13].text,".")

        self.assertEqual(doc[14].text,"Hunden")
        self.assertEqual(doc[15].text,"hedder")
        self.assertEqual(doc[16].text,"Siko")
        self.assertEqual(doc[17].text,".")

        self.assertEqual(len(doc),18)


