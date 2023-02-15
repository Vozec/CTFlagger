#!/usr/bin/python3
# -*- encoding: utf-8 -*-
# Author: Vozec
# CTFiles Scan Project 

import sqlite3
import time
from os.path import exists
import shutil

db_client = sqlite3.connect('files.db', check_same_thread=False)
max_time  = 3600 * 24 # 1 Day
base_path = '/tmp/CTfilesScan/'

def main():
	# Fetch All
	cmd = "SELECT hash FROM files WHERE last_up < %s"%(round(time.time()) - (max_time))
	res = db_client.cursor().execute(cmd).fetchall()

	# Remove All From Database & Remove files
	for h in res:
		db_client.cursor().execute("DELETE FROM files WHERE hash = '%s'"%(h[0]))
		if exists(base_path+h[0]):
			shutil.rmtree(base_path+h[0])

	# Commit
	db_client.commit()


if __name__ == "__main__":
	main()