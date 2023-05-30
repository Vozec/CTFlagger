#!/usr/bin/python3
# -*- encoding: utf-8 -*-
# Author: Vozec
# CTFlagger

from utils.utils_func import Execmd
from os import path

def help():
	config = {
		'type':{'picture':['.bmp','.png','.gif','.webp','.wav']},
		'name':'Stegpy'
	}
	return config


def scan(config):
	config_current = help()

	path1 = '%s/stegpy.txt'%config['env_dir']

	cmd = 'stegpy %s | tee -a %s'%(config['path'],path1)
	content = Execmd(cmd).decode()

	result_path = '/%s/stegpy.txt'%(config['hash']) if path.exists(path1) else ""

	return {"type":"file","path":result_path,"content":content}
