from unittest.mock import Mock
import os, json
from lxml import etree
from unittest import TestCase
from tokenizer import tokenizer

class TokenizerTestCase(TestCase):

    def readFixture(self, type=None, name=None):
        fixture = os.path.join('tests', 'fixtures', type, name)
        with open(fixture, 'r', encoding="utf-8") as (stream):
            text = stream.read()
        return text

    def setUp(self):
        self.client = tokenizer.app.test_client()
        tokenizer.init_app(tokenizer.app, config_file='config.cfg')

    def tearDown(self):
        pass

    def test_tokenize_tei_defaults(self):
        text = self.readFixture(type='tei', name='withlines.xml')
        rv = self.client.post('/tokenize?lang=en',data=text, headers={'Content-Type': 'application/xml'})
        data = json.loads(rv.get_data(as_text=True))
        self.assertEqual(len(data['tokens']),1)
        self.assertEqual(len(data['tokens'][0]['tokens']),30)
        self.assertEqual(data['tokens'][0]['tokens'][0]['text'],"nullus")
        self.assertEqual(data['tokens'][0]['tokens'][-1]['text'],",")
        self.assertFalse(data['tokens'][0]['tokens'][0]['line_break_before'])
        self.assertEqual(data['tokens'][0]['tokens'][7]['text'],"nec")
        self.assertTrue(data['tokens'][0]['tokens'][7]['line_break_before'])

    def test_tokenize_tei_segline(self):
        text = self.readFixture(type='tei', name='withlines.xml')
        rv = self.client.post('/tokenize?lang=en&segments=l',data=text, headers={'Content-Type': 'application/xml'})
        data = json.loads(rv.get_data(as_text=True))
        self.assertEqual(len(data['tokens']),4)
        self.assertEqual(data['tokens'][0]['tokens'][0]['text'],"nullus")
        self.assertEqual(data['tokens'][1]['tokens'][0]['text'],"nec")
        self.assertEqual(data['tokens'][2]['tokens'][0]['text'],"Hanc")
        self.assertEqual(data['tokens'][3]['tokens'][0]['text'],"Nam")

    def test_tokenize_text_defaults(self):
        text = self.readFixture(type='text', name='singleseg.csv')
        rv = self.client.post('/tokenize?lang=en',data=text, headers={'Content-Type': 'text/plain'})
        print(rv)
        data = json.loads(rv.get_data(as_text=True))
        self.assertEqual(len(data['tokens']),4)


