import unittest
from unittest import TestCase
from tokenizer.lib.spacy.models.default import Default
import re


class TestDefault(TestCase):

    def setUp(self):
        model = Default()
        self.nlp = model.load_model(lang="grc",config={})

    def tearDown(self):
        pass

    def testEntities(self):
        txt = "&amp; &quot; &apos; &gt; &lt; ;"
        doc = self.nlp(txt)
        self.assertEqual(len(doc),6)

    def testBasicGreek(self):
        txt = "καὶ διὰ τῆς περὶ τὴν ἀρχαιολογίαν συγγραφῆς."
        doc = self.nlp(txt)
        self.assertEqual(len(doc),8)

    def testHandlesApostrophe(self):
        txt = "εὖ δ᾽ ἴστε."
        doc = self.nlp(txt)
        self.assertEqual(len(doc),4)

    def testSplitOnApostrophe(self):
        txt = "εὖ δ᾽ἴστε."
        doc = self.nlp(txt)
        self.assertEqual(len(doc),4)

    def testSplitsKrasis(self):
        txt = "κἄπειτα."
        doc = self.nlp(txt)
        self.assertEqual(len(doc),3)
        self.assertEqual(doc[0].text,"κ")
        self.assertEqual(doc[1].text,"ἄπειτα")

    def testSplitsKrasisDipthong(self):
        txt = "τοὔνομα."
        doc = self.nlp(txt)
        self.assertEqual(len(doc),3)
        self.assertEqual(doc[0].text,"τ")

    def testSplitsMultipleKrasis(self):
        txt = "κἄπειτα τῆς περὶ τὴν ἀρχαιολογίαν κἄπειτα."
        doc = self.nlp(txt)
        self.assertEqual(len(doc),9)
        self.assertEqual(doc[2].text, "τῆς")
        self.assertEqual(doc[8].text, ".")


