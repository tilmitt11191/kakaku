#!/usr/bin/python
# -*- coding: utf-8 -*-
import yaml
import os
import re
class Conf:
	def __init__(self):
		with open("../../etc/config.yml", "r") as f:
			conf = yaml.load(f)

	@classmethod
	def getconf(cls, conf, conffile="../../etc/config.yml"):
		if(conffile==""):
			conffile="../../etc/config.yml"
		with open(conffile, "r") as f:
			confs = yaml.load(f)
		result = confs[conf]

		p = re.compile('\<%= ENV\[\'.*?\'\] %\>')
		if not p.match(str(result)):
			return result
		result = p.sub(cls.sub_env, str(result), count=0)
		return result

	@classmethod
	def sub_env(cls, matchobj):
		env = re.sub('\<%= ENV\[\'|\'\] %\>', "", matchobj.group(0))
		return os.environ[env]
