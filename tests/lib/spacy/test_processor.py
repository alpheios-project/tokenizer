import unittest
from unittest import TestCase
from tokenizer.lib.spacy.processor import Processor
import os

class ProcessorTest(TestCase):

    def setUp(self):
        self.tbrequestmeta = 'META|TB_SENT_{ALPHEIOS_SEGMENT_INDEX}'
        pass

    def tearDown(self):
        pass

    def readFixture(self, type=None, name=None):
        fixture = os.path.join('tests', 'fixtures', type, name)
        with open(fixture, 'r', encoding="utf-8") as (stream):
            text = stream.read()
        return text

    def test_props(self):
        text = self.readFixture(type='text', name='singleseg.txt')
        processor = Processor(config=None)
        tokenized = processor.tokenize(text=text, lang='lat')
        segment = tokenized[0]
        self.assertEqual(segment['index'],0)
        self.assertNotIn('alpheios_data_tb_sent',segment)
        token = tokenized[0]['tokens'][0]
        self.assertEqual(token['text'],'In')
        self.assertFalse(token['punct'])
        self.assertFalse(token['line_break_before'])
        self.assertEqual(token['alpheios_data_tb_word'],'')
        self.assertEqual(token['index'],0)
        self.assertEqual(token['docIndex'],0)

    def test_tokenize_singleseg(self):
        text = self.readFixture(type='text', name='singleseg.txt')
        processor = Processor(config=None)
        tokenized = processor.tokenize(text=text, lang='lat')
        self.assertEqual(len(tokenized),1)
        self.assertEqual(len(tokenized[0]['tokens']),32)
        self.assertEqual(tokenized[0]['tokens'][0]['index'],0)
        self.assertEqual(tokenized[0]['tokens'][0]['docIndex'],0)
        self.assertEqual(tokenized[0]['tokens'][6]['text'],'formas')
        self.assertFalse(tokenized[0]['tokens'][6]['line_break_before'])
        self.assertEqual(tokenized[0]['tokens'][7]['text'],'corpora')
        self.assertTrue(tokenized[0]['tokens'][7]['line_break_before'])

    def test_tokenize_lineseg(self):
        text = self.readFixture(type='text', name='lineseg.txt')
        processor = Processor(config=None)
        tokenized = processor.tokenize(text=text, lang='lat', segmentOn='singleline')
        self.assertEqual(len(tokenized),20)
        self.assertEqual(len(tokenized[0]['tokens']),7)
        self.assertEqual(len(tokenized[19]['tokens']),9)
        self.assertFalse(tokenized[0]['tokens'][-1]['line_break_before'])
        self.assertEqual(tokenized[1]['tokens'][0]['index'],0)
        self.assertEqual(tokenized[1]['tokens'][0]['docIndex'],8)
        self.assertTrue(tokenized[1]['tokens'][0]['line_break_before'])

    def test_tokenize_linesegcite(self):
        text = self.readFixture(type='text', name='linesegcite.txt')
        processor = Processor(config=None)
        tokenized = processor.tokenize(text=text, lang='lat', segmentOn='singleline')
        self.assertEqual(len(tokenized),4)
        self.assertEqual(tokenized[0]['alpheios_data_cite'],'urn:cts:latinLit:phi0959.phi006.alpheios-text-lat1:1.1')
        self.assertEqual(tokenized[0]['tokens'][0]['text'],'In')
        self.assertEqual(tokenized[1]['alpheios_data_cite'],'http://citation2')
        self.assertEqual(tokenized[1]['tokens'][0]['text'],'corpora')
        self.assertEqual(tokenized[2]['alpheios_data_cite'],'https://citation3')
        self.assertEqual(tokenized[2]['tokens'][0]['text'],'adspirate')
        self.assertEqual(tokenized[3]['alpheios_data_cite'],'citation4')
        self.assertEqual(tokenized[3]['tokens'][0]['text'],'ad')

    def test_tokenize_linesegsenttbsent(self):
        text = self.readFixture(type='text', name='lineseg.txt')
        processor = Processor(config=None)
        tokenized = processor.tokenize(
            text=text,
            lang='lat',
            segmentOn='singleline',
            segmentStart=1,
            segmentMetadataTemplate=self.tbrequestmeta)
        self.assertEqual(len(tokenized),20)
        self.assertEqual(tokenized[0]['alpheios_data_tb_sent'],'1')
        self.assertEqual(tokenized[1]['alpheios_data_tb_sent'],'2')

    def test_tokenize_doublelineseg(self):
        text = self.readFixture(type='text', name='doublelineseg.txt')
        processor = Processor(config=None)
        tokenized = processor.tokenize(text=text, lang='lat', segmentOn='doubleline')
        self.assertEqual(len(tokenized),2)
        self.assertEqual(tokenized[1]['tokens'][0]['text'],'nullus')
        self.assertTrue(tokenized[1]['tokens'][0]['line_break_before'])

    def test_tokenize_doublelinesegcite(self):
        text = self.readFixture(type='text', name='doublelinesegcite.txt')
        processor = Processor(config=None)
        tokenized = processor.tokenize(text=text, lang='lat', segmentOn='doubleline')
        self.assertEqual(len(tokenized),2)
        self.assertTrue(tokenized[0]['alpheios_data_cite'],'citation1')
        self.assertTrue(tokenized[1]['alpheios_data_cite'],'citation2')
        self.assertEqual(tokenized[1]['tokens'][0]['text'],'nullus')
        self.assertTrue(tokenized[1]['tokens'][0]['line_break_before'])

    def test_tokenize_linesegcustomtb(self):
        text = self.readFixture(type='text', name='linesegtb.txt')
        processor = Processor(config=None)
        tokenized = processor.tokenize(text=text, lang='lat', segmentOn='singleline', segmentStart=1)
        self.assertEqual(len(tokenized),3)
        self.assertTrue(tokenized[0]['index'],1)
        self.assertEqual(tokenized[0]['tokens'][2]['text'],'fert')
        self.assertEqual(tokenized[0]['tokens'][2]['alpheios_data_tb_word'],'1')
        self.assertEqual(tokenized[1]['alpheios_data_tb_sent'],'11')
        self.assertEqual(tokenized[1]['index'],2)
        self.assertEqual(tokenized[2]['alpheios_data_tb_sent'],'12')
        self.assertTrue(tokenized[2]['index'],3)
        self.assertEqual(tokenized[2]['tokens'][0]['text'],'adspirate')
        self.assertEqual(tokenized[2]['tokens'][0]['alpheios_data_tb_word'],'1')



if __name__ == '__main__':
  unittest.main()