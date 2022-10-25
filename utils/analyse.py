from threading import Thread
from time import sleep

from utils.logger import logger
from utils.utils_func import *

import os.path
import os


class Scanner(Thread):
	def __init__(self,config,data):

		DB_CLIENT,CONFIG,modules,ext_word = config
		hash,data,password,format_flag = data

		Thread.__init__(self)

		self.config = {		
			'env_dir':'%s/%s'%(CONFIG['dwnl_dir'],hash),
			'path':data['path_up'],
			'filename':os.path.basename(data['path_up']),
			'password':password,
			'formatflag':format_flag,
			'hash':hash
		}
		self.modules = modules
		self.hash 	 = hash
		self.DB_CLIENT = DB_CLIENT
		self.ext_word  = ext_word

	def run(self):

		if(self.config['path'].endswith('cap') or self.config['path'].endswith('pcapng')):
			self.config['path'] = Check_traffic(self.config['path'])

		_type,extension	= Determine_type(self.ext_word,self.config)
		scan_index		= 0

		# extension not supported
		if(not _type or not extension):
			Update_Result(self.DB_CLIENT,self.hash,"error","Unsupported file")
			Update_Status(self.DB_CLIENT,self.hash,'end')
			return -1

		modules_filtred = Filter_modules(self.modules,self.config,extension,_type)

		Update_Progress(self.DB_CLIENT,self.hash,'%s/%s'%(scan_index,len(modules_filtred)))

		result = {}
		bad = [{"type":"file","path":"","content":""},{"type":"file","path":[],"content":""}]
		for mod in list(modules_filtred.items()):
			try:
				res = mod[1][0].scan(self.config)
				if(res not in bad):
					Update_Result(self.DB_CLIENT,self.hash,mod[1][1]['name'],res)
				scan_index += 1
				Update_Progress(self.DB_CLIENT,self.hash,'%s/%s'%(scan_index,len(modules_filtred)))
			except Exception as ex:
				print('[-] Error with "%s" module: %s'%(mod[1][1]['name'],ex))

		Update_Status(self.DB_CLIENT,self.hash,'end')
		return 1


def Analyse(setup,info):
	hash,password,format_flag = info
	DB_CLIENT,CONFIG,THREADS,modules,ext_word = setup

	content = ConvertResult(Get_Result(DB_CLIENT,hash))

	config = (DB_CLIENT,CONFIG,modules,ext_word)
	data   = (hash,content,password,format_flag)

	th = Scanner(config,data)
	th.start()

	
	return True