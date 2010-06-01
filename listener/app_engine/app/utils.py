# general utils
import sys
import logging
from django.conf import settings

def log(msg):
    logging.info(" Arecibo: %s" % msg)

def safe_string(text):
    try:
        return str(text)
    except (ValueError, AttributeError):
        return ""