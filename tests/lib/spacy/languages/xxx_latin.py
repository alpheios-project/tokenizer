import unittest
from unittest import TestCase
from tokenizer.lib.spacy.models.latin import Latin
import re


class TestLatin(TestCase):

    def setUp(self):
        self.model = Latin()
        self.nlp = self.model.load_model(config={})

    def tearDown(self):
        pass

    def testPeriod(self):
        doc = self.nlp("C. Caesar Antoniusque ratione superavit.")
        self.assertEqual(len(doc),7)

    def testParens(self):
        txt = "<Marcus> (et Claudius) †amici† [sunt]."
        doc = self.nlp(txt)
        self.assertEqual(len(doc),14)
        tokens = list(map(lambda t: t.text, doc))
        self.assertEqual(tokens,['<' ,'Marcus', '>', '(', 'et', 'Claudius', ')', '†', 'amici', '†', '[', 'sunt', ']', '.' ])

    def testEntities(self):
        txt = "&amp; &quot; &apos; &gt; &lt; ;"
        doc = self.nlp(txt)
        self.assertEqual(len(doc),6)

    def testAbbr(self):
        txt = "M. Cicero et Marcus aimici sunt."
        doc = self.nlp(txt)
        self.assertEqual(len(doc),6)

    def testSplit(self):
        config = {}
        config[Latin.SPLIT_ENCLYTICS] = 1
        nlp = self.model.load_model(config=config)
        txt = 'M. Cicero pecūniam gaudĭămque incolīs dabit.'
        split = [
          "laetusque",
          "eoque",
          "eamque",
          "easque",
          "neque",
          "Neque",
          "nec",
          "Nec",
          "altusque"
        ]
        no_split = [
          "Atque",
          "atque",
          "cuiusque",
          "denique",
          "itaque",
          "plerumque",
          "plerosque",
          "plerique",
          "plerarumque",
          "quaque",
          "quemque",
          "undique",
          "uterque",
          "utriusque",
          "utcumque",
          "usque",
          "quantumcumque",
          "quantulacumque",
          "unusquisque",
          "quisque",
          "quaeque",
          "uniuscuiusque",
        ]
        for example in split:
            doc = nlp(example)
            self.model.retokenize(doc=doc,config=config)
            self.assertEqual(len(doc),2)
        for example in no_split:
            doc = nlp(example)
            self.assertEqual(len(doc),2)
            self.model.retokenize(doc=doc,config=config)
            self.assertEqual(len(doc),1)




