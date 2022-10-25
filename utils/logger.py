from datetime import datetime
from flask import jsonify,render_template
from time import time

from utils.utils_func import RdnName

class bcolors:
    WHITE = '\033[0m'
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

all_context = {
    'progress':bcolors.HEADER,
    'white':bcolors.WHITE,
    'info':bcolors.WARNING,
    'flag':bcolors.OKGREEN,
    'log':bcolors.OKBLUE,
    'error':bcolors.FAIL,
    'warning':bcolors.OKCYAN,
    '':''
}


def logger(message,context='',newline=0,tab=0,json=False,time=True):
    final = ""
    if(json):
        final = '{"%s":"%s"}'%(context,message)
    else:
        final += '\n'*newline
        if(time):
            now = datetime.now()
            final += now.strftime("%H:%M:%S")
            final += " | "
        final += (all_context[context] if context in all_context.keys() else '')
        final += '\t'*tab
        if(time and tab == 0):
            final += ' '
        final += message
        final += bcolors.ENDC

    print(final)


def Error_handler(msg,API=False,Custom_head='Error'):
    return jsonify({'Error':msg}) if API else render_template('erreur.html',head=Custom_head,msg=msg)

def Error_Internal(Error,CONFIG,use_api=False):
    code = RdnName(6)
    all_error = '%s\nIdentifier : %s\nError at : %s\nError :%s\n%s'%("#"*50,code,str(round(time())),Error,"#"*50)
    open((CONFIG['report']),'a').write(all_error)
    return Error_handler('Please Contact Admin with the Following code : %s'%code,use_api,'Internal Fatal Error')

