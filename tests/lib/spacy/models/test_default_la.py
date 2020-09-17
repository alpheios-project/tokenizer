import unittest
from unittest import TestCase
from tokenizer.lib.spacy.models.default import Default
import re


class TestDefault(TestCase):

    def setUp(self):
        model = Default()
        self.nlp = model.load_model(lang="la",config={})

    def tearDown(self):
        pass

    def test_nec(self):
        doc = self.nlp("sine qua nec intelligi quidquam")
        self.assertEqual(len(doc),6)
        self.assertEqual(doc[2].text,'ne')
        self.assertEqual(doc[3].text,'c')

    def test_nese(self):
        doc = self.nlp("Cum Nese ante alias facie praestantior")
        self.assertEqual(len(doc),7)
        self.assertEqual(doc[1].text,'Ne')
        self.assertEqual(doc[2].text,'se')

    def test_nisi(self):
        doc = self.nlp("Nísi quidem qui sése malit púgnitus pessúm dari")
        self.assertEqual(len(doc),9)
        self.assertEqual(doc[0].text,'Ní')
        self.assertEqual(doc[1].text,'si')

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




