import unittest
from unittest import TestCase
from tokenizer.lib.spacy.models.default import Default
import re
import os

class TestUkranianDefault(TestCase):

    def setUp(self):
        model = Default()
        self.nlp = model.load_model(lang="ukr",config={})

    def tearDown(self):
        pass

    def readFixture(self, type=None, name=None):
        fixture = os.path.join('tests', 'fixtures', type, name)
        with open(fixture, 'r', encoding="utf-8") as (stream):
            text = stream.read()
        return text

    def testCatalanTokens(self):
        text = self.readFixture(type='langs', name='ukranian.txt')
        doc = self.nlp(text)
        # Готель Panorama De Luxe – унікальне місце в Одесі, де можна відпочити із родиною, відсвяткувати важливий день із друзями та близькими, провести бізнес-захід.

        self.assertEqual(doc[0].text,"Готель")
        self.assertEqual(doc[1].text,"Panorama")
        self.assertEqual(doc[2].text,"De")
        self.assertEqual(doc[3].text,"Luxe")

        self.assertEqual(doc[4].text,"–")
        self.assertEqual(doc[5].text,"унікальне")
        self.assertEqual(doc[6].text,"місце")

        self.assertEqual(doc[7].text,"в")
        self.assertEqual(doc[8].text,"Одесі")
        self.assertEqual(doc[9].text,",")

        self.assertEqual(doc[10].text,"де")
        self.assertEqual(doc[11].text,"можна")
        self.assertEqual(doc[12].text,"відпочити")
        self.assertEqual(doc[13].text,"із")

        self.assertEqual(doc[14].text,"родиною")

        self.assertEqual(doc[15].text,",")

        self.assertEqual(doc[16].text,"відсвяткувати")
        self.assertEqual(doc[17].text,"важливий")
        self.assertEqual(doc[18].text,"день")
        self.assertEqual(doc[19].text,"із")
        self.assertEqual(doc[20].text,"друзями")
        self.assertEqual(doc[21].text,"та")
        self.assertEqual(doc[22].text,"близькими")
        self.assertEqual(doc[23].text,",")
        self.assertEqual(doc[24].text,"провести")
        self.assertEqual(doc[25].text,"бізнес")
        self.assertEqual(doc[26].text,"-")
        self.assertEqual(doc[27].text,"захід")
        self.assertEqual(doc[28].text,".")

        self.assertEqual(len(doc),29)


