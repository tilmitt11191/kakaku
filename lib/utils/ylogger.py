import sys
import os
import logging

class YarnLogger:
	@staticmethod
	def setup_logger():
		if not 'LOG_DIRS' in os.environ:
			sys.stderr.write('Missing LOG_DIRS environment variable, pyspark logging disabled')
			return 

		file = os.environ['LOG_DIRS'].split(',')[0] + '/log'
		logging.basicConfig(filename=file, level=logging.INFO, 
				format='%(asctime)s.%(msecs)03d %(levelname)s %(module)s - %(funcName)s: %(message)s')

	def __getattr__(self, key):
		return getattr(logging, key)

YarnLogger.setup_logger()