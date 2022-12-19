from utils.utils_func import Execmd
from os import path

def help():
	config = {
		'type':{'other':['.zip']},
		'name':'ZipCracker'
	}
	return config


def scan(config):
	config_current = help()

	path1 = '%s/zipinfo.txt'%config['env_dir']
	path2 = '%s/hash_zip.txt'%config['env_dir']
	path3 = '%s/zip_cracked.txt'%config['env_dir']

	cmd1 = 'zipinfo %s | tee -a %s'%(config['path'],path1)
	cmd2 = 'zipdetails %s | tee -a %s'%(config['path'],path1)

	rockyou = "/usr/share/wordlists/rockyou.txt"
	more = 'timeout 40 john %s --wordlist=%s ;john %s --show | tee -a %s'\
				%(path2,rockyou,path2,path3)\
				if(path.exists(rockyou)) else ''

	cmd3 ="""
if zipdetails %s | grep -q Encryption; then
  zip2john %s | tee -a %s;
  %s
fi
"""[1:-1]%(config['path'],config['path'],path2,more)

	res = [Execmd(c).decode().strip() for c in (cmd1,cmd2,cmd3)]
	print(res)
	exit()
	
	result_path = []
	for file in [path1,path2,path3]:
		if(path.exists(file)):
			result_path.append('/%s/%s'%(config['hash'],file.split('/')[-1]))

	return {"type":"file","path":result_path,"content":res}