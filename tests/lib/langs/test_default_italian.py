import unittest
from unittest import TestCase
from tokenizer.lib.spacy.models.default import Default
import re
import os

class TestItalianDefault(TestCase):

    def setUp(self):
        model = Default()
        self.nlp = model.load_model(lang="ita",config={})

    def tearDown(self):
        pass

    def readFixture(self, type=None, name=None):
        fixture = os.path.join('tests', 'fixtures', type, name)
        with open(fixture, 'r', encoding="utf-8") as (stream):
            text = stream.read()
        return text

    def testCatalanTokens(self):
        text = self.readFixture(type='langs', name='italian.txt')
        doc = self.nlp(text)
        # I nostri figli, Manuela che ha diciassette anni, e Marco che ha quindici anni, e poi c'è anche Tremendo,
        # il cane che vive con noi da nove anni, ed è parte della famiglia.

        self.assertEqual(doc[0].text,"I")
        self.assertEqual(doc[1].text,"nostri")
        self.assertEqual(doc[2].text,"figli")
        self.assertEqual(doc[3].text,",")

        self.assertEqual(doc[4].text,"Manuela")
        self.assertEqual(doc[5].text,"che")
        self.assertEqual(doc[6].text,"ha")
        self.assertEqual(doc[7].text,"diciassette")
        self.assertEqual(doc[8].text,"anni")
        self.assertEqual(doc[9].text,",")

        self.assertEqual(doc[10].text,"e")
        self.assertEqual(doc[11].text,"Marco")
        self.assertEqual(doc[12].text,"che")
        self.assertEqual(doc[13].text,"ha")
        self.assertEqual(doc[14].text,"quindici")
        self.assertEqual(doc[15].text,"anni")
        self.assertEqual(doc[16].text,",")

        self.assertEqual(doc[17].text,"e")
        self.assertEqual(doc[18].text,"poi")
        self.assertEqual(doc[19].text,"c'")
        self.assertEqual(doc[20].text,"è")
        self.assertEqual(doc[21].text,"anche")
        self.assertEqual(doc[22].text,"Tremendo")
        self.assertEqual(doc[23].text,",")

        self.assertEqual(doc[24].text,"il")
        self.assertEqual(doc[25].text,"cane")
        self.assertEqual(doc[26].text,"che")
        self.assertEqual(doc[27].text,"vive")
        self.assertEqual(doc[28].text,"con")
        self.assertEqual(doc[29].text,"noi")
        self.assertEqual(doc[30].text,"da")

        self.assertEqual(doc[31].text,"nove")
        self.assertEqual(doc[32].text,"anni")
        self.assertEqual(doc[33].text,",")
        self.assertEqual(doc[34].text,"ed")
        self.assertEqual(doc[35].text,"è")
        self.assertEqual(doc[36].text,"parte")
        self.assertEqual(doc[37].text,"della")
        self.assertEqual(doc[38].text,"famiglia")
        self.assertEqual(doc[39].text,".")

        self.assertEqual(len(doc),40)


