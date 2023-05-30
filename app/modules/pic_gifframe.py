#!/usr/bin/python3
# -*- encoding: utf-8 -*-
# Author: Vozec
# CTFlagger

from utils.utils_func import Execmd
from os import path
from PIL import Image,ImageFile
import glob
import os

ImageFile.LOAD_TRUNCATED_IMAGES = True

def help():
	config = {
		'type':{'picture':['.gif','.apng']},
		'name':'GifFrame'
	}
	return config

def scan(config):
	config_current = help()

	path1	  = '%s/frame_all.zip'%config['env_dir']
	path2	  = '%s/frame_timing.txt'%config['env_dir']
	path_work = '%s/gifpng'%config['env_dir']
	result_path,content = [],""

	if(not path.exists(path_work)):
		os.mkdir(path_work)

	cmd = 'zip -q -r %s %s;'%(path1,path_work)

	duration = []
	with Image.open(config['path']) as im:
		num_key_frames = im.n_frames
		for i in range(num_key_frames):
			im.seek(i)
			duration.append(im.info['duration'])
			im.save('%s/frame_%s.png'%(path_work,i))
			result_path.append('/%s/frame_%s.png'%(config['hash'],i))

	data = 'Frames Duration : \n%s'%str(duration)
	open(path2,'w').write(data)

	Execmd(cmd)		
	
	if path.exists(path1):
		result_path.append('/%s/frame_all.zip'%(config['hash']))
	if path.exists(path2):
		result_path.append('/%s/frame_timing.txt'%(config['hash']))
		content = data

	return {"type":"file","path":result_path,"content":content}
