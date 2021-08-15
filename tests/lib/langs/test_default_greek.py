import unittest
from unittest import TestCase
from tokenizer.lib.spacy.models.default import Default
import re
import os

class TestGreekDefault(TestCase):

    def setUp(self):
        model = Default()
        self.nlp = model.load_model(lang="grc",config={})

    def tearDown(self):
        pass

    def readFixture(self, type=None, name=None):
        fixture = os.path.join('tests', 'fixtures', type, name)
        with open(fixture, 'r', encoding="utf-8") as (stream):
            text = stream.read()
        return text

    def testCatalanTokens(self):
        text = self.readFixture(type='langs', name='greek.txt')
        doc = self.nlp(text)
        # Τί νεώτερον, ὦ Σώκρατες, γέγονεν, ὅτι σὺ τὰς ἐν Λυκείωι καταλιπὼν διατριβὰς ἐνθάδε νῦν διατρίβεις περὶ τὴν τοῦ βασιλέως στοάν;

        self.assertEqual(doc[0].text,"Τί")
        self.assertEqual(doc[1].text,"νεώτερον")
        self.assertEqual(doc[2].text,",")
        self.assertEqual(doc[3].text,"ὦ")
        self.assertEqual(doc[4].text,"Σώκρατες")
        self.assertEqual(doc[5].text,",")
        self.assertEqual(doc[6].text,"γέγονεν")
        self.assertEqual(doc[7].text,",")
        self.assertEqual(doc[8].text,"ὅτι")

        self.assertEqual(doc[9].text,"σὺ")
        self.assertEqual(doc[10].text,"τὰς")
        self.assertEqual(doc[11].text,"ἐν")
        self.assertEqual(doc[12].text,"Λυκείωι")
        self.assertEqual(doc[13].text,"καταλιπὼν")
        self.assertEqual(doc[14].text,"διατριβὰς")
        self.assertEqual(doc[15].text,"ἐνθάδε")
        self.assertEqual(doc[16].text,"νῦν")

        self.assertEqual(doc[17].text,"διατρίβεις")
        self.assertEqual(doc[18].text,"περὶ")
        self.assertEqual(doc[19].text,"τὴν")
        self.assertEqual(doc[20].text,"τοῦ")
        self.assertEqual(doc[21].text,"βασιλέως")
        self.assertEqual(doc[22].text,"στοάν")

        self.assertEqual(doc[23].text,";")

        self.assertEqual(len(doc),24)


