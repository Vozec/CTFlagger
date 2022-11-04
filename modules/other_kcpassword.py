from utils.utils_func import Execmd
from os import path

def help():
	config = {
		'type':{'other':['kcpassword']},
		'name':'KcPassword'
	}
	return config

def XOR(password,key):
	return ''.join([chr((password[i])^(key[i%len(key)])) for i in range(len(password))])

def scan(config):
	config_current = help()

	path1 = '%s/KcPassword_decoded.txt'%config['env_dir']

	magic_Key_hex	 = '7d895223d2bcddeaa3b91f'
	magic_Key 		 = bytes.fromhex(magic_Key_hex)
	kcpassword 		 = open(config['path'],'rb').read()
	kcpassword_clear = XOR(kcpassword,magic_Key)

	data = "Magic Key Hex   : %s\nMagic Key Ascii : %s\n\nKcPassword      : %s\nKcPassword Clear: %s\n"\
		%(magic_Key_hex,magic_Key,kcpassword,kcpassword_clear)

	if(kcpassword_clear != ""):
		f = open(path1,'w')
		f.write(data)
		f.close()
	
	result_path = ''
	if(path.exists(path1)):
		result_path = '/%s/KcPassword_decoded.txt'%(config['hash'])
		
	return {"type":"file","path":result_path,"content":data}