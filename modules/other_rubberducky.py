from utils.utils_func import Execmd
from os import path
from ducktoolkit import decoder

def help():
	config = {
		'type':{'other':['.bin']},
		'name':'RubberDucky'
	}
	return config


def scan(config):
	config_current = help()

	path1 = '%s/RubberDucky_Decoded.txt'%config['env_dir']

	res1 = decoder.decode_script('gb',open(config['path'],'rb').read())

	if(res1 != ""):
		f = open(path1,'w')
		f.write(res1)
		f.close()


	result_path = ''
	if(path.exists(path1)):
		result_path = '/%s/%s'%(config['hash'],path1.split('/')[-1])
			
	return {"type":"file","path":result_path,"content":res1}
