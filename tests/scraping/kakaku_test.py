# -*- coding: utf-8 -*-

import unittest
import sys,os

sys.path.append(os.path.dirname(os.path.abspath(__file__)) + "/../../lib/utils")
from log import Log
from conf import Conf

sys.path.append(os.path.dirname(os.path.abspath(__file__)) + "/../../lib/scraping")
from phantomjs_ import PhantomJS_

sys.path.append(os.path.dirname(os.path.abspath(__file__)) + "/../../src/scraping")
from kakaku import Kakaku

class webdriver_test(unittest.TestCase):

	@classmethod
	def setUpClass(cls):
		
		cls.log = Log.getLogger()
		cls.conf = Conf()
		cls.driver = PhantomJS_()
		cls.kakaku = Kakaku()
		cls.log.info("\n\n"+__class__.__name__+ "."+sys._getframe().f_code.co_name+" finished.\n---------- start ---------")

	def setUp(self):
		pass

	"""
	def test_phantomjs_init(self):
		self.log.debug(__class__.__name__ + "." + sys._getframe().f_code.co_name + " start.")
		self.driver = PhantomJS_(warning_messages=True)
		self.log.debug(__class__.__name__ + "." + sys._getframe().f_code.co_name + " finishd.")
	"""
	"""
	def test_phantomjs_wait_appearance_of_tag(self):
		url = "http://kakaku.com/search_results/%82%E4%82%AB%82%BF%96%7B%95%DC+OBD%82Q%81%40%83%7C%81%5B%83g%97p16PIN%81%40%83%81%83X%82Q%8Cn%93%9D%81%40%95%AA%8A%F2%8E%E6%82%E8%8Fo%82%B5%81%40%89%84%92%B7%83P%81%5B%83u%83%8B/"
		tag = '//a[@class="selfLink"]'
		tag = '//div[@class="slideItemCard"]'
		self.kakaku.driver.get(url,tag_to_wait=tag)
	"""
	"""
	def test_move_to_top_page(self):
		self.log.debug(__class__.__name__ + "." + sys._getframe().f_code.co_name + " start.")
		self.kakaku.move_to_top_page()
		self.log.debug(__class__.__name__ + "." + sys._getframe().f_code.co_name + " finished.")
	"""
	"""
	def test_search_product1(self):
		self.log.debug(__class__.__name__ + "." + sys._getframe().f_code.co_name + " start.")
		product_name = "Ryzen Threadripper 1950X BOX"
		self.kakaku.move_to_top_page()
		results = self.kakaku.search_product(product_name)
		self.log.debug("len(results): " + str(len(results)))
		self.assertTrue(len(results) > 0)
		self.log.debug(__class__.__name__ + "." + sys._getframe().f_code.co_name + " finished.")
	"""
	def test_search_product2(self):
		self.log.debug(__class__.__name__ + "." + sys._getframe().f_code.co_name + " start.")
		product_name = "ゆきち本舗 OBD２　ポート用16PIN　メス２系統　分岐取り出し　延長ケーブル"
		self.kakaku.move_to_top_page()
		results = self.kakaku.search_product(product_name)
		self.log.debug("len(results): " + str(len(results)))
		self.assertTrue(len(results) > 0)
		self.log.debug(__class__.__name__ + "." + sys._getframe().f_code.co_name + " finished.")
	"""
	def test_get_cheapest_vendor(self):
		self.log.debug(__class__.__name__ + "." + sys._getframe().f_code.co_name + " start.")
		url = "http://kakaku.com/item/K0000987818/?lid=ksearch_kakakuitem_image"
		tag = '//p[@class="wordwrapShop"]/a'
		self.kakaku.driver.get(url, tag_to_wait=tag, warning_messages=False)
		#self.kakaku.driver.save_current_page("ss/get_cheapest_vendor.png")
		cheapest_vendor_button, name = self.kakaku.get_cheapest_vendor_button()
		print("vendor name: " + name)

		self.kakaku.move_to_vendor_page(cheapest_vendor_button)
		self.kakaku.driver.save_current_page("ss/move_to_vendor_page.png")
		self.log.debug(__class__.__name__ + "." + sys._getframe().f_code.co_name + " finished.")
	"""
	"""
	def test_conf_env(self):
		result = Conf.getconf("pdf_save_path")
		print(result)
	"""
if __name__ == '__main__':
	unittest.main()