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
        tokenizer.init_app(tokenizer.app, config_file='config.py')

    def tearDown(self):
        pass

    def test_tokenize_tei_defaults(self):
        text = self.readFixture(type='tei', name='withlines.xml')
        rv = self.client.post('/tokenize/tei?lang=en',data=text, headers={'Content-Type': 'application/xml'})
        data = json.loads(rv.get_data(as_text=True))
        self.assertEqual(len(data['segments']),1)
        self.assertEqual(len(data['segments'][0]['tokens']),30)
        self.assertEqual(data['segments'][0]['tokens'][0]['text'],"nullus")
        self.assertEqual(data['segments'][0]['tokens'][-1]['text'],",")
        self.assertFalse(data['segments'][0]['tokens'][0]['line_break_before'])
        self.assertEqual(data['segments'][0]['tokens'][7]['text'],"nec")
        self.assertTrue(data['segments'][0]['tokens'][7]['line_break_before'])

    def test_tokenize_tei_segline(self):
        text = self.readFixture(type='tei', name='withlines.xml')
        rv = self.client.post('/tokenize/tei?lang=en&segments=l',data=text, headers={'Content-Type': 'application/xml'})
        data = json.loads(rv.get_data(as_text=True))
        self.assertEqual(len(data['segments']),4)
        self.assertEqual(data['segments'][0]['tokens'][0]['text'],"nullus")
        self.assertEqual(data['segments'][1]['tokens'][0]['text'],"nec")
        self.assertEqual(data['segments'][2]['tokens'][0]['text'],"Hanc")
        self.assertEqual(data['segments'][3]['tokens'][0]['text'],"Nam")

    def test_tokenize_tei_tbsegstart(self):
        text = self.readFixture(type='tei', name='withlines.xml')
        rv = self.client.post('/tokenize/tei?lang=en&segments=l',data=text, headers={'Content-Type': 'application/xml'})
        data = json.loads(rv.get_data(as_text=True))
        self.assertEqual(len(data['segments']),4)
        self.assertEqual(data['segments'][0]['index'],1)
        self.assertNotIn('alpheios_data_tb_sent',data['segments'][0])
        self.assertEqual(data['segments'][1]['index'],2)
        self.assertNotIn('alpheios_data_tb_sent',data['segments'][1])
        text = self.readFixture(type='tei', name='withlines.xml')
        rv = self.client.post('/tokenize/tei?lang=en&segments=l&tbsegstart=0',data=text, headers={'Content-Type': 'application/xml'})
        data = json.loads(rv.get_data(as_text=True))
        self.assertEqual(len(data['segments']),4)
        self.assertEqual(data['segments'][0]['index'],0)
        self.assertEqual(data['segments'][0]['alpheios_data_tb_sent'],'0')
        self.assertEqual(data['segments'][1]['index'],1)
        self.assertEqual(data['segments'][1]['alpheios_data_tb_sent'],'1')

    def test_tokenize_text_defaults(self):
        text = self.readFixture(type='text', name='lineseg.txt')
        rv = self.client.post('/tokenize/text?lang=en',data=text, headers={'Content-Type': 'text/plain'})
        data = json.loads(rv.get_data(as_text=True))
        self.assertEqual(len(data['segments']),1)

    def test_tokenize_text_segdoubleline(self):
        text = self.readFixture(type='text', name='doublelineseg.txt')
        rv = self.client.post('/tokenize/text?lang=en&segments=doubleline',data=text, headers={'Content-Type': 'text/plain'})
        data = json.loads(rv.get_data(as_text=True))
        self.assertEqual(len(data['segments']),2)

    def test_tokenize_text_tbsegstart(self):
        text = self.readFixture(type='text', name='doublelineseg.txt')
        rv = self.client.post('/tokenize/text?lang=en&segments=doubleline',data=text, headers={'Content-Type': 'text/plain'})
        data = json.loads(rv.get_data(as_text=True))
        self.assertEqual(len(data['segments']),2)
        self.assertEqual(data['segments'][0]['index'],1)
        self.assertNotIn('alpheios_data_tb_sent',data['segments'][0])
        self.assertEqual(data['segments'][1]['index'],2)
        self.assertNotIn('alpheios_data_tb_sent',data['segments'][1])
        rv = self.client.post('/tokenize/text?lang=en&segments=doubleline&tbsegstart=0',data=text, headers={'Content-Type': 'text/plain'})
        data = json.loads(rv.get_data(as_text=True))
        self.assertEqual(len(data['segments']),2)
        self.assertEqual(data['segments'][0]['index'],0)
        self.assertEqual(data['segments'][0]['alpheios_data_tb_sent'],'0')
        self.assertEqual(data['segments'][1]['index'],1)
        self.assertEqual(data['segments'][1]['alpheios_data_tb_sent'],'1')

    def test_tokenize_tei_invalidxml(self):
        text = self.readFixture(type='tei', name='invalid.xml')
        rv = self.client.post('/tokenize/tei?lang=en',data=text, headers={'Content-Type': 'application/xml'})
        self.assertEqual(rv.status_code, 400)
        data = json.loads(rv.get_data(as_text = True))
        self.assertIn("Opening and ending tag mismatch",data['message'])




