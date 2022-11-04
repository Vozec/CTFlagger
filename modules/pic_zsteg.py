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

def Filter(data,filename):
	cnt = data.split('\n')
	final = ''
	for element in cnt:
		if(not element.endswith('.. ') and not element == ''):
			final += element.strip() + '\n'
	f = open(filename,'w')
	f.write(final)
	f.close()
	return final

def scan(config):
	config_current = help()
	path1 = '%s/zsteg.txt'%config['env_dir']
	cmd = 'zsteg -a %s | tee -a %s'%(config['path'],path1)
	data = Execmd(cmd).decode()
	Filter(data,path1)
	result_path = '/%s/zsteg.txt'%(config['hash'])
	return {"type":"file","path":result_path,"content":""}
