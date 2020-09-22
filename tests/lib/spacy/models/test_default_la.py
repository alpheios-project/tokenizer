import unittest
from unittest import TestCase
from tokenizer.lib.spacy.models.default import Default
import re


class TestDefault(TestCase):
    """ Tests for default model with Latin Language """

    def setUp(self):
        model = Default()
        self.nlp = model.load_model(lang="la",config={})

    def tearDown(self):
        pass

    def testEntities(self):
        txt = "&amp; &quot; &apos; &gt; &lt; ;"
        doc = self.nlp(txt)
        self.assertEqual(len(doc),6)

    def test_nec(self):
        doc = self.nlp("sine qua nec intelligi quidquam")
        self.assertEqual(len(doc),6)
        self.assertEqual(doc[2].text,'ne')
        self.assertEqual(doc[3].text,'c')
        doc = self.nlp("sine qua foonec intelligi quidquam")
        self.assertEqual(len(doc),5)
        self.assertEqual(doc[2].text,'foonec')

    def test_neu(self):
        doc = self.nlp("domino, neu quid dominum celauisse")
        self.assertEqual(len(doc),7)
        self.assertEqual(doc[2].text,'ne')
        self.assertEqual(doc[3].text,'u')
        doc = self.nlp("domino, fooneu quid dominum celauisse")
        self.assertEqual(len(doc),6)
        self.assertEqual(doc[2].text,'fooneu')

    def test_seu(self):
        doc = self.nlp("si irati seu cui propitii sunt")
        self.assertEqual(len(doc),7)
        self.assertEqual(doc[2].text,'se')
        self.assertEqual(doc[3].text,'u')
        doc = self.nlp("si irati fooseu cui propitii sunt")
        self.assertEqual(len(doc),6)
        self.assertEqual(doc[2].text,'fooseu')


    def test_nisi(self):
        doc = self.nlp("Nísi quidem qui sése malit púgnitus pessúm dari")
        self.assertEqual(len(doc),9)
        self.assertEqual(doc[0].text,'Ní')
        self.assertEqual(doc[1].text,'si')
        doc = self.nlp("fooNísi quidem qui sése malit púgnitus pessúm dari")
        self.assertEqual(len(doc),8)
        self.assertEqual(doc[0].text,'fooNísi')

    def test_que_enclytic(self):
        txt = 'M. Cicero pecūniam gaudĭămque incolīs dabit.'
        split = [
          "laetusque",
          "eoque",
          "eamque",
          "easque",
          "neque",
          "Neque",
          "altusque",
          "gaudĭămque"
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
            doc = self.nlp(example)
            self.assertEqual(len(doc),2)
        for example in no_split:
            doc = self.nlp(example)
            self.assertEqual(len(doc),1)

    def testAbbrevName(self):
        doc = self.nlp("C. Caesar Antoniusque ratione superavit.")
        self.assertEqual(doc[0].text,"C.")
        self.assertEqual(len(doc),7)

    def testParensVariAndDagger(self):
        txt = "<Marcus> (et Claudius) †amici† [sunt]."
        doc = self.nlp(txt)
        #self.assertEqual(len(doc),14)
        tokens = list(map(lambda t: t.text, doc))
        self.assertEqual(tokens,['<' ,'Marcus', '>', '(', 'et', 'Claudius', ')', '†', 'amici', '†', '[', 'sunt', ']', '.' ])

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



