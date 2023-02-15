#!/usr/bin/python3
# -*- encoding: utf-8 -*-
# Author: Vozec
# CTFiles Scan Project 

from flask import Flask, render_template,redirect,url_for,request,jsonify,send_from_directory
from werkzeug.utils import secure_filename
from os.path import exists
from shlex import quote

import re
import os
import sqlite3
import sys
import time
import shutil

from utils.logger import *
from utils.utils_func import *
from utils.db_cmd import *
from utils.analyse import Analyse
from utils.render import Result_manager

app = Flask(__name__)

app.config['MAX_CONTENT_LENGHT'] = 16777216
app.static_folder = 'static'

os.chdir(os.path.dirname(__file__))

CONFIG = {
    'dwnl_dir':'/tmp/CTfilesScan',
    'report':'/tmp/CTfilesScan/error.log',
    'db':'files.db',
    'max_thread':10
}

THREADS   = 0
DB_CLIENT = None
modules   = None
ext_word  = [{
        "document":['ASCII text'],
        "binary":['ELF'],
        },
        {
        }
    ]

def Init():
    global modules , ext_word
    if(not exists(CONFIG['dwnl_dir'])):os.makedirs(CONFIG['dwnl_dir'],exist_ok=True)
    if(exists(CONFIG['report'])):os.remove(CONFIG['report'])
    Init_DB()
    modules , ext_word  = Load_modules(ext_word)

def Init_DB():
    global DB_CLIENT
    DB_CLIENT = sqlite3.connect(CONFIG['db'], check_same_thread=False)
    DB_CLIENT.cursor().execute(CMD_create_table)


@app.route("/")
def index():
    return render_template('index.html')


@app.route("/upload", methods=['POST','GET'])
def upload_file():
    global THREADS
    try:
        use_api = Use_api(request)
        file     = request.files.get('files')

        if(file == None):
            return Error_handler('No file uploaded.',use_api)
        elif(THREADS > CONFIG['max_thread']):
            return Error_handler('Too many Scans are in progress, please come back later',use_api)
            
        password  = quote(request.form['password']) \
            if 'password' in request.form.keys() \
                and quote(request.form['password']) != '\'\''\
            else ''

        format_flag = quote(request.form["fflag"]).replace('{','').replace('}','') \
            if 'fflag' in request.form.keys() \
                and quote(request.form['fflag']) != '\'\''\
            else 'flag'


        file_cnt    = file.stream.read()
        ext         = quote(str(os.path.splitext(secure_filename(file.filename))[-1].lower().lstrip(".")))
        filename    = secure_filename(os.path.splitext(file.filename)[0].lower())
        hash_sha1   = Sha1(file_cnt)
        time_up     = round(time.time())


        if(Check_exist(DB_CLIENT,hash_sha1)):
            Update_File(DB_CLIENT,hash_sha1,time_up,password)
        else:
            path_save  = Save(file_cnt,hash_sha1,ext,CONFIG)
            config = {
                'hash':hash_sha1,
                'filename':'%s_original.%s'%(filename,ext),
                'ext':ext,
                'status':'scan',
                'path_up':path_save,
                'first_up':time_up,
                'last_up':time_up,
                'size':Size(path_save),
                'upload_count':1,
                'magic':Magic(path_save),
                'all_password':str([password] if password else []),
                'flag':str([]),
                'result':r'{}',
                'progress':'0'
            }
            c = DB_CLIENT.cursor().execute(CMD_add_file,config)
            DB_CLIENT.commit()

            THREADS += 1
            info     = (hash_sha1,password,format_flag)
            setup    = (DB_CLIENT,CONFIG,THREADS,modules,ext_word)
            Analyse(setup,info)
            THREADS -= 1

        return jsonify({'hash':hash_sha1})

    except Exception as ex:
        print(ex)
        return Error_Internal(ex,CONFIG,use_api)




@app.route('/<hash>', methods=['POST','GET'])
def result_file(hash):
    if re.findall(r"\b[0-9a-f]{5,40}\b", hash):
        API = Use_api(request)
        if(Check_exist(DB_CLIENT,hash)):
            status = Get_Status(DB_CLIENT,hash)
            if(status == 'scan'):
                progress = Get_Progress(DB_CLIENT,hash)
                return Error_handler('The file is being scanned, please wait a few seconds | Progress: %s'%progress,API,'Scan in progress ...')
            else:
                result = Get_Result(DB_CLIENT,hash)
                return ResultToJson(result) if API else Result_manager(result,CONFIG)           
        else:
            return Error_handler('Invalid OR Expired ScanID',API)
    return redirect(url_for('index'))



@app.route('/<hash>/<filename>', methods=['GET'])
def download(hash,filename):
    if re.findall(r"\b[0-9a-f]{5,40}\b", hash):
        API = Use_api(request)
        if(Check_exist(DB_CLIENT,hash)):
            file        = secure_filename(filename)
            directory   = '%s/%s'%(CONFIG['dwnl_dir'],hash)            
            if(exists('%s/%s'%(directory,file))):
                return send_from_directory(directory=directory, path=file, as_attachment=True)
            else:
                found_dir,found_file = find(file,directory)
                if(len(found_file)>0):
                    return send_from_directory(directory=found_dir, path=found_file, as_attachment=True)
            return Error_handler('File not found for this ScanID',API)
        else:
            return Error_handler('Invalid OR Expired ScanID',API)
    return redirect(url_for('index'))



if __name__ == '__main__':
    debug = False
    ssl   = False

    # DEBUG
    if(debug and exists('files.db')):
        os.remove('files.db')
        shutil.rmtree(CONFIG['dwnl_dir'])

    Init()

    if ssl:
        app.run(host='0.0.0.0',debug=debug,port=80,ssl_context='adhoc')
    else:
        app.run(host='0.0.0.0',debug=debug,port=80)
