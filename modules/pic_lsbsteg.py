#!/usr/bin/python3
# -*- encoding: utf-8 -*-
# Author: Vozec
# CTFiles Scan Project 

from utils.utils_func import Execmd
from os import path
import cv2
from modules.resources.LSBSteg import *
from stegano import lsb
from Crypto import Random
from Crypto.Cipher import AES
from hashlib import sha256
from PIL import Image
import struct

def help():
	config = {
		'type':{'picture':['.png','.jpg']},
		'name':'LsbSteg'
	}
	return config

def cloackedpixel(config,path):
	# https://github.com/livz/cloacked-pixel/blob/master/lsb.py
	if(config['password'] != None):
		def decrypt(enc,key):
			iv = enc[:AES.block_size]
			cipher = AES.new(key, AES.MODE_CBC, iv)
			return unpad(cipher.decrypt(enc[AES.block_size:]))

		def unpad(s):
			return s[:-ord(s[len(s)-1:])]

		def assemble(v):
			bytes_ = ""
			length = len(v)
			for idx in range(0, len(v)//8):
				byte = 0
				for i in range(0, 8):
					if (idx*8+i < length):
						byte = (byte<<1) + v[idx*8+i]
				bytes_ = bytes_ + chr(byte)

			payload_size = struct.unpack("i", bytes(bytes_,'utf-8')[:4])[0] # https://github.com/livz/cloacked-pixel
			return bytes_[4: payload_size + 4]

		key = sha256(bytes(config['password'],'utf-8')).digest()
		img = Image.open(config["path"])
		(width, height) = img.size
		conv = img.convert("RGBA").getdata()
		v = []
		for h in range(height):
			for w in range(width):
				(r, g, b, a) = conv.getpixel((w, h))
				v.append(r & 1)
				v.append(g & 1)
				v.append(b & 1)
		data_out = assemble(v)
		if(len(data_out) > 16):
			# print(v,data_out)
			data_dec = decrypt(data_out,key)

			out_f = open(path, "wb")
			out_f.write(data_dec)
			out_f.close()


def lsbsteg(config,path):
	steg = LSBSteg(cv2.imread(config["path"]))
	data = steg.decode_text()
	if(data != ''):
		f = open(path,'w')
		f.write(data)
		f.close()

def steganolsb(config,path):
	try:
		clear_message = lsb.reveal(config["path"])
		if(clear_message != '' and clear_message != None):
			f = open(path,'w')
			f.write(clear_message)
			f.close()
	except:
		pass

def scan(config):
	config_current = help()

	path1 = '%s/lsbsteg.txt'%config['env_dir']
	path2 = '%s/stegano-lsb.txt'%config['env_dir']
	path3 = '%s/cloacked-pixel_extracted.raw'%config['env_dir']

	lsbsteg(config,path1)
	steganolsb(config,path2)

	if(config['password'] != ''):
		cloackedpixel(config,path3)
	
	result_path = []
	if(path.exists(path1)):	result_path.append('/%s/lsbsteg.txt'%(config['hash']))
	if(path.exists(path2)):	result_path.append('/%s/stegano-lsb.txt'%(config['hash']))
	if(path.exists(path2)):	result_path.append('/%s/cloacked-pixel_extracted.raw'%(config['hash']))

	return {"type":"file","path":result_path,"content":""}
