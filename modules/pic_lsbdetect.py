#!/usr/bin/python3
# -*- encoding: utf-8 -*-
# Author: Vozec
# CTFiles Scan Project 

from utils.utils_func import Execmd
from os import path

def help():
	config = {
		'type':{'picture':['.jpeg','.jpg']},
		'name':'LsbDetect'
	}
	return config

def Save(data,filename):
	f = open(filename,'wb')
	f.write(data)
	f.close()

def scan(config):
	config_current = help()

	path1 = '%s/lsbDetect.txt'%config['env_dir']

	cmd  = 'stegdetect %s'%(config['path'])

	Save(Execmd(cmd),path1)
	
	content = open(path1,'r').read()
	result_path = '/%s/lsbDetect.txt'%(config['hash'])

	return {"type":"file","path":result_path,"content":content}