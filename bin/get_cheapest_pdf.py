# -*- coding: utf-8 -*-

#python ../../bin/get_cheapest_pdf.py "Ryzen Threadripper 1950X BOX"
import os
import sys
import re
import datetime

sys.path.append(os.path.dirname(os.path.abspath(__file__)) + "/../lib/utils")
from conf import Conf
from log import Log

sys.path.append(os.path.dirname(os.path.abspath(__file__)) + "/../src/scraping")
from kakaku import Kakaku

log = Log.getLogger()
kakaku = Kakaku()

args = sys.argv[1:]
print("products: " + str(args))
log_dir = Conf.getconf("product_log_dir")
for arg in args:
	log.info("target product name[" + str(arg) + "]")
	product_name = arg
	log_name = str(datetime.datetime.now().strftime("%Y%m%d_%H%M%S")+"_" + re.sub(" |/", "_", product_name) + ".log")
	#log_name = "product.log"
	#product_log = Log.getLogger(logfile=log_dir+log_name)
	product_log = log
	print("product: " + product_name + ", save log to: " + log_dir+log_name)
	try:
		kakaku.save_cheapest_pdf(product_name, logger=product_log)
	except Exception as e:
		print("Faild. caught " + e.__class__.__name__ + " exception. Please retry [" + product_name + "]")
		print(e)
	print("\n\n")
