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
log_dir = os.getcwd() + Conf.getconf("logdir")
for arg in args:
	log.info("target product name[" + str(arg) + "]")
	product_name = re.sub(" ", "_", arg)
	log_name = str(datetime.datetime.now().strftime("%Y/%m/%d-%H:%M:%S")+"_" + product_name + ".log")
	product_log = Log.getLogger(logfile=log_dir+"/"+log_name)
	print("product: " + product_name + ", save log to: " + log_dir+"/"+log_name)
	kakaku.save_cheapest_pdf(product_name, logger=product_log)
