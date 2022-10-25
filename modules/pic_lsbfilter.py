#!/usr/bin/python3
# -*- encoding: utf-8 -*-
# Author: Vozec
# CTFiles Scan Project 

from utils.utils_func import Execmd
from os import path

from PIL import Image

def help():
	config = {
		'type':{'picture':['.png']},
		'name':'LsbFilter'
	}
	return config

def Lsb_filter(in_file):
	img = Image.open(in_file)
	if img.mode in ["P", "1", "L", "LA", "RGBX", "RGBa", "CMYK", "LAB","YCbCr", "HSV", "I", "F"]:
		img = img.convert('RGBA')

	data = list(img.getdata())
	newdata = list()
	for pix in data:
		r,g,b = pix[0],pix[1],pix[2]
		r = (r & 1) << 7
		g = (g & 1) << 7
		b = (b & 1) << 7
		newdata.append((r, g, b))
	new_img = Image.new(img.mode, img.size)
	new_img.putdata(newdata)
	return new_img

def scan(config):
	config_current = help()

	path1 = '%s/lsbfilter.png'%config['env_dir']

	filtered = Lsb_filter(config['path'])
	filtered.save(path1)

	result_path = ""
	if path.exists(path1):
		result_path = '/%s/lsbfilter.png'%(config['hash'])
		
	return {"type":"file","path":result_path,"content":""}