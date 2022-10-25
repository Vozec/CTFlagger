#!/usr/bin/python3
# -*- encoding: utf-8 -*-
# Author: Vozec
# CTFiles Scan Project 

from utils.utils_func import Execmd
from os import path

def help():
	config = {
		'type':{'picture':['.gif','.jpeg','.jpg','.png','.tiff','.bmp']}, # Prefer to focus on image ext. not all
		'name':'Stegoveritas'
	}
	return config


def scan(config):
	config_current = help()

	cmd  = "ENV_DIR=%s;"%config['env_dir']
	cmd += "TMP_DIR=$ENV_DIR/stegoVeritas;"
	cmd += "mkdir -p $TMP_DIR;"
	cmd += "stegoveritas %s -out $TMP_DIR -meta -imageTransform -colorMap -trailing;"%config['path']
	cmd += "zip -q -r $TMP_DIR/stegoVeritas.zip $TMP_DIR ;"
	cmd += "mv $TMP_DIR/stegoVeritas.zip $ENV_DIR;"
	cmd += "rm -r $TMP_DIR"

	Execmd(cmd)

	path1 = "%s/stegoVeritas.zip"%config['env_dir']
	result_path = '/%s/stegoVeritas.zip'%(config['hash']) if path.exists(path1) else ""

	return {"type":"file","path":result_path,"content":""}
