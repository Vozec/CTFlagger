import hashlib
import sqlite3
import os
import random
import json
import subprocess
import time

from os.path import exists
from flask import Flask, render_template,jsonify
from pwnlib.util.safeeval import expr as Save_Eval

from utils.importdir import do as LD_modules
from utils.db_cmd import *

def Use_api(request):
	return True if 'Api' in dict(request.headers).keys() and request.headers['API'] == 'True' else False

def Sha1(data):
	return str(hashlib.sha1(data).hexdigest())

def Save(data,hash,ext,CONFIG):
	path = '%s/%s'%(CONFIG['dwnl_dir'],hash)
	if(not exists(path)):os.mkdir(path)
	path_save = '%s/%s/original.%s'%(CONFIG['dwnl_dir'],hash,ext)
	f = open(path_save,'wb')
	f.write(data)
	f.close()
	return path_save

def Execmd(cmd,t=0.25,debug=False):
	if(debug):
		cnt = subprocess.Popen(cmd,shell=True)
	else:
		cnt = subprocess.Popen(cmd,shell=True,stderr=subprocess.PIPE,stdout=subprocess.PIPE,stdin=subprocess.PIPE)
	for k in range(int(t*240)):
		time.sleep(t)
		if(cnt.poll() is not None):
			try:
				return tuple(x for x in cnt.communicate() if x!=b'')[0]#.decode("")
			except Exception as ex:
				return None
	cnt.kill()
	return None

def Size(filename):
	l = os.path.getsize(filename)
	units = ['B','kB','MB','GB','TB','PB']
	for k in range(len(units)):
		if l < (1024**(k+1)):
			break
	return "%4.2f %s" % (round(l/(1024**(k)),2), units[k])

def RdnName(lenght):
	return ''.join([random.choice('abcdefghijklmnopqrstuvwxyz') for _ in range(lenght)])

def Check_exist(DB_CLIENT,hash) -> bool:
	return bool(DB_CLIENT.cursor().execute(CMD_get_by_hash,{'hash':hash}).fetchone())

def Get_Status(DB_CLIENT,hash) -> str:
	return DB_CLIENT.cursor().execute(CMD_get_status_by_hash,{'hash':hash}).fetchone()[0]	

def Get_Result(DB_CLIENT,hash) -> str:
	return DB_CLIENT.cursor().execute(CMD_get_by_hash,{'hash':hash}).fetchone()

def Get_Progress(DB_CLIENT,hash) -> str:
	return DB_CLIENT.cursor().execute(CMD_get_progress_by_hash,{'hash':hash}).fetchone()

def Update_Result(DB_CLIENT,hash_sha1,name,content):
	c = DB_CLIENT.cursor()	
	result = ConvertResult(c.execute(CMD_get_by_hash,{'hash':hash_sha1}).fetchone())
	result_json = json.loads(result['result'])
	result_json[name] = content
	c.execute(CMD_update_result,{'result':json.dumps(result_json),'hash':hash_sha1})
	DB_CLIENT.commit()

def Update_Status(DB_CLIENT,hash_sha1,status):
	c = DB_CLIENT.cursor()
	result = ConvertResult(c.execute(CMD_get_by_hash,{'hash':hash_sha1}).fetchone())
	c.execute(CMD_update_status,{'status':status,'hash':hash_sha1})
	DB_CLIENT.commit()

def Update_Progress(DB_CLIENT,hash_sha1,progress):
	c = DB_CLIENT.cursor()
	result = ConvertResult(c.execute(CMD_get_by_hash,{'hash':hash_sha1}).fetchone())
	c.execute(CMD_update_progress,{'progress':progress,'hash':hash_sha1})
	DB_CLIENT.commit()

def ConvertResult(result):
	config = {
		'hash':result[0],
		'filename':result[1],
		'ext':result[2],
		'status':result[3],
		'path_up':result[4],
		'first_up':result[5],
		'last_up':result[6],
		'size':result[7],
		'upload_count':result[8],
		'magic':result[9],
		'all_password':result[10],
		'flag':result[11],
		'result':result[12],
		'progress':result[13]
	}
	return config

def ResultToJson(result):
	config = ConvertResult(result)
	result = {
		"informations":{
			"first_upload":config['first_up'],
			"last_upload":config['last_up'],
			"name":config['filename'],
			"size":config['size'],
			"upload_count":config['upload_count'],
			"magic":config['magic'],
			"password":Save_Eval(config['all_password']),
		},
		"result":json.loads(config['result'])
	}
	return jsonify(result)

def Update_File(DB_CLIENT,hash_sha1,last_up,password):
	c = DB_CLIENT.cursor()
	result = ConvertResult(c.execute(CMD_get_by_hash,{'hash':hash_sha1}).fetchone())
	all_password = set(Save_Eval(result['all_password']))
	if(password):all_password.add(password)
	c.execute(CMD_update_info,{'last_up':last_up,'upload_count':result['upload_count']+1,'all_password':str(list(all_password)),'hash':hash_sha1})
	DB_CLIENT.commit()

def Result_manager(result):
	config = ConvertResult(result)
	# ToDo : Finir le résultat en HTML
	return render_template('result.html')

def Pcapng_to_pcap(filename):
	new_name = filename.split('.pcapng')[0]+'.pcap'
	cmd = "tshark -F pcap -r %s -w %s"%(filename,new_name)
	Execmd(cmd)
	return new_name

def Cap_to_pcap(filename):
	new_name = filename.split('.cap')[0]+'.pcap'
	cmd = "tshark -F pcap -r %s -w %s"%(filename,new_name)
	Execmd(cmd)
	return new_name

def Check_traffic(filename):
	new_name = filename
	if(filename.endswith('.pcapng')):
		new_name = Pcapng_to_pcap(filename)
	elif (filename.endswith('.cap')):		
		new_name = Cap_to_pcap(filename)
	if( not exists(new_name)):
		new_name = filename
	return new_name

def File(filename):
	return Execmd('file "%s"'%filename).decode().split(filename)[1].split(":")[1].strip()

def Determine_type(ext_word,config):
	filename = config['path']
	file_res = File(filename)
	for _ in ext_word:
		for _type in list(_.keys()):
			for ext in list(_[_type]):
				if(filename.endswith(ext) or ext in file_res):
					_extension = '.'+filename.split('.')[::-1][0].lower() if '.' in filename else filename
					return _type,_extension
	return None,None

def Filter_modules(modules,config,ext,_type):
	filtered = {}
	for mod in list(modules.items()):
		for type_module,ext_module in mod[1][1]['type'].items():
			if(type_module  == ''):
				filtered[mod[0]]=mod[1] # 'All' files modules
			else:
				if((type_module == _type or _type == None) and \
					 (ext_module == [] or ext == config['filename'])): # If 'None' => type not found in all modules
					filtered[mod[0]]=mod[1] # If Valid ext | If Module allow all files
				elif(ext in ext_module):
					filtered[mod[0]]=mod[1]
	return filtered

def Load_modules(ext_word):
	modules = LD_modules("./modules/", globals())	
	for mod in modules.items():		
		for _ in mod[1][1]['type'].items():
			if(_[0] not in ext_word[1].keys()):
				ext_word[1][_[0]] = set()
				ext_word[1][_[0]].update(_[1])
			else:
				for ext in _[1]:
					if(ext not in ext_word[1][_[0]]):
						ext_word[1][_[0]].update([ext])
	return modules , ext_word

def Magic(filename):
	line = Execmd('xxd -p -l 12 "%s"'%filename).decode()
	return ' '.join([line[i:i+2] for i in range(0, len(line), 2)]).strip()


def find(name, path):
	for root, dirs, files in os.walk(path):
		if name in files:
			return root,name
	return "",""