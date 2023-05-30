#!/usr/bin/python3
# -*- encoding: utf-8 -*-
# Author: Vozec
# CTFlagger

from utils.utils_func import Execmd
from os import path

def help():
	config = {
		'type':{'traffic':['.pcap','.cap']},
		'name':'Urlsnarf'
	}
	return config


def scan(config):
	config_current = help()

	path1 		 = '%s/urlsnarf.txt'%config['env_dir']

	cmd1 = 'urlsnarf -p %s | tee -a %s'%(config['path'],path1)	
	res  = Execmd(cmd1).decode()

	result_path = ''
	if(path.exists(path1)):
		result_path = '/%s/urlsnarf.txt'%(config['hash'])


	return {"type":"file","path":result_path,"content":res}