#!/usr/bin/python3
# -*- encoding: utf-8 -*-
# Author: Vozec
# CTFiles Scan Project 

from utils.utils_func import Execmd
from os import path
import os
from PIL import Image, ImageMath

class LSBDecode():
	def __init__(self, steg, bits, outfile):
		self.bits = bits
		self.outfile = outfile
		self.steg = Image.open(steg)
		if self.steg.mode in ["P", "1", "L", "LA", "RGBX", "RGBa", "CMYK", "LAB","YCbCr", "HSV", "I", "F"]:
			self.steg = self.steg.convert('RGBA')
		self._decode_img()

	def _decode_img(self):
		s = self.steg.split()
		expr = 'convert((s & 2**bits - 1) << (8 - bits), "L")'
		out = [ImageMath.eval(expr, s = s[k], bits = self.bits) for k in range(len(s))] 
		out = Image.merge(self.steg.mode, out)
		out.save(self.outfile)

def help():
	config = {
		'type':{'picture':['.png']},
		'name':'LSB Palette swap'
	}
	return config

def scan(config):

	config_current = help()

	path1 = '%s/lsb_palette_swap'%config['env_dir']
	path_save = '%s/lsb_palette_swap.zip'%config['env_dir']

	if not path.exists(path1):
		os.mkdir(path1)

	result_direct_path = []
	for i in range(8):
		path_img = '%s/lsb_palette_swap/lsb_layer%s.png'%(config['env_dir'],i)
		try:
			LSBDecode(config['path'],i,path_img)
		except:
			pass
		if path.exists(path_img):
			result_direct_path.append('/%s/lsb_layer%s.png'%(config['hash'],i))

	Execmd('zip -q -r %s/lsb_palette_swap.zip %s'%(config['env_dir'],path1))	
	result_path = ""
	if path.exists(path_save):
		result_path = '/%s/lsb_palette_swap.zip'%config['hash']

	return {"type":"file","path":result_path,"direct_path":result_direct_path,"content":""}

