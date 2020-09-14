import unittest
from unittest import TestCase
from tokenizer.lib.meta.parser import Parser

class ParserTest(TestCase):

    def setUp(self):
        self.parser = Parser()

    def tearDown(self):
        pass

    def test_parseLine(self):
        meta,line = self.parser.parseLine(line='foo')
        self.assertEqual(meta,{})
        meta, line = self.parser.parseLine(line='foo META|')
        self.assertEqual(meta,{})
        meta, line = self.parser.parseLine(line='META| abc')
        self.assertEqual(meta,{})
        meta, line = self.parser.parseLine(line='META|TB_SENT_1 abc')
        self.assertEqual(meta,{'TB_SENT': '1'})
        self.assertEqual(line, 'META|TB_SENT_1 abc' )
        meta, line = self.parser.parseLine(line='META|TB_SENT_1 abc',replace=True)
        self.assertEqual(meta,{'TB_SENT': '1'})
        self.assertEqual(line, 'abc' )
        meta, line = self.parser.parseLine(line='META|TB_SENT_1 abc',extra="META|TB_SENT_10",replace=True)
        self.assertEqual(meta,{'TB_SENT': '10'})
        self.assertEqual(line, 'abc' )

    def test_parseToken(self):
        self.assertEqual(self.parser.parseToken('foo'),{})
        self.assertEqual(self.parser.parseToken('META|'),{})
        self.assertEqual(self.parser.parseToken('META|TB_SENT_1'),{'TB_SENT': '1'})
        self.assertEqual(self.parser.parseToken('META|TB_WORD_1'),{'TB_WORD': '1'})
        self.assertEqual(
            self.parser.parseToken('META|CITE_urn:cts:latinLit:phi0959.phi006.alpheios-text-lat1'),
            {'CITE': 'urn:cts:latinLit:phi0959.phi006.alpheios-text-lat1'}
        )
        self.assertEqual(
            self.parser.parseToken('META|TB_SENT_1|CITE_urn:cts:latinLit:phi0959.phi006.alpheios-text-lat1'),
                {
                    'CITE': 'urn:cts:latinLit:phi0959.phi006.alpheios-text-lat1',
                    'TB_SENT': '1'
                }
        )



if __name__ == '__main__':
  unittest.main()