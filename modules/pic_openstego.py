#!/usr/bin/python3
# -*- encoding: utf-8 -*-
# Author: Vozec
# CTFiles Scan Project 

from utils.utils_func import Execmd
from os import path
import os

def help():
	config = {
		'type':{'traffic':['.png']},
		'name':'Openstego'
	}
	return config

def scan(config):
	config_current = help()

	path1 	= '%s/openstego.txt'%config['env_dir']
	cmd1 	= "echo '' | openstego --extract -sf %s --extractdir %s | tee -a %s"%(config['path'],config['env_dir'],path1)
	content = Execmd(cmd1).decode()

	result_path = ''
	if path.exists(path1):
		result_path = '/%s/openstego.txt'%config['hash']

	return {"type":"file","path":result_path,"content":content}