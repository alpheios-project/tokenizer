from unittest import TestCase
from tokenizer import tokenizer
class BaseTest(TestCase):

    def setUp(self):
        self.client = tokenizer.app.test_client()
        tokenizer.init_app(tokenizer.app, config_file='config.cfg')

