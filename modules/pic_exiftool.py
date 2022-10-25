#!/usr/bin/python3
# -*- encoding: utf-8 -*-
# Author: Vozec
# CTFiles Scan Project 

from utils.utils_func import Execmd
from os import path

def help():
	config = {
		'type':{'picture':[]},
		'name':'Exiftool'
	}
	return config


def scan(config):
	config_current = help()

	path1 = '%s/exiftool.txt'%config['env_dir']

	cmd = 'exiftool -E -a -u -g1 %s > %s'%(config['path'],path1)

	Execmd(cmd)
	
	result_path = '/%s/exiftool.txt'%(config['hash']) if path.exists(path1) else ''

	content 	= open(path1,'r').read() if path.exists(path1) else ''
	return {"type":"file","path":result_path,"content":content}
