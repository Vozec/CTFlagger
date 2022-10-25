#!/usr/bin/python3
# -*- encoding: utf-8 -*-
# Author: Vozec
# CTFiles Scan Project 

from utils.utils_func import Execmd
from os import path,mkdir,rmdir


def help():
	config = {
		'type':{'picture':['.png','.bmp']},
		'name':'LsbExpose'
	}
	return config

def Save(data,filename):
	f = open(filename,'wb')
	f.write(data)
	f.close()

def scan(config):
	config_current = help()

	dir_img = '%s/stegexp'%config['env_dir']

	mkdir(dir_img)
	cmd  = 'StegExpose %s default 0.25 %s/stegexp.csv'%(dir_img,config['env_dir'])
	Execmd(cmd)
	rmdir(dir_img)

	files = ''
	if path.exists('%s/stegexp.csv'%config['env_dir']):
		files = '/%s/stegexp.csv'%(config['hash'])

	return {"type":"file","path":files,"content":content}