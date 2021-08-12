import unittest
from unittest import TestCase
from tokenizer.lib.spacy.models.default import Default
import re
import os

class TestCatalanDefault(TestCase):

    def setUp(self):
        model = Default()
        self.nlp = model.load_model(lang="cat",config={})

    def tearDown(self):
        pass

    def readFixture(self, type=None, name=None):
        fixture = os.path.join('tests', 'fixtures', type, name)
        with open(fixture, 'r', encoding="utf-8") as (stream):
            text = stream.read()
        return text

    def testCatalanTokens(self):
        text = self.readFixture(type='langs', name='catalan.txt')
        doc = self.nlp(text)
        # Tota persona té dret a l'educació. L'educació serà gratuïta, si més no, en la instrucció elemental i fonamental. 
        
        self.assertEqual(doc[0].text,"Tota")
        self.assertEqual(doc[1].text,"persona")
        self.assertEqual(doc[2].text,"té")
        self.assertEqual(doc[3].text,"dret")

        self.assertEqual(doc[4].text,"a")
        self.assertEqual(doc[5].text,"l'")
        self.assertEqual(doc[6].text,"educació")
        self.assertEqual(doc[7].text,".")

        self.assertEqual(doc[8].text,"L'")
        self.assertEqual(doc[9].text,"educació")
        self.assertEqual(doc[10].text,"serà")
        self.assertEqual(doc[11].text,"gratuïta")
        self.assertEqual(doc[12].text,",")

        self.assertEqual(doc[13].text,"si")
        self.assertEqual(doc[14].text,"més")
        self.assertEqual(doc[15].text,"no")
        self.assertEqual(doc[16].text,",")

        self.assertEqual(doc[17].text,"en")
        self.assertEqual(doc[18].text,"la")
        self.assertEqual(doc[19].text,"instrucció")
        self.assertEqual(doc[20].text,"elemental")

        self.assertEqual(doc[21].text,"i")
        self.assertEqual(doc[22].text,"fonamental")
        self.assertEqual(doc[23].text,".")

        self.assertEqual(len(doc),24)


