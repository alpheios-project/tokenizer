import unittest
from unittest import TestCase
from tokenizer.lib.tei.parser import Parser
import os

class ParserTest(TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def readFixture(self, type=None, name=None):
        fixture = os.path.join('tests', 'fixtures', type, name)
        with open(fixture, 'r', encoding="utf-8") as (stream):
            text = stream.read()
        return text

    def test_cleantext(self):
        parser = Parser(config=None)
        self.maxDiff = None
        text = self.readFixture(type='tei', name='singlesegout.txt')
        cleaned = parser.clean_text(text)
        self.assertEqual(cleaned,"In nova fert animus mutatas dicere formas \ncorpora; di, coeptis ( nam vos mutastis et illas) \nadspirate meis primaque ab origine mundi \nad mea perpetuum deducite tempora carmen. \n\n")
        text = self.readFixture(type='tei', name='multisegout.txt')
        cleaned = parser.clean_text(text)
        self.assertEqual(cleaned,"In nova fert animus mutatas dicere formas \ncorpora; di, coeptis ( nam vos mutastis et illas) \nadspirate meis primaque ab origine mundi \nad mea perpetuum deducite tempora carmen. \n\nIn nova fert animus mutatas dicere formas \ncorpora; di, coeptis ( nam vos mutastis et illas) \nadspirate meis primaque ab origine mundi \nad mea perpetuum deducite tempora carmen. \n\n")

    def test_parsetext_defaults(self):
        parser = Parser(config=None)
        text = self.readFixture(type='tei', name='caesarciv.xml')
        expected = "Gallia est omnis divisa in partes tres, quarum unam incolunt Belgae, aliam Aquitani, tertiam qui ipsorum lingua Celtae, nostra Galli appellantur. \nHi omnes lingua, institutis, legibus inter se differunt. Gallos ab Aquitanis Garumna flumen, a Belgis Matrona et Sequana dividit. \nHorum omnium fortissimi sunt Belgae, propterea quod a cultu atque humanitate provinciae longissime absunt, minimeque ad eos mercatores saepe commeant atque ea quae ad effeminandos animos pertinent important, \n\n"
        parsed = parser.parse_text(tei=text)
        self.maxDiff = None
        self.assertEqual(parsed,expected)

    def test_parsetext_divseg(self):
        parser = Parser(config=None)
        text = self.readFixture(type='tei', name='caesarciv.xml')
        expected = "Gallia est omnis divisa in partes tres, quarum unam incolunt Belgae, aliam Aquitani, tertiam qui ipsorum lingua Celtae, nostra Galli appellantur. \n\nHi omnes lingua, institutis, legibus inter se differunt. Gallos ab Aquitanis Garumna flumen, a Belgis Matrona et Sequana dividit. \n\nHorum omnium fortissimi sunt Belgae, propterea quod a cultu atque humanitate provinciae longissime absunt, minimeque ad eos mercatores saepe commeant atque ea quae ad effeminandos animos pertinent important, \n\n"
        parsed = parser.parse_text(tei=text,segmentElems="div")
        self.maxDiff = None
        self.assertEqual(parsed,expected)

    def test_parsetext_varia(self):
        parser = Parser(config=None)
        text = self.readFixture(type='tei', name='withlines.xml')
        expected = "nullus adhuc mundo praebebat lumina Titan, \nnec nova crescendo reparabat cornua Phoebe, \nHanc deus et melior litem natura diremit. \nNam caelo terras et terris abscidit undas, \n\n"
        parsed = parser.parse_text(tei=text)
        self.maxDiff = None
        self.assertEqual(parsed,expected)
        expected = "nullus adhuc mundo praebebat lumina Titan, nec nova crescendo reparabat cornua Phoebe, Hanc deus et melior litem natura diremit. Nam caelo terras et terris abscidit undas, \n\n"
        parsed = parser.parse_text(tei=text,linebreakElems="ab")
        self.assertEqual(parsed,expected)
        expected = "nullus adhuc mundo praebebat lumina Titan,\n\nnec nova crescendo reparabat cornua Phoebe,\n\nHanc deus et melior litem natura diremit.\n\nNam caelo terras et terris abscidit undas,\n\n"
        parsed = parser.parse_text(tei=text,segmentElems="l")
        self.assertEqual(parsed,expected)
        expected = "header \nnullus adhuc mundo praebebat lumina Titan, \nnec nova crescendo reparabat cornua Phoebe, \nHanc deus et melior litem natura diremit. \nNam caelo terras et terris abscidit undas, \n\n"
        parsed = parser.parse_text(tei=text,ignoreElems="none")
        self.assertEqual(parsed,expected)

    def test_parseonlytext(self):
        parser = Parser(config=None)
        text = self.readFixture(type='tei', name='withheadertext.xml')
        parsed = parser.parse_text(tei=text)
        self.assertEqual(parsed,"Gallia est omnis divisa \n\n")

if __name__ == '__main__':
  unittest.main()