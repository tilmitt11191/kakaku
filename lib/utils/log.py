# -*- coding: utf-8 -*-
import sys
import logging
import logging.handlers
from conf import Conf

class Log:

	@classmethod
	def getLogger(cls, logfile="", conffile=""):
		exec_env = Conf.getconf("exec_env")
		if exec_env == "normal":
			return cls.getNormalLogger(logfile=logfile, conffile=conffile)
		elif exec_env == "spark":
			return cls.getSparkLogger(logfile=logfile, conffile=conffile)
		else:
			sys.exit("getLogger Type Error[" + str(exec_env) + "]")

	@classmethod
	def getNormalLogger(cls, logfile="", conffile=""):
		logger = logging.getLogger()
		if logger.hasHandlers(): # called before and already created.
			return logger

		if(logfile==""):
			logfile = Conf.getconf("logdir", conffile=conffile) + Conf.getconf("logfile", conffile=conffile)
		loglevel = Conf.getconf("loglevel", conffile=conffile)
		rotate_log_size = Conf.getconf("rotate_log_size")
		if len(logger.handlers) < 1:
			#fh = logging.FileHandler(filename="../../var/log/log2")
			#logger.addHandler(fh)
			rfh = logging.handlers.RotatingFileHandler(
				filename=logfile,
				maxBytes=rotate_log_size, 
				backupCount=Conf.getconf("backup_log_count")
			)
			formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
			rfh.setFormatter(formatter)
			logger.addHandler(rfh)

			stream_handler = logging.StreamHandler()
			stream_handler.setFormatter(formatter)
			stream_handler.setLevel(\
				Conf.getconf("loglevel_to_stdout", conffile=conffile)\
				)
			logger.addHandler(stream_handler)

		id_ = id(logger)
		logger.setLevel(eval("logging."+loglevel))
		logger.debug("return normal logger\n logfile[{logfile}]\n rotate_log_size[{rotate_log_size}]\n id[{id_}]".format(**locals()))
		return logger


	@classmethod
	def getSparkLogger(cls, logfile="", conffile=""):
		if(logfile==""):
			logfile = Conf.getconf("logdir", conffile=conffile) + Conf.getconf("logfile", conffile=conffile)
		from pyspark import SparkContext
		#sc = SparkContext.getOrCreate()
		#log4j = sc._jvm.org.apache.log4j
		#logger = log4j.LogManager.getLogger("myLogger")
		#logger = log4j.LogManager.getLogger(__name__)
		#logger = log4j.LogManager.getRootLogger()
		#logger.appender.FILE.File="../../var/log/log"
		#logger.setLevel(log4jLogger.Level.DEBUG)
		#logger.info("aaaa")
		#return logger

		if not 'LOG_DIRS' in os.environ:
			sys.stderr.write('Missing LOG_DIRS environment variable, pyspark logging disabled')
			return 

		file = os.environ['LOG_DIRS'].split(',')[0] + '/log'
		logging.basicConfig(filename=file, level=logging.INFO, 
				format='%(asctime)s.%(msecs)03d %(levelname)s %(module)s - %(funcName)s: %(message)s')
		logger = logging.getLogger()
		return logger
