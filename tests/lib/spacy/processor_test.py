import unittest
from unittest import TestCase
from tokenizer.lib.spacy.processor import Processor
import os

class ProcessorTest(TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def readFixture(self, type=None, lang=None, name=None):
        fixture = os.path.join('tests', 'fixtures', type, lang, name)
        with open(fixture, 'r', encoding="utf-8") as (stream):
            text = stream.read()
        return text

    def test_props(self):
        text = self.readFixture(type='text', lang='lat', name='singleseg.csv')
        processor = Processor(config=None)
        tokenized = processor.tokenize(text=text, lang='lat')
        segment = tokenized[0]
        self.assertEqual(segment['index'],0)
        self.assertEqual(segment['tb_sent'],'')
        token = tokenized[0]['tokens'][0]
        self.assertEqual(token['text'],'In')
        self.assertFalse(token['start_sent'])
        self.assertFalse(token['is_punct'])
        self.assertFalse(token['lb_before'])
        self.assertEqual(token['tb_word'],'')
        self.assertEqual(token['index'],0)
        self.assertEqual(token['docIndex'],0)

    def test_tokenize_singleseg(self):
        text = self.readFixture(type='text', lang='lat', name='singleseg.csv')
        processor = Processor(config=None)
        tokenized = processor.tokenize(text=text, lang='lat')
        self.assertEqual(len(tokenized),1)
        self.assertEqual(len(tokenized[0]['tokens']),32)
        self.assertFalse(tokenized[0]['tokens'][0]['start_sent'])
        self.assertEqual(tokenized[0]['tokens'][0]['index'],0)
        self.assertEqual(tokenized[0]['tokens'][0]['docIndex'],0)
        self.assertEqual(tokenized[0]['tokens'][6]['text'],'formas')
        self.assertFalse(tokenized[0]['tokens'][6]['lb_before'])
        self.assertEqual(tokenized[0]['tokens'][7]['text'],'corpora')
        self.assertTrue(tokenized[0]['tokens'][7]['lb_before'])

    def test_tokenize_singlesegsent(self):
        text = self.readFixture(type='text', lang='lat', name='singleseg.csv')
        processor = Processor(config=None)
        tokenized = processor.tokenize(text=text, lang='lat', sentencize=True)
        self.assertEqual(len(tokenized),1)
        self.assertEqual(len(tokenized[0]['tokens']),32)
        self.assertTrue(tokenized[0]['tokens'][0]['start_sent'])
        self.assertTrue(tokenized[0]['tokens'][9]['start_sent'])
        self.assertEqual(tokenized[0]['tokens'][6]['text'],'formas')
        self.assertFalse(tokenized[0]['tokens'][6]['lb_before'])
        self.assertEqual(tokenized[0]['tokens'][7]['text'],'corpora')
        self.assertTrue(tokenized[0]['tokens'][7]['lb_before'])

    def test_tokenize_lineseg(self):
        text = self.readFixture(type='text', lang='lat', name='lineseg.csv')
        processor = Processor(config=None)
        tokenized = processor.tokenize(text=text, lang='lat', segon='singleline')
        self.assertEqual(len(tokenized),20)
        self.assertEqual(len(tokenized[0]['tokens']),7)
        self.assertEqual(len(tokenized[19]['tokens']),9)
        self.assertFalse(tokenized[0]['tokens'][0]['start_sent'])
        self.assertFalse(tokenized[0]['tokens'][-1]['lb_before'])
        self.assertEqual(tokenized[1]['tokens'][0]['index'],0)
        self.assertEqual(tokenized[1]['tokens'][0]['docIndex'],8)
        self.assertTrue(tokenized[1]['tokens'][0]['lb_before'])

    def test_tokenize_linesegsent(self):
        text = self.readFixture(type='text', lang='lat', name='lineseg.csv')
        processor = Processor(config=None)
        tokenized = processor.tokenize(text=text, lang='lat', segon='singleline', sentencize=True)
        self.assertEqual(len(tokenized),20)
        self.assertEqual(len(tokenized[0]['tokens']),7)
        self.assertEqual(len(tokenized[19]['tokens']),9)
        self.assertTrue(tokenized[0]['tokens'][0]['start_sent'])
        self.assertTrue(tokenized[1]['tokens'][2]['start_sent'])

    def test_tokenize_linesegsenttbsent(self):
        text = self.readFixture(type='text', lang='lat', name='lineseg.csv')
        processor = Processor(config=None)
        tokenized = processor.tokenize(text=text, lang='lat', segon='singleline', sentencize=True, tbseg=True, segstart=1)
        self.assertEqual(len(tokenized),20)
        self.assertTrue(tokenized[0]['tb_sent'],1)
        self.assertTrue(tokenized[1]['tb_sent'],2)

    def test_tokenize_doublelineseg(self):
        text = self.readFixture(type='text', lang='lat', name='doublelineseg.csv')
        processor = Processor(config=None)
        tokenized = processor.tokenize(text=text, lang='lat', segon='doubleline')
        self.assertEqual(len(tokenized),2)
        self.assertEqual(tokenized[1]['tokens'][0]['text'],'nullus')
        self.assertTrue(tokenized[1]['tokens'][0]['lb_before'])

    def test_tokenize_linesegcustomtb(self):
        text = self.readFixture(type='text', lang='lat', name='linesegtb.csv')
        processor = Processor(config=None)
        tokenized = processor.tokenize(text=text, lang='lat', segon='singleline', sentencize=True, tbseg=False, segstart=1)
        self.assertEqual(len(tokenized),3)
        self.assertTrue(tokenized[0]['tb_sent'],10)
        self.assertTrue(tokenized[0]['index'],0)
        self.assertTrue(tokenized[1]['tb_sent'],11)
        self.assertTrue(tokenized[0]['index'],1)
        self.assertTrue(tokenized[1]['tb_sent'],12)
        self.assertTrue(tokenized[0]['index'],2)



if __name__ == '__main__':
  unittest.main()