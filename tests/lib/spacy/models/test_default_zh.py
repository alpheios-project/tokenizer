import unittest
from unittest import TestCase
from tokenizer.lib.spacy.models.default import Default
import re


class TestDefault(TestCase):
    """ Tests for default model with Ancient Greek Language """

    def setUp(self):
        model = Default()
        self.nlp = model.load_model(lang="zh",config={})

    def tearDown(self):
        pass

    def testChineseTokens(self):
        txt = "有子曰："
        doc = self.nlp(txt)
        self.assertEqual(doc[0].text,"有子")
        self.assertEqual(doc[1].text,"曰")
        self.assertEqual(doc[2].text,"：")
        self.assertEqual(len(doc),3)


