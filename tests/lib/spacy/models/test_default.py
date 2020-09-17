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
        self.assertEqual(len(doc),6)



