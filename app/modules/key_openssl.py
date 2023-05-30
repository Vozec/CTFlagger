#!/usr/bin/python3
# -*- encoding: utf-8 -*-
# Author: Vozec
# CTFlagger

from utils.utils_func import Execmd
from os import path
from factordb.factordb import FactorDB

def help():
	config = {
		'type':{'key':['.pem','.pub','.key','.der','.crt']},
		'name':'Openssl'
	}
	return config


def scan(config):
	config_current = help()

	path1 		 = '%s/Openssl_pubkey.txt'%config['env_dir']
	path2 		 = '%s/Openssl_privkey.txt'%config['env_dir']

	cmd1 = 'openssl rsa -noout -text -inform PEM -in "%s" -pubin -modulus'%(config['path'])
	cmd2 = 'openssl rsa -noout -text -in "%s" -modulus'%(config['path'])

	res1 = Execmd(cmd1)
	res2 = Execmd(cmd2)

	content = ""

	if(res1 is not None):
		res1 = res1.decode()
	if(res2 is not None):
		res2 = res2.decode()

	if("Public-Key" in res1):
		try:
			modulus = int(res1.split('Modulus=')[1].strip(),16)
			f = FactorDB(modulus)
			f.connect()
			factors = f.get_factor_list()
			if(len(factors)) != 1:
				res1 += '\n'+'#'*30+'\n'
				res1 += 'Factors Found:\n'
				res1 += str(factors)+"\n"
				res1 += '#'*30			
		except Exception as ex:
			pass

		open(path1,'w').write(res1)		
		content = res1

	if("Private-Key" in res2):
		open(path2,'w').write(res2)		
		content = res2

	result_path = []
	for file in [path1,path2]:
		if(path.exists(file)):
			result_path.append('/%s/%s'%(config['hash'],file.split('/')[-1]))

	return {"type":"file","path":result_path,"content":content}