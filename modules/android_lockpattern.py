from utils.utils_func import Execmd
from os import path
import hashlib
import multiprocessing
import itertools
import binascii
# Adapted from https://github.com/sch3m4/androidpatternlock

def help():
	config = {
		'type':{'other':['.key']},
		'name':'AndroidLockpattern'
	}
	return config

MATRIX_SIZE = [3,3]
MAX_LEN = MATRIX_SIZE[0]*MATRIX_SIZE[1]
MIN_POSITIONS_NUMBER = 3
FOUND = multiprocessing.Event()


def Load_pattern(path):
	return binascii.hexlify(open(path, 'rb').read(hashlib.sha1().digest_size)).decode()
   	
def Check_Lenght(gest):
	return False if (len(gest) / 2 != hashlib.sha1().digest_size) else True

def lookup(param):
    global FOUND
    lenhash = param[0]
    target = param[1]
    positions = param[2]
    if FOUND.is_set() is True:
        return None
    perms = itertools.permutations(positions, lenhash)
    for item in perms:
        if FOUND.is_set() is True:
            return None
        pattern = ''.join(str(v) for v in item)
        key = binascii.unhexlify(''.join('%02x' % (ord(c) - ord('0')) for c in pattern))
        sha1 = hashlib.sha1(key).hexdigest()
        if sha1 == target:
            FOUND.set()
            return pattern
    return None

def Crack_pattern(target_hash):
    ncores = multiprocessing.cpu_count()
    pool = multiprocessing.Pool(ncores)
    positions = [i for i in range(MAX_LEN)]    
    generate_worker_params = lambda x: [x, target_hash, positions]
    params = [generate_worker_params(i) for i in range(MIN_POSITIONS_NUMBER, MAX_LEN + 1)]    
    result = pool.map(lookup,params)
    pool.close()
    pool.join()    
    ret = None
    for r in result:
        if r is not None:
            ret = r
            break
    return ret

def scan(config):
	config_current = help()

	path1 	= '%s/AndroidLockPattern.txt'%config['env_dir']
	res1 	= ''
	pattern = Load_pattern(config['path'])
	if(Check_Lenght(pattern)):
		cracked = Crack_pattern(pattern)
		if(cracked != None):
			res1 = '[+]Android Pattern Cracked : %s\n\n[+] Gesture:\n  -----  -----  -----\n  | 3 |  | 2 |  | 1 |\n  -----  -----  -----\n  -----  -----  -----\n  | 4 |  | 5 |  | 6 |\n  -----  -----  -----\n  -----  -----  -----\n  | 9 |  | 8 |  | 7 |\n  -----  -----  -----'%cracked
	
	return {"type":"file","path":"","content":res1}
