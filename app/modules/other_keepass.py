#!/usr/bin/python3
# -*- encoding: utf-8 -*-
# Author: Vozec
# CTFlagger

from utils.utils_func import Execmd
from os import path

def help():
	config = {
		'type':{'other':['.kdbx','.kdb']},
		'name':'Keepass'
	}
	return config

def scan(config):
	config_current = help()

	rockyou = '/usr/share/wordlists/rockyou.txt'
	path1 = '%s/keepass_hash.txt'%config['env_dir']
	path2 = '%s/keepass_john.txt'%config['env_dir']

	cmd1 = 'keepass2john %s |  grep -o "$keepass$.*" | tee -a %s'%(config['path'],path1)
	cmd2 = 'timeout 15 | john %s --wordlist=%s | tee -a %s'%(path1,rockyou,path2)

	data = [Execmd(cmd).decode() for cmd in [cmd1,cmd2]]

	result_path = []
	for p in [path1,path2]:
		if(path.exists(p)):
			result_path.append('/%s/%s'%(config['hash'],p.split('/')[-1]))
		
	return {"type":"file","path":result_path,"content":data}