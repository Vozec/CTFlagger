#!/usr/bin/python3
# -*- encoding: utf-8 -*-
# Author: Vozec
# CTFlagger

from utils.utils_func import Execmd
from os import path

def help():
	config = {
		'type':{'picture':['.png']},
		'name':'Stegolsb'
	}
	return config


def scan(config):
	config_current = help()

	path1 		 = '%s/StegoLSB_bruteforce.raw'%config['env_dir']
	path2 		 = '%s/StegoLSB_extract.raw'%config['env_dir']

	cmd1 = 'stegolsb bruteforce  %s 2> %s'%(config['path'],path1)
	cmd2 = 'stegolsb -v extract %s --column-step 2 --rows 1 --columns 128 2> %s'%(config['path'],path2)

	Execmd(cmd1)
	Execmd(cmd2)

	result_path = []

	cpl = [
		('/%s/StegoLSB_bruteforce.raw'%(config['hash']),open(path1,'rb').read()),
		('/%s/StegoLSB_extract.raw'%(config['hash']),open(path2,'rb').read())
	]

	for c in cpl:
		if c[1] != b'':
			result_path.append(c[0])
	
	return {"type":"file","path":result_path,"content":""}
