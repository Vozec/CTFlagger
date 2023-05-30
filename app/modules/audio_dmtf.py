#!/usr/bin/python3
# -*- encoding: utf-8 -*-
# Author: Vozec
# CTFlagger

from utils.utils_func import Execmd
from os import path
import os

def help():
	config = {
		'type':{'audio':['.wav','.mp3']},
		'name':'Dmtf'
	}
	return config

def Save(data,filename):
	f = open(filename,'wb')
	f.write(data)
	f.close()

def scan(config):
	config_current = help()

	path1 = '%s/Dmtf.txt'%config['env_dir']

	cmd = 'dtmf -v %s'%(config['path'])
	
	res = Execmd(cmd).decode()

	result_path = ''
	if(res != ""):
		Save(res,path1)
		result_path = '/%s/Dmtf.txt'%config['hash']
	
	return {"type":"file","path":result_path,"content":res}