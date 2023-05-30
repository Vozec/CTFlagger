#!/usr/bin/python3
# -*- encoding: utf-8 -*-
# Author: Vozec
# CTFlagger

from utils.utils_func import Execmd
from os import path

def help():
	config = {
		'type':{'picture':['.png']},
		'name':'StegoPit'
	}
	return config


def scan(config):
	config_current = help()

	path1 		 = '%s/StegoLSB_bruteforce.raw'%config['env_dir']
	path2 		 = '%s/StegoLSB_extract.raw'%config['env_dir']

	content 	= []
	result_path = []

	for X in ['R','G','B']:
		path1   = '%s/PIT_secret_%s.txt'%(config['env_dir'],X)
		cmd 	= 'stegopit -v -i %s %s -w %s'%(X,config['path'],path1)
		Execmd(cmd)
		if(path.exists(path1)):
			result_path.append('/%s/PIT_secret_%s.txt'%(config['hash'],X))
			data = open(path1,'rb').read()
			try:
				content.append(data.decode('utf-8'))
			except:
				pass

	return {"type":"file","path":result_path,"content":content}
