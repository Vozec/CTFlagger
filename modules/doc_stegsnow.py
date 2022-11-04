from utils.utils_func import Execmd
from os import path

def help():
	config = {
		'type':{'document':['.txt']},
		'name':'Stegsnow'
	}
	return config


def scan(config):
	config_current = help()

	path1 = '%s/Stegsnow_nopwd.txt'%config['env_dir']
	path2 = '%s/Stegsnow_pwd.txt'%config['env_dir']

	result = ''

	res1 = Execmd('stegsnow -C %s'%(config['path']))
	if res1 is not None:
		res1 = res1.decode()
		result += res1
		if(res1 != ""):
			f = open(path1,'w')
			f.write(res1)
			f.close()

	if(config['password'] != ''):
		res2 = Execmd('stegsnow -C -p "%s" %s'%(config['password'],config['path']))
		if res2 is not None:
			res2 = res2.decode()
			result += res2
			if(res2 != ""):
				f = open(path2,'w')
				f.write(res2)
				f.close()
	

	result_path = []
	for file in [path1,path2]:
		if(path.exists(file)):
			result_path.append('/%s/%s'%(config['hash'],file.split('/')[-1]))

	return {"type":"file","path":result_path,"content":result}