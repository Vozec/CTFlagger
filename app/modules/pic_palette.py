#!/usr/bin/python3
# -*- encoding: utf-8 -*-
# Author: Vozec
# CTFlagger

from utils.utils_func import Execmd
from os import path
import os
import numpy as np
from PIL import Image

def help():
	config = {
		'type':{'picture':['.png']},
		'name':'COLOR Palette swap'
	}
	return config

def compute_layers(arr, mode, filename,path):
	for i in range(8):
		newdata = (arr >> i) % 2 * 255
		if mode == 'RGBA':
			newdata[:, :, 3] = 255
		Image.fromarray(newdata, mode).save("%s/%s_%s.png"%(path,filename,i+1))

def scan(config):

	config_current = help()

	path1 = '%s/palette_swap'%config['env_dir']
	path_save = '%s/palette_swap.zip'%config['env_dir']

	if not path.exists(path1):
		os.mkdir(path1)

	# Thanks to @Zeecka : https://github.com/Zeecka/AperiSolve/blob/master/backend/modules/view.py
	img_pil = Image.open(config['path'])
	if img_pil.mode in ["P", "1", "L", "LA", "RGBX", "RGBa", "CMYK", "LAB","YCbCr", "HSV", "I", "F"]:
		img_pil = img_pil.convert('RGBA')
	npimg = np.array(img_pil)
	compute_layers(npimg, img_pil.mode, "image_rgb",path1)  # rgb
	compute_layers(npimg[:, :, 0], 'L', "image_r",path1)  # r
	compute_layers(npimg[:, :, 1], 'L', "image_g",path1)  # g
	compute_layers(npimg[:, :, 2], 'L', "image_b",path1)  # b

	images_name = {}
	images_name["Supperimposed"] = [f"image_rgb_{i+1}.png" for i in range(8)]
	images_name["Red"] 			 = [f"image_r_{i+1}.png" for i in range(8)]
	images_name["Green"] 		 = [f"image_g_{i+1}.png" for i in range(8)]
	images_name["Blue"] 		 = [f"image_b_{i+1}.png" for i in range(8)]

	if img_pil.mode == "RGBA":
		compute_layers(npimg[:, :, 3], 'L', "image_a",path1)
		images_name["Alpha"] = [f"image_a_{i+1}.png" for i in range(8)]


	Execmd('zip -q -r %s/palette_swap.zip %s'%(config['env_dir'],path1))
	
	result_path = ""
	if path.exists(path_save):
		result_path = '/%s/palette_swap.zip'%config['hash']


	for key,value in images_name.items():
		type_filter = {key:[]}
		for img in value:
			path_img = '%s/palette_swap/%s'%(config['env_dir'],img)
			if path.exists(path_img):
				type_filter[key].append('/%s/%s'%(config['hash'],img))


	return {"type":"file","path":result_path,"content":"Module inspired from Aperisolve (Credit: @Zeecka)"}

