__doc__ = "Extra module loader"

import sys
import os
import imp

##########################

EXTRA_DIR  = "extra"
EXTRA_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(sys.argv[0]))), EXTRA_DIR)

SHARE_DIR  = "share"
SHARE_PATH = os.path.join(EXTRA_PATH, SHARE_DIR)

METHOD_DIR  = "methods"
METHOD_PATH = os.path.join(EXTRA_PATH, METHOD_DIR)

GUI_DIR  = "share"
GUI_PATH = os.path.join(EXTRA_PATH, GUI_DIR)

##########################

def loadFromFile( filepath ):
    mod_name,file_ext = os.path.splitext(os.path.split(filepath)[-1])

    if file_ext.lower() == '.py':
        return imp.load_source(mod_name, filepath)
    elif file_ext.lower() == '.pyc':
        return imp.load_compiled(mod_name, filepath)

    return False

def loadModule( modulePath, moduleName ):
    path = os.path.join(modulePath, moduleName)
    return loadFromFile(path)
