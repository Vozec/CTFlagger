#!/usr/bin/python3
# -*- encoding: utf-8 -*-
# Author: Vozec
# CTFlagger

from utils.utils_func import Execmd
from os import path

def help():
	config = {
		'type':{'picture':['.jpg','.jpeg','.wav','.bmp','.au']},
		'name':'StegSeek'
	}
	return config

def Filter(paths):
	for p in paths:
		cnt = open(p,'r').read().split('\n')
		final = ''
		for l in cnt:
			if('Progress: ' not in l and l != ''):
				final += l.strip() + '\n'
		f = open(p,'w')
		f.write(final)
		f.close()

def scan(config):
	config_current = help()
	rockyou = '/usr/share/wordlists/rockyou.txt'
	
	path1 		 = '%s/stegseek_brute.txt'%config['env_dir']
	path2 		 = '%s/stegseek_seed.txt'%config['env_dir']

	cmd1 = 'stegseek --crack -sf %s -wl %s -a -f -v -xf %s/output_stegseek.txt &> %s'%(config['path'],rockyou,config['env_dir'],path1)
	cmd2 = 'stegseek --seed -f  -a -v %s  &> %s'%(config['path'],path2)

	Execmd(cmd1)
	Execmd(cmd2)

	#Filter((path1,path2))

	result_path = ['/%s/stegseek_brute.txt'%(config['hash']),'/%s/stegseek_seed.txt'%(config['hash'])]
	content = [open(path1,'r').read(),open(path2,'r').read()]

	if(path.exists('%s/output_stegseek.txt'%config['env_dir'])):
		result_path.append('/%s/output_stegseek.txt'%(config['hash']),)

	return {"type":"file","path":result_path,"content":content}