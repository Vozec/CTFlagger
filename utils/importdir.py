# Adapted from https://gitlab.com/aurelien-lourot/importdir/-/blob/master/importdir.py

import os
import re
import sys

def do(path, env):
    sys.path.append(path)
    modules = {}
    for module_name in sorted(get_module_names_in_dir(path)):
        env[module_name] = __import__(module_name)
        # Save module | object + config
        modules[module_name]=(env[module_name],__import__(module_name).help())
    return modules

def get_module_names_in_dir(path):
    result = set()
    for entry in os.listdir(path):
        if os.path.isfile(os.path.join(path, entry)):
            regexp_result = re.search("(.+)\.py(c?)$", entry)
            if regexp_result: # is a module file name
                result.add(regexp_result.groups()[0])
    return result