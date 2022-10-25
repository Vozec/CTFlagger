from utils.utils_func import Execmd
from os import path
import os

def help():
	config = {
		'type':{'audio':['.wav','.mp3']},
		'name':'Hideme'
	}
	return config


def scan(config):
	config_current = help()

	path1 = '%s/hideme.txt'%config['env_dir']

	cmd = 'hideme %s -f'%(config['path'])
	
	res = Execmd(cmd).decode()

	if(res != ""):
		f = open(path1,'w')
		f.write(res)
		f.close()
	
	result_path = ''
	if path.exists(path1):
		result_path = '/%s/hideme.txt'%config['hash']
	
	return {"type":"file","path":result_path,"content":res}