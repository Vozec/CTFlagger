#!/usr/bin/python3
# -*- encoding: utf-8 -*-
# Author: Vozec
# CTFlagger

from utils.utils_func import Execmd
from os import path

def help():
	config = {
		'type':{'picture':['.png']},
		'name':'Stegopvd'
	}
	return config


def scan(config):
	config_current = help()

	path1 		 = '%s/StegoPVD_bruteforce.raw'%config['env_dir']
	path2 		 = '%s/StegoPVD_extract.raw'%config['env_dir']
	path3 		 = '%s/StegoPVD_extract_zigzag.raw'%config['env_dir']

	cmd1 = 'stegopvd bruteforce  %s &> %s'%(config['path'],path1)
	cmd2 = 'stegopvd -v extract %s  &> %s'%(config['path'],path2)
	cmd3 = 'stegopvd -v extract %s --zigzag &> %s'%(config['path'],path3)
	
	Execmd(cmd1)
	Execmd(cmd2)
	Execmd(cmd3)
	
	result_path = []

	cpl = [
		('/%s/StegoPVD_bruteforce.raw'%(config['hash']),open(path1,'rb').read()),
		('/%s/StegoPVD_extract.raw'%(config['hash']),open(path2,'rb').read()),
		('/%s/StegoPVD_extract_zigzag.raw'%(config['hash']),open(path3,'rb').read())
	]

	for c in cpl:
		if c[1] != b'':
			result_path.append(c[0])

	return {"type":"file","path":result_path,"content":""}