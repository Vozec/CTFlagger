#!/usr/bin/python3
# -*- encoding: utf-8 -*-
# Author: Vozec
# CTFiles Scan Project 

from utils.utils_func import Execmd
from os import path

def help():
	config = {
		'type':{'picture':['.jpg','.jpeg','.pnm','.ppm']}, #  All extension
		'name':'Outguess'
	}
	return config

def scan(config):
	config_current = help()
	path_extracted = "%s/outguess_extracted.txt"%config['env_dir']

	if config['password']:
		cmd = "outguess -k '%s' -r %s %s"%(config['password'],config['path'],path_extracted)
	else:
		cmd = "outguess -k ''   -r %s %s"%(config['path'],path_extracted)


	res = Execmd(cmd)
	if (b'datalen is too long' in res):
		Execmd('rm %s'%path_extracted)

	content = open(path_extracted,'r').read() if path.exists(path_extracted) else ""	
	result_path = '/%s/outguess_extracted.txt'%(config['hash']) if path.exists(path_extracted) else ""

	return {"type":"file","path":result_path,"content":content}