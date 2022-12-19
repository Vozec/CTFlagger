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

	path1 	= '%s/openstego_nopass.txt'%config['env_dir']
	path2 	= '%s/openstego_pass.txt'%config['env_dir']

	content = []

	if config['password']:
		cmd = "openstego extract --password '%s' -sf %s --extractdir %s | tee -a %s"%(
			['password'],config['path'],config['env_dir'],path2)
		content.append(Execmd(cmd).decode())

	cmd = "echo '' | openstego extract -sf %s --extractdir %s 2>&1 | tee -a %s"%(
		config['path'],config['env_dir'],path1)
	content.append(Execmd(cmd).decode())

	result_path = []
	for p in [path1,path2]:
		if path.exists(p):
			result_path.append('/%s/%s'%(config['hash'],p.split('/')[-1]))

	return {"type":"file","path":result_path,"content":content}