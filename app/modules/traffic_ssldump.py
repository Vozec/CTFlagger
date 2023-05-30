#!/usr/bin/python3
# -*- encoding: utf-8 -*-
# Author: Vozec
# CTFlagger

from utils.utils_func import Execmd
from os import path

def help():
	config = {
		'type':{'traffic':['.pcap','.cap']},
		'name':'SslDump'
	}
	return config


def scan(config):
	config_current = help()

	path1 = '%s/ssldump.txt'%config['env_dir']

	cmd = 'ssldump -r %s'%(config['path'])

	res = Execmd(cmd).decode()

	if(res != ''):
		f = open(path1,'w')
		f.write(res)
		f.close()

	result_path = []
	if(path.exists(path1)):
		result_path.append('/%s/%s'%(config['hash'],path1.split('/')[-1]))

	return {"type":"file","path":result_path,"content":res}
