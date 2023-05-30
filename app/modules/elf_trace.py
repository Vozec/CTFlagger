#!/usr/bin/python3
# -*- encoding: utf-8 -*-
# Author: Vozec
# CTFlagger

from utils.utils_func import Execmd
from os import path

def help():
	config = {
		'type':{'binary':['.bin','.so']}, #  All extension
		'name':'Trace'
	}
	return config


def scan(config):
	config_current = help()

	path1 		 = '%s/ltrace.txt'%config['env_dir']
	path2 		 = '%s/strace.txt'%config['env_dir']
	path3 		 = '%s/checksec.txt'%config['env_dir']

	cmd1 = 'timeout 10 echo "%s" | chmod +x %s ;ltrace %s guess2 2> %s'%('A'*200,config['path'],config['path'],path1)
	cmd2 = 'timeout 10 echo "%s" | chmod +x %s ;strace %s guess2 2> %s'%('A'*200,config['path'],config['path'],path2)
	cmd3 = 'checksec  %s 2> %s;cat %s'%(config['path'],path3,path3)

	Execmd(cmd1)
	Execmd(cmd2)
	
	content = Execmd(cmd3)
	if(content is not None):
		content = content.decode()

	if(path.exists(path1) and "not an ELF file" in open(path1,'r').read()):
		Execmd('rm %s'%path1)

	if(path.exists(path2) and "Exec format error" in open(path2,'r').read()):
		Execmd('rm %s'%path2)

	if(path.exists(path3) and "Magic number does not match" in open(path3,'r').read()):
		Execmd('rm %s'%path3)
		content = ''

	result_path = []
	for file in [path1,path2,path3]:
		if(path.exists(file)):
			result_path.append('/%s/%s'%(config['hash'],file.split('/')[-1]))
			
	return {"type":"file","path":result_path,"content":content}
