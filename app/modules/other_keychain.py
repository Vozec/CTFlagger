#!/usr/bin/python3
# -*- encoding: utf-8 -*-
# Author: Vozec
# CTFlagger

from utils.utils_func import Execmd
from os import path

def help():
	config = {
		'type':{'other':['.keychain','.keychain-db']},
		'name':'Keychain'
	}
	return config


def scan(config):
	config_current = help()

	path1 = '%s/Keychain.txt'%config['env_dir']

	res1 = Execmd('chainbreaker --dump-keychain-password-hash %s '%(config['path'])).decode()


	if (config['password'] != None):
		res1 += Execmd('chainbreaker --password=%s -a %s '%(config['password'],config['path'])).decode()
		if(res1 != ""):
			f = open(path1,'w')
			f.write(res1)
			f.close()
		
	result_path = ''
	if(path.exists(path1)):
		result_path = '/%s/%s'%(config['hash'],path1.split('/')[-1])
		
	return {"type":"file","path":result_path,"content":res1}