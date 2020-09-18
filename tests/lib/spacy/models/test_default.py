import unittest
from unittest import TestCase
from tokenizer.lib.spacy.models.default import Default
import re


class TestDefault(TestCase):

    def setUp(self):
        model = Default()
        self.nlp = model.load_model(lang="xx",config={})

    def tearDown(self):
        pass

    def testPeriod(self):
        doc = self.nlp("C. Caesar Antoniusque ratione superavit.")
        self.assertEqual(doc[0].text,"C.")
        self.assertEqual(len(doc),6)

    def testEntities(self):
        txt = "&amp; &quot; &apos; &gt; &lt; ;"
        doc = self.nlp(txt)

    def testDoubleHyphen(self):
        txt = 'Arma -- virum -- cano.'
        doc = self.nlp(txt)
        self.assertEqual(len(doc),6)

    def testDoublePunc(self):
        txt = 'Arma cano!?'
        doc = self.nlp(txt)
        self.assertEqual(len(doc),4)

    def testDirectSpeech(self):
        txt = "'Arma', inquit 'cano'."
        doc = self.nlp(txt)
        self.assertEqual(len(doc),9)
        txt = '"Arma" inquit "cano".'
        doc = self.nlp(txt)
        self.assertEqual(len(doc),8)
        txt = '”Arma” inquit ”cano”.'
        doc = self.nlp(txt)
        self.assertEqual(len(doc),8)

