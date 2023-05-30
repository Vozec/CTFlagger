#!/usr/bin/python3
# -*- encoding: utf-8 -*-
# Author: Vozec
# CTFlagger

from utils.utils_func import Execmd
from os import path

import numpy
import matplotlib.pyplot as plt
import os
import wave
import pylab
from scipy.io import wavfile
import librosa
import librosa.display
from pydub import AudioSegment
from scipy.fftpack import fft
import random

def help():
	config = {
		'type':{'audio':['.wav','.mp3']},
		'name':'Spectrogram'
	}
	return config

def rdnname():
	return str(random.randint(11111111,99999999))

def spectrogram(path,pathsave):
	result = []

	try:
		samplingFreq, mySound = wavfile.read(path)
		mySoundDataType = mySound.dtype
		mySound = mySound / (2.**15)
		mySoundShape = mySound.shape
		samplePoints = float(mySound.shape[0])
		signalDuration =  mySound.shape[0] / samplingFreq
		mySoundOneChannel = mySound[:,0]
		timeArray = numpy.arange(0, samplePoints, 1)
		timeArray = timeArray / samplingFreq
		timeArray = timeArray * 1000
		plt.plot(timeArray, mySoundOneChannel, color='green')
		plt.xlabel('Time (ms)')
		plt.ylabel('Amplitude')
		plt.savefig('%s/spectro_audio1.png'%pathsave)

		mySoundLength = len(mySound)
		fftArray = fft(mySoundOneChannel)
		numUniquePoints = int(numpy.ceil((mySoundLength + 1) / 2.0))
		fftArray = fftArray[0:numUniquePoints]
		fftArray = abs(fftArray)
		fftArray = fftArray / float(mySoundLength)
		fftArray = fftArray **2
		if mySoundLength % 2 > 0:
			fftArray[1:len(fftArray)] = fftArray[1:len(fftArray)] * 2
		else:
			fftArray[1:len(fftArray) -1] = fftArray[1:len(fftArray) -1] * 2  
		freqArray = numpy.arange(0, numUniquePoints, 1.0) * (samplingFreq / mySoundLength);
		plt.plot(freqArray/1000, 10 * numpy.log10 (fftArray), color='blue')
		plt.xlabel('Frequency (Khz)')
		plt.ylabel('Power (dB)')
		plt.savefig('%s/spectro_audio2.png'%pathsave)
		freqArrayLength = len(freqArray)
		
		numpy.savetxt("%s/freqData.txt"%pathsave, freqArray, fmt='%6.2f')
		numpy.savetxt("%s/fftData.txt"%pathsave, fftArray)


	except Exception as ex:
		pass
	
	try:
		x, sr = librosa.load(path, sr=44100)
		X = librosa.stft(x)
		Xdb = librosa.amplitude_to_db(abs(X))
		plt.figure(figsize=(14, 5))
		librosa.display.specshow(Xdb, sr = sr, x_axis = 'time', y_axis = 'log')
		plt.savefig('%s/spectro_audio3.png'%pathsave)
	except Exception as ex:
		pass

	try:
		x, sr = librosa.load(path, sr=44100)
		X = librosa.stft(x)	
		Xdb = librosa.amplitude_to_db(abs(X))
		plt.figure(figsize=(14, 5))
		librosa.display.specshow(Xdb, sr = sr, x_axis = 'time', y_axis = 'hz')
		plt.savefig('%s/spectro_audio4.png'%pathsave)
	except Exception as ex:
		pass

	try:
		wav = wave.open(path, 'r')
		frames = wav.readframes(-1)
		sound_info = pylab.fromstring(frames, 'int16')
		frame_rate = wav.getframerate()
		wav.close()
		pylab.figure(num=None, figsize=(19, 12))
		pylab.subplot(111)
		pylab.title('spectrogram of %r' % path)
		pylab.specgram(sound_info, Fs=frame_rate)
		pylab.savefig('%s/spectro_audio5.png'%pathsave)
	except Exception as ex:
		pass

	return result

def scan(config):
	config_current = help()

	new_path = "%s/%s.wav"%(config['env_dir'],rdnname())
	Execmd('sox %s  %s'%(config['path'],new_path))
	config['path'] = new_path

	path1 		 = '%s/spectrogram'%config['env_dir']
	pathsave     = '%s/spectrogram.zip'%config['env_dir']

	if(not path.exists(path1)):
		os.mkdir(path1)

	spectrogram(config['path'],path1)

	cmd1  = 'sox %s -n spectrogram;mv spectrogram.png %s/sox_spectrogram.png;'%(config['path'],path1)
	cmd1 += 'zip -q -r %s %s ;'%(pathsave,path1)
	# cmd1 += 'rm -r %s'%path1

	Execmd(cmd1)

	files = []
	for i in range(1,6):
		filename = 'spectro_audio%s.png'%i
		if path.exists('%s/%s/%s'%(config['env_dir'],'spectrogram',filename)):
			files.append('/%s/%s'%(config['hash'],filename))

	for file in [
					pathsave,'%s/spectrogram/fftData.txt'%config['env_dir'],
					'%s/spectrogram/freqData.txt'%config['env_dir'],
					'%s/spectrogram/sox_spectrogram.png'%config['env_dir']
				]:
		if path.exists(file):
			files.append('/%s/%s'%(config['hash'],file.split('/')[-1]))

	return {"type":"file","path":files,"content":""}




#####################
# "config": 
#####################
# env_dir : Directory Created for the scanned filed
# system_tp : linux/windows
# path : File path
# json : Json response required (optional)
# quiet : Use quiet mode ?  (optional)
# password : Password provided (optional)
# iv : Iv provided (hex) (optional)
# formatflag : Format flag (optional)
# module : Module selected (optional)