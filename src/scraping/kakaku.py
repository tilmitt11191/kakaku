# -*- coding: utf-8 -*-

import os
import sys
import re

sys.path.append(os.path.dirname(os.path.abspath(__file__)) + "/../../lib/utils")
from conf import Conf
from log import Log

sys.path.append(
	os.path.dirname(os.path.abspath(__file__)) + "/../../lib/scraping")
from phantomjs_ import PhantomJS_

class Kakaku:
	def __init__(self):
		self.conf = Conf()
		self.log = Log.getLogger()
		self.driver = self.create_driver()
		self.top_url = self.conf.getconf("kakaku_top_page")
		self.target_stores = self.conf.getconf("target_stores")
		self.extract_store_name = re.compile(r"\'")
		self.log.debug(__class__.__name__ + "." + sys._getframe().f_code.co_name + " start")

	def save_cheapest_pdf(self, product_name):
		self.log.debug(__class__.__name__ + "." + sys._getframe().f_code.co_name + " start.")
		self.log.debug("product_name[" + product_name + "]")
		self.move_to_top_page()

		tag = '//input[@type="text" and @class="c-box-search_text-1_input p-topSerach_input"]'
		input_form = self.driver.find_element_with_handling_exceptions(tag=tag)
		input_form.send_keys(product_name)

		tag = '//span[@class="p-topSerach_submit"]/input[@id="main_search_button" and @name="search" and @type="submit"]'
		submit_button = self.driver.find_element_with_handling_exceptions(tag=tag)
		self.driver.click(submit_button)

		tag = '//a[@class="selfLink"]'
		search_results = self.driver.find_elements_with_handling_exceptions(tag=tag)
		if len(search_results) > 1:
			self.log.warn("search results of product_name[" + str(product_name) + "] > 1.")
			self.log.warn("use only first result.")
		self.driver.click(search_results[0])
		#tag = '//td[@class="fRed"]/p[@class="wordwrapTrs"]/a'
		tag = '//p[@class="wordwrapShop"]/a'
		self.driver.wait_appearance_of_tag(by="xpath", tag=tag)
		vendor_elements = self.driver.find_elements_with_handling_exceptions(tag=tag)
		tag = '//tr/td/a'
		button_elements = []
		els = self.driver.find_elements_with_handling_exceptions(tag=tag)
		for el in els:
			print(el.get_property())
			#if el.get_att("onclick"):
			#	button_elements.append(el)
		self.log.debug("num of vendor: " + str(len(vendor_elements)))
		self.log.debug("num of button: " + str(len(button_elements)))
		
		if len(vendor_elements) == 0:
			self.log.error("num of vendor == 0. Please retry!")
			exit(0)
		vendors = [vendor_element.text for vendor_element in vendor_elements]
		self.log.debug("vendor list: " + str(vendors))
		vendor_id = 0
		for vendor in vendors:
			if vendor in self.target_stores:
				cheapest_vendor = vendor_elements[vendor_id]
				break
			vendor_id += 1
		else:
			self.log.error("No vendor of product_name[" + str(product_name) + "].")
			self.log.error("Vendor list: " + str(self.target_stores))
			exit(0)
		"""
		self.driver.click(cheapest_vendor)
		#self.driver.save_current_page("click_vendor.png")
		#self.driver.save_current_page("click_vendor.html")
		tag = '//p[@class="imgvm"]/a'
		go_to_shop_button = self.driver.find_elements_with_handling_exceptions(tag=tag)
		if len(vendor_elements) == 1:
			self.log.error("num of go_to_shop_button != 1. Use first button!")
		self.driver.click(go_to_shop_button[0])
		self.driver.save_current_page("click_go_to_shop.png")
		self.driver.save_current_page("click_go_to_shop.html")
		
		
		print(len(go_to_shop_button))
		"""
		self.log.debug(__class__.__name__ + "." + sys._getframe().f_code.co_name + " finished.")

	def move_to_top_page(self, timeout=30):
		self.log.debug(__class__.__name__ + "." + sys._getframe().f_code.co_name + " start.")
		tag = '//input[@type="text" and @class="c-box-search_text-1_input p-topSerach_input"]'
		self.driver.get(self.top_url, tag_to_wait=tag)
		self.log.debug(__class__.__name__ + "." + sys._getframe().f_code.co_name + " finished.")

	def create_driver(self, service_args=None, timeout=30):
		self.log.debug(__class__.__name__ + "." +
					   sys._getframe().f_code.co_name + " start")
		driver = PhantomJS_(desired_capabilities={
							'phantomjs.page.settings.resourceTimeout': timeout}, service_args=service_args)
		self.log.debug(__class__.__name__ + "." +
					   sys._getframe().f_code.co_name + " finished. return driver")
		return driver

