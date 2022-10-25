from utils.utils_func import Execmd
from os import path
import pcapkit

def help():
	config = {
		'type':{'traffic':['.pcap']},
		'name':'Pcapkit'
	}
	return config

def scan(config):
	config_current = help()

	path1 = '%s/pcapkit.json'%(config['env_dir'])
	plist = pcapkit.extract(fin=config['path'], fout=path1, format='json', store=False)


	result_path = ""
	if path.exists(path1):
		result_path = '/%s/pcapkit.json'%(config['hash'])

	return {"type":"file","path":result_path,"content":""}
