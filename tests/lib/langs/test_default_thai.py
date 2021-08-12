import unittest
from unittest import TestCase
from tokenizer.lib.spacy.models.default import Default
import re
import os

class TestRussianDefault(TestCase):

    def setUp(self):
        model = Default()
        self.nlp = model.load_model(lang="tha",config={})

    def tearDown(self):
        pass

    def readFixture(self, type=None, name=None):
        fixture = os.path.join('tests', 'fixtures', type, name)
        with open(fixture, 'r', encoding="utf-8") as (stream):
            text = stream.read()
        return text

    def testCatalanTokens(self):
        text = self.readFixture(type='langs', name='thai.txt')
        doc = self.nlp(text)
        # มินิบาร์ครบครัน อุปกรณ์ชงชาและกาแฟ และตู้นิรภัยส่วนบุคคล ห้องน้ำมีฝักบัวน้ำอุ่น รองเท้าแตะ และเครื่องใช้ในห้องน้ำฟรี

        self.assertEqual(doc[0].text,"มินิ")
        self.assertEqual(doc[1].text,"บาร์")
        self.assertEqual(doc[2].text,"ครบครัน")
        self.assertEqual(doc[3].text," ")

        self.assertEqual(doc[4].text,"อุปกรณ์")
        self.assertEqual(doc[5].text,"ชงชา")
        self.assertEqual(doc[6].text,"และ")
        self.assertEqual(doc[7].text,"กาแฟ")
        self.assertEqual(doc[8].text," ")

        self.assertEqual(doc[9].text,"และ")
        self.assertEqual(doc[10].text,"ตู้นิรภัย")
        self.assertEqual(doc[11].text,"ส่วนบุคคล")
        self.assertEqual(doc[12].text," ")

        self.assertEqual(doc[13].text,"ห้องน้ำ")
        self.assertEqual(doc[14].text,"มี")
        self.assertEqual(doc[15].text,"ฝักบัว")
        self.assertEqual(doc[16].text,"น้ำอุ่น")
        self.assertEqual(doc[17].text," ")

        self.assertEqual(doc[18].text,"รองเท้าแตะ")
        self.assertEqual(doc[19].text," ")

        self.assertEqual(doc[20].text,"และ")
        self.assertEqual(doc[21].text,"เครื่องใช้")
        self.assertEqual(doc[22].text,"ใน")
        self.assertEqual(doc[23].text,"ห้องน้ำ")
        self.assertEqual(doc[24].text,"ฟรี")

        self.assertEqual(len(doc),25)


