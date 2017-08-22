# -*- coding: utf-8 -*-

#python ../../bin/get_cheapest_pdf.py "Ryzen Threadripper 1950X BOX"
import os
import sys

sys.path.append(os.path.dirname(os.path.abspath(__file__)) + "/../lib/utils")
from conf import Conf
from log import Log

sys.path.append(os.path.dirname(os.path.abspath(__file__)) + "/../src/scraping")
from kakaku import Kakaku

log = Log.getLogger()
kakaku = Kakaku()

args = sys.argv[1:]

for arg in args:
	log.info("product name[" + str(arg) + "]")
	kakaku.save_cheapest_pdf(arg)
