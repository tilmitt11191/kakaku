# -*- coding: utf-8 -*-

import os
import sys
import re
import time

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

	def save_cheapest_pdf(self, product_name, logger=""):
		self.log.debug(__class__.__name__ + "." + sys._getframe().f_code.co_name + " start.")
		self.log.debug("product_name[" + product_name + "]")
		if logger != "":
			self.log = logger
		
		print("move to kakaku.com")
		self.move_to_top_page()

		print("search product. name[" + product_name + "]")
		search_results = self.search_product(product_name)
		if len(search_results) > 1:
			self.log.warn("search results of product_name[" + str(product_name) + "] = " + str(len(search_results)) + " > 1.")
			self.log.warn("use only first result.")

		print("click top of search result")
		if not self.driver.click(search_results[0]):
			self.log.error("click failed. Please retry.")
			exit(1)
		#tag = '//td[@class="fRed"]/p[@class="wordwrapTrs"]/a'
		tag = '//p[@class="wordwrapShop"]/a'
		self.driver.wait_appearance_of_tag(by="xpath", tag=tag)

		print("get cheapest vendor")
		cheapest_vendor, vendor_name = self.get_cheapest_vendor_button()

		print("move_to_vendor_page")
		self.move_to_vendor_page(cheapest_vendor)
		path = Conf.getconf("pdf_save_path")
		print("save as " + path + "/" + product_name + "|" + vendor_name + ".pdf")
		self.driver.save_current_page(path + "/" + product_name + "|" + vendor_name + ".pdf")
		
		self.log.debug(__class__.__name__ + "." + sys._getframe().f_code.co_name + " finished.")

	def move_to_top_page(self, timeout=30, warning_messages=False):
		self.log.debug(__class__.__name__ + "." + sys._getframe().f_code.co_name + " start.")
		tag = '//input[@type="text" and @class="c-box-search_text-1_input p-topSerach_input"]'
		self.driver.get(self.top_url, tag_to_wait=tag, warning_messages=warning_messages)
		#self.driver.get(self.top_url)
		self.log.debug(__class__.__name__ + "." + sys._getframe().f_code.co_name + " finished.")

	def search_product(self, product_name, timeout=30):
		self.log.debug(__class__.__name__ + "." + sys._getframe().f_code.co_name + " start.")
		tag = '//input[@type="text" and @class="c-box-search_text-1_input p-topSerach_input"]'
		input_form = self.driver.find_element_with_handling_exceptions(tag=tag)
		if input_form == None:
			self.log.warning("input_form not found. Please retly!")
			exit(1)
		input_form.send_keys(product_name)

		tag = '//span[@class="p-topSerach_submit"]/input[@id="main_search_button" and @name="search" and @type="submit"]'
		submit_button = self.driver.find_element_with_handling_exceptions(tag=tag)
		self.log.debug("self.driver.click(submit_button)")
		if not self.driver.click(submit_button):
			self.log.error("click failed. Please retry.")
			exit(1)

		tag = '//a[@class="selfLink"]'
		self.driver.wait_appearance_of_tag(by="xpath", tag=tag)
		search_results = self.driver.find_elements_with_handling_exceptions(tag=tag)
		self.log.debug(__class__.__name__ + "." + sys._getframe().f_code.co_name + " finished.")
		return search_results

	def get_cheapest_vendor_button(self):
		self.log.debug(__class__.__name__ + "." + sys._getframe().f_code.co_name + " start.")
		tag = '//p[@class="wordwrapShop"]/a'
		vendor_elements = self.driver.find_elements_with_handling_exceptions(tag=tag)
		self.log.debug("num of vendor: " + str(len(vendor_elements)))
		tag = '//tr/td/a'
		button_elements = []
		els = self.driver.find_elements_with_handling_exceptions(tag=tag)
		for el in els:
			if el.get_attribute("onclick") and el.get_attribute("href"):
				button_elements.append(el)
		self.log.debug("num of button: " + str(len(button_elements)))
		if len(vendor_elements) != len(button_elements):
			self.log.error("len(vendor_elements) != len(button_elements)")
			self.log.error("vendor_elements: " + str(len(vendor_elements)) + ", button_elements: " + str(len(button_elements)))
			self.log.error("Probably invalid tag. please check kakaku.py")
		if len(vendor_elements) == 0:
			self.log.error("num of vendor == 0. Please retry!")
			exit(0)
		vendors = [vendor_element.text for vendor_element in vendor_elements]
		self.log.debug("vendor list: " + str(vendors))
		vendor_id = 0
		for vendor in vendors:
			if vendor in self.target_stores:
				cheapest_vendor = button_elements[vendor_id]
				break
			vendor_id += 1
		else:
			self.log.error("No vendor of product_name[" + str(product_name) + "].")
			self.log.error("Vendor list: " + str(self.target_stores))
			exit(0)
		self.log.debug(__class__.__name__ + "." +
					sys._getframe().f_code.co_name + " finished. return vendor_id[ " + str(vendor_id) + "]")
		return button_elements[vendor_id], vendors[vendor_id]

	def move_to_vendor_page(self, vendor_button, warning_messages=False):
		self.log.debug(__class__.__name__ + "." + sys._getframe().f_code.co_name + " start.")
		self.driver.get(vendor_button.get_attribute("href"), warning_messages=warning_messages)
		self.log.debug("wait start")
		for sec in range(self.conf.getconf("phantomJS_load_timeout")):
			self.log.debug("wait redirect " + str(sec) + "[sec]")
			if self.driver.title:
				self.log.debug("move to shop page finished. page title: " + self.driver.title)
				break
			time.sleep(Conf.getconf("vendor_page_wait_time"))
		self.log.debug(__class__.__name__ + "." +
					sys._getframe().f_code.co_name + " finished.")

	def create_driver(self, service_args=None, timeout=30):
		self.log.debug(__class__.__name__ + "." +
					   sys._getframe().f_code.co_name + " start")
		driver = PhantomJS_(desired_capabilities={
							'phantomjs.page.settings.resourceTimeout': timeout}, service_args=service_args)
		self.log.debug(__class__.__name__ + "." +
					   sys._getframe().f_code.co_name + " finished. return driver")
		return driver

