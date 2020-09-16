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

    def testSplit(self):
        config = {}
        config[Latin.SPLIT_ENCLYTICS] = 1
        nlp = self.model.load_model(config=config)
        txt = 'M. Cicero pecūniam gaudĭămque incolīs dabit.'
        doc = nlp(txt)
        self.assertEqual(len(doc),9)

        with doc.retokenize() as retokenizer:
            for token in doc:
                p = re.compile(r'que$')
                match = p.match(token.text)
                if match:
                    retokenizer.merge(doc[token.i-1:token.i+1])
        self.assertEqual(len(doc),8)




