from utils.utils_func import Execmd
from os import path
import os

def help():
	config = {
		'type':{'audio':['.wav','.mp3']},
		'name':'Dmtf'
	}
	return config


def scan(config):
	config_current = help()

	path1 = '%s/Dmtf.txt'%config['env_dir']

	cmd = 'dtmf -v %s'%(config['path'])
	
	res = Execmd(cmd).decode()

	if(res != ""):
		f = open(path1,'w')
		f.write(res)
		f.close()
	
	result_path = '/%s/Dmtf.txt'%config['hash'] if path.exists(path1) else ""	
	return {"type":"file","path":result_path,"content":res}