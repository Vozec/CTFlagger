from utils.utils_func import Execmd
from os import path
from oletools.olevba import VBA_Parser,VBA_Scanner, TYPE_OLE, TYPE_OpenXML, TYPE_Word2003_XML, TYPE_MHTML

def help():
	config = {
		'type':{'document':['.dotm','.docm','.doc','.dot','.xls','.xlsm','.xlsb','.pptm','.ppsm','.opc','.xml','.mht','.pub','.slk','.odt','docx']}, #  All extension
		'name':'Olevba'
	}
	return config


def scan(config):
	config_current = help()

	path1 = '%s/Olevba.txt'%config['env_dir']

	data = ""
	vbaparser = VBA_Parser(config['path'], data=open(config['path'], 'rb').read())
	
	if vbaparser.detect_vba_macros() or 1==1: # detect_vba_macros() bugged idk why

		for (filename, stream_path, vba_filename, vba_code) in vbaparser.extract_macros():
			data  = '-'*79+'\n'
			data += "Filename    : %s\n"%filename
			data += "OLE stream  : %s\n"%stream_path
			data += "VBA filename: %s\n"%vba_filename
			data += '- '*39+'\n'
			data += vba_code+'\n'
			data += '-'*79+'\n'


		results = vbaparser.analyze_macros()
		for kw_type, keyword, description in results:
		    data += 'type=%s - keyword=%s - description=%s\n' % (kw_type, keyword, description)

		results = VBA_Scanner(vbaparser.reveal()).scan(include_decoded_strings=True)
		for kw_type, keyword, description in results:
		    data +=  'type=%s - keyword=%s - description=%s\n' % (kw_type, keyword, description)

		data += 'AutoExec keywords: %d\n' % vbaparser.nb_autoexec
		data += 'Suspicious keywords: %d\n' % vbaparser.nb_suspicious
		data += 'IOCs: %d\n' % vbaparser.nb_iocs
		data += 'Hex obfuscated strings: %d\n' % vbaparser.nb_hexstrings
		data += 'Base64 obfuscated strings: %d\n' % vbaparser.nb_base64strings
		data += 'Dridex obfuscated strings: %d\n' % vbaparser.nb_dridexstrings
		data += 'VBA obfuscated strings: %d\n' % vbaparser.nb_vbastrings
		data += '-'*79+'\n'
		data += 'Macro Decoded :\n'
		data += vbaparser.reveal()+'\n'
		data += '-'*79+'\n'

	vbaparser.close()

	if data != "":
		f = open(path1,'w')
		f.write(data)
		f.close()

	result_path = []	
	if(path.exists(path1)):
		result_path.append('/%s/%s'%(config['hash'],path1.split('/')[-1]))

	return {"type":"file","path":result_path,"content":data}
