# -*- coding: utf-8 -*-

import unittest
import sys,os

sys.path.append(os.path.dirname(os.path.abspath(__file__)) + "/../../lib/utils")
from log import Log
from conf import Conf

sys.path.append(os.path.dirname(os.path.abspath(__file__)) + "/../../lib/scraping")
from phantomjs_ import PhantomJS_

class webdriver_test(unittest.TestCase):

	@classmethod
	def setUpClass(cls):
		
		cls.log = Log.getLogger()
		cls.driver = PhantomJS_()
		cls.conf = Conf()
		cls.log.info("\n\n"+__class__.__name__+ "."+sys._getframe().f_code.co_name+" finished.\n---------- start ---------")

	def setUp(self):
		pass

	def test_png_to_pdf(self):
		self.driver.convert_png_to_pdf("click_vendor3.png")


if __name__ == '__main__':
	unittest.main()