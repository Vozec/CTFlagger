#!/usr/bin/python3
# -*- encoding: utf-8 -*-
# Author: Vozec
# CTFiles Scan Project 

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

	result_path = [
		'/%s/StegoPVD_bruteforce.raw'%(config['hash']),
		'/%s/StegoPVD_extract.raw'%(config['hash']),
		'/%s/StegoPVD_extract_zigzag.raw'%(config['hash'])
	]

	config = [
		open(path1,'r').read(),
		open(path2,'r').read(),
		open(path3,'r').read(),
	]
	
	return {"type":"file","path":result_path,"content":content}