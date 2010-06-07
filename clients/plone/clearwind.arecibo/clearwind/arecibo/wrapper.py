import sys
import os 
from lib.arecibo import post, postaddress
from App.config import getConfiguration
from AccessControl import getSecurityManager
from ZODB.POSException import ConflictError
from clearwind.arecibo.interfaces import IAreciboConfiguration

from logging import getLogger
log = getLogger('Plone')

headers = ['HOME', 'HTTP_ACCEPT', 'HTTP_ACCEPT_ENCODING', \
         'HTTP_ACCEPT_LANGUAGE', 'HTTP_CONNECTION', 'HTTP_HOST', 'LANG', \
         'PATH_INFO', 'QUERY_STRING', 'REQUEST_METHOD', 'SCRIPT_NAME', \
         'SERVER_NAME', 'SERVER_PORT', 'SERVER_PROTOCOL', 'SERVER_SOFTWARE']

try:                          
    import site_configuation
    from site_configuration import config
    log("Arecibo configuration read from: %s" % os.path.abspath(site_configuration.__file__))
except:                  
    # please don't override this here, look in site_configuration.py for a chance to 
    # overload this, details are there too
    config = {                                          
        "account": "",
        "transport": "http",
        "priorities": {
            404: 5,
            403: 3,
            500: 1,
        },
        "default-priority": 3,
        "ignores": ["Redirect",]
    }

def get(context):
    # pull first from our default settings above
    # the from site_configuration
    # and finally from the Plone Control Panel
    cfg = config.copy()
    qu = context.getSiteManager().queryUtility(IAreciboConfiguration, name='Arecibo_config')
    if not qu:
        return cfg
    if qu.account_number:
        cfg["account"] = qu.account_number
    if qu.transport == "smtp":
        cfg["transport"] = "smtp"
    return cfg

def arecibo(context, **kw):
    cfg = get(context)
    if kw.get("error_type") in cfg["ignores"]:
        return
         
    if not cfg["account"]: 
        msg = "There is no account number configured so that the error can be sent to Arecibo"
        log.error('Arecibo: %s', msg)
        return
        
    req = context.REQUEST
    error = post()
    
    mail_possible = not not context.MailHost.smtp_host
    if mail_possible and cfg["transport"] == "smtp":
        error.transport = "smtp"
       
    if kw.get("error_type") == 'NotFound':
        status = 404
    elif kw.get("error_type") == 'Unauthorized':
        status = 403
    else:
        status = 500
    
    priority = cfg["priorities"].get(status, cfg["default-priority"])
    
    error.set("account", cfg["account"])
    error.set("priority", priority)
    error.set("user_agent", req.get('HTTP_USER_AGENT', ""))
    
    if req.get("QUERY_STRING"):
        error.set("url", "%s?%s" % (req['ACTUAL_URL'], req['QUERY_STRING']))
    else:
        error.set("url", req['ACTUAL_URL'])

    if kw.get("error_log_id"):
        error.set("uid", kw.get("error_log_id")) 
    
    error.set("ip", req.get("X_FORWARDED_FOR", req.get('REMOTE_ADDR', '')))   
    error.set("type", kw.get("error_type"))
    error.set("status", status)
    error.set("request", "\n".join([ "%s: %s" % (k, req[k]) for k in headers if req.get(k)]))
    
    if status != 404:
        # lets face it the 404 tb is not useful
        error.set("traceback", kw.get("error_tb"))
    
    usr = getSecurityManager().getUser()
    error.set("username", "%s (%s)" % (usr.getId(), usr.getUserName()))
    error.set("msg", kw.get("error_msg"))

    if error.transport == "http":    
        try:
            error.send()
        except ConflictError:
            raise
        except:
            exctype, value = sys.exc_info()[:2]
            msg = "There was an error posting that error to Arecibo via http %s, %s" % (exctype, value)
            log.error('Arecibo: %s', msg)
    elif error.transport == "smtp":
        # use the MailHost to send out which is configured by the site
        # administrator, and has more functionality than straight smtplib
        try:
            context.MailHost.send(error._msg_body())
        except ConflictError:
            raise
        except:
            exctype, value = sys.exc_info()[:2]
            msg = "There was an error posting that error to Arecibo via smtp %s, %s" % (exctype, value)
            log.error('Arecibo: %s', msg)
