#!/usr/bin/python3
# -*- encoding: utf-8 -*-
# Author: Vozec
# CTFlagger

from utils.utils_func import Execmd
from os import path

def help():
	config = {
		'type':{'':[]}, # All type | All extension
		'name':'Strings'
	}
	return config


def scan(config):
	config_current = help()	

	path1 = '%s/strings_total.txt'%config['env_dir']
	path2 = '%s/strings_head.txt'%config['env_dir']
	path3 = '%s/strings_bottom.txt'%config['env_dir']

	cmd1 = 'strings -n 7 -t x %s | tee -a %s  '%(config['path'],path1)
	cmd2 = 'strings -n 7 -t x %s  | head -n 20 | tee -a %s'%(config['path'],path2)
	cmd3 = 'strings -n 7 -t x %s  | tail -n 20 | tee -a %s'%(config['path'],path3)

	res = [Execmd(x).decode().strip() for x in (cmd1,cmd2,cmd3)]
	
	result_path = []
	for file in [path1,path2,path3]:
		if(path.exists(file)):
			result_path.append('/%s/%s'%(config['hash'],file.split('/')[-1]))

	return {"type":"file","path":result_path,"content":res}