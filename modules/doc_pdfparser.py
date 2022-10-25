from utils.utils_func import Execmd
from os import path
import pyUnicodeSteganography as usteg

def help():
	config = {
		'type':{'document':['.pdf']},
		'name':'PdfParser'
	}
	return config

def scan(config):
	config_current = help()

	path1 		 = '%s/PdfParser.txt'%config['env_dir']
	
	cmd = 'pdf-parser -a %s | tee -a %s'%(config['path'],path1)

	res = Execmd(cmd)
	
	result_path = []	
	if(path.exists(path1)):
		result_path.append('/%s/%s'%(config['hash'],path1.split('/')[-1]))

	return {"type":"file","path":result_path,"content":res}


