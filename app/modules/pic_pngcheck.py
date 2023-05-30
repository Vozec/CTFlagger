#!/usr/bin/python3
# -*- encoding: utf-8 -*-
# Author: Vozec
# CTFlagger

from utils.utils_func import Execmd
from os import path

def help():
	config = {
		'type':{'picture':['.png']},
		'name':'Pngcheck'
	}
	return config


def scan(config):
	config_current = help()

	path1 = '%s/pngcheck.txt'%config['env_dir']

	cmd = 'pngcheck -vtp7 %s | tee -a %s'%(config['path'],path1)

	content = Execmd(cmd).decode()		
	result_path = '/%s/pngcheck.txt'%(config['hash'])

	return {"type":"file","path":result_path,"content":content}
