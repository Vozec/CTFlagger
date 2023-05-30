#!/usr/bin/python3
# -*- encoding: utf-8 -*-
# Author: Vozec
# CTFlagger

from utils.utils_func import Execmd
from os import path

def help():
	config = {
		'type':{'binary':['.bin','.so']},
		'name':'Steg86'
	}
	return config


def scan(config):
	config_current = help()	

	cmd1 = 'steg86 extract %s'%(config['path'])
	content = Execmd(cmd1).decode() 	
	
	return {"type":"file","path":"","content":content}