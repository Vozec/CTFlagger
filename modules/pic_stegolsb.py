#!/usr/bin/python3
# -*- encoding: utf-8 -*-
# Author: Vozec
# CTFiles Scan Project 

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

	cmd1 = 'stegolsb bruteforce  %s 2> %s'%(config['path'],path2)
	cmd2 = 'stegolsb -v extract %s --column-step 2 --rows 1 --columns 128 2> %s'%(config['path'],path1)

	Execmd(cmd1)
	Execmd(cmd2)

	result_path = [
		'/%s/StegoLSB_bruteforce.raw'%(config['hash']),
		'/%s/StegoLSB_extract.raw'%(config['hash']),
	]

	config  	= [
		open(path1,'r').read(),
		open(path2,'r').read()
	]
	return {"type":"file","path":result_path,"content":config}
