from utils.utils_func import Execmd
from os import path
from docopt import docopt
import midi

# From https://github.com/maxcruz/stegano_midi/blob/master/stegano-midi.py

def help():
	config = {
		'type':{'audio':['.mid']},
		'name':'Stegano-Midi'
	}
	return config

def Reveal(midi_file):
	tracks = midi.read_midifile(midi_file)
	secrets = {}
	secret_index = 0
	forget_indexes = list()
	for event in tracks[0]:
		i = 0
		if isinstance(event, midi.NoteOnEvent) and event.tick == 0 and event.get_pitch() == midi.G_3:
			secrets[secret_index] = list()
			forget_indexes.append(i)
		if isinstance(event, midi.ProgramChangeEvent) and event.tick == 0:
			secrets[secret_index].append(event.data[0])
			forget_indexes.append(i)
		if isinstance(event, midi.NoteOffEvent) and event.tick == 0 and event.get_pitch() == midi.G_3:
			secret_index += 1
			forget_indexes.append(i)
		i += 1
	for i in secrets:
		secret = ''
		for char in reversed(secrets[i]):
			secret = secret + chr(char)
		return secret
	return ''

def Save(data,filename):
	f = open(filename,'wb')
	f.write(data)
	f.close()

def scan(config):
	config_current = help()

	path1 = '%s/stegano-midi.txt'%config['env_dir']
	
	res = Reveal(config['path'])

	result_path = ''
	if(res != ""):
		Save(res,path1)
		result_path = '/%s/stegano-midi.txt'%config['hash']
	
	return {"type":"file","path":result_path,"content":res}