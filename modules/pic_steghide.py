#!/usr/bin/python3
# -*- encoding: utf-8 -*-
# Author: Vozec
# CTFiles Scan Project 

from utils.utils_func import Execmd
from os import path
import os

def help():
	config = {
		'type':{'traffic':['.jpg','.jpeg','.bmp','.wav','.au']},
		'name':'Steghide'
	}
	return config

def Save(data,path):
	f = open(path,'wb')
	f.write(data)
	f.close()

def scan(config):
	config_current = help()

	path1 		 = '%s/Steghide.raw'%config['env_dir']
	path2 		 = '%s/Steghide_password.raw'%config['env_dir']

	cmd1 = "steghide extract  -sf %s -q -f -p ''"%(config['path'])
	cmd2 = "steghide extract  -sf %s -q -f -p '%s'"%(config['path'],config['password'])

	Save(Execmd(cmd1),path1)

	result_path = ['/%s/Steghide.raw'%(config['hash'])]
	content 	= [open(path1,'r').read()]

	if(config['password'] != ''):
		Save(Execmd(cmd2),path2)
		result_path.append('/%s/Steghide_password.raw'%(config['hash']))
		content.append(open(path2,'r').read())

	return {"type":"file","path":result_path,"content":content}