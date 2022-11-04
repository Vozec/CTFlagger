from utils.utils_func import Execmd
from os import path
import os

def help():
	config = {
		'type':{'doc':['.pdf']},
		'name':'PdfCrack'
	}
	return config


def scan(config):
	config_current = help()
	rockyou = "/usr/share/wordlists/rockyou.txt"

	path1 ,res = '%s/PdfCrack.txt'%config['env_dir'] , ''

	if(not path.exists(path1)):
		os.mkdir(path1)

	if('Document is password protected' in Execmd("exiftool %s"%config['path']).decode()):
		res = Execmd('pdfcrack --wordlist=%s %s | tee -a %s'%(rockyou,config['path'],path1))

	result_path = ''
	if(path.exists(path1)):
		result_path = '/%s/%s'%(config['hash'],path1.split('/')[-1])

	return {"type":"file","path":result_path,"content":res}