#!/usr/bin/python3
# -*- encoding: utf-8 -*-
# Author: Vozec
# CTFiles Scan Project 

from utils.utils_func import Execmd
from os import path

def help():
	config = {
		'type':{'picture':['.bmp','.png']},
		'name':'Zsteg'
	}
	return config

def Filter(filename):
	if path.exists(filename):
		cnt = open(filename,'r').read().split('\n')
		final = ''
		for element in cnt:
			if(not element.endswith('.. ') and not element == ''):
				final += element.strip() + '\n'
		f = open(filename,'w')
		f.write(final)
		f.close()

def scan(config):
	config_current = help()
	path1 = '%s/zsteg.txt'%config['env_dir']
	cmd = 'zsteg -a %s > %s'%(config['path'],path1)
	Execmd(cmd)	

	Filter(path1)

	content = open(path1,'r').read() if path.exists(path1) else ""	
	result_path = '/%s/zsteg.txt'%(config['hash']) if path.exists(path1) else ""
	return {"type":"file","path":result_path,"content":content}
