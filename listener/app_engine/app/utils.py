# general utils
import sys
import logging
from django.conf import settings

def log(msg):
    logging.info(" Arecibo: %s" % msg)

def safe_int(key, result=None):
    try:
        return int(key)
    except (ValueError, AttributeError):
        return result

def safe_string(text, result=""):
    try:
        return str(text)
    except (ValueError, AttributeError):
        return result

def _pdb():
    import pdb, sys 
    sys.__stdout__.write('\a') 
    sys.__stdout__.flush() 
    debugger = pdb.Pdb(stdin=sys.__stdin__, stdout=sys.__stdout__) 
    debugger.set_trace()