#!/usr/bin/python3
# -*- encoding: utf-8 -*-
# Author: Vozec
# CTFlagger

from utils.utils_func import Execmd
from os import path

def help():
	config = {
		'type':{'':[]},
		'name':'Binwalk'
	}
	return config


def scan(config):
	config_current = help()

	path1 		 = '%s/binwalk.txt'%config['env_dir']
	path_save 	 = '%s/binwalk'%config['env_dir']

	cmd 		 = 'binwalk %s -D=".*" -M --directory=%s | tee -a %s;'%(config['path'],path_save,path1)
	cmd 		+= 'zip -q -r %s/binwalk.zip %s ;'%(config['env_dir'],path_save)
	cmd 		+= 'rm -r %s;'%(path_save)

	res = Execmd(cmd).decode()
	
	result_path = []
	for file in [path1,'%s/binwalk.zip'%config['env_dir']]:
		if(path.exists(file)):
			result_path.append('/%s/%s'%(config['hash'],file.split('/')[-1]))
	
	return {"type":"file","path":result_path,"content":res}