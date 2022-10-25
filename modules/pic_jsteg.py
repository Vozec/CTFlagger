#!/usr/bin/python3
# -*- encoding: utf-8 -*-
# Author: Vozec
# CTFiles Scan Project 

from utils.utils_func import Execmd
from os import path

def help():
	config = {
		'type':{'picture':['.jpg','.jpeg']},
		'name':'Jsteg'
	}
	return config


def scan(config):
	config_current = help()
	path1 = '%s/jsteg.txt'%config['env_dir']

	cmd = 'jsteg reveal %s > %s'%(config['path'],path1)
	Execmd(cmd)
	
	content = open(path1,'r').read() if path.exists(path1) else ""	
	result_path = '/%s/jsteg.txt'%(config['hash']) if path.exists(path1) else ""

	return {"type":"file","path":result_path,"content":content}

