sample_500_body = """Traceback (most recent call last):
  
  File "/Users/andy/svn/private/sites/arecibo_marketing/django/core/handler=
s/base.py", line 92, in get_response
    response =3D callback(request, *callback_args, **callback_kwargs)
  
  File "/Users/andy/svn/private/sites/arecibo_marketing/app/views.py", line=
 6, in sample_500
    1/0

ZeroDivisionError: integer division or modulo by zero


<WSGIRequest
GET:<QueryDict: {}>,
POST:<QueryDict: {}>,
COOKIES:{'__utma': '111872281.1161894572.1274903003.1275942811.1276115922.1=
7',
 '__utmb': '111872281.13.10.1276115922',
 '__utmc': '111872281',
 '__utmz': '111872281.1274903003.1.1.utmcsr=3D(direct)|utmccn=3D(direct)|ut=
mcmd=3D(none)',
 'dev_appserver_login': 'test@example.com:False:185804764220139124118',
 'sessionid': '2f5e00247239b613e51017ab204e7419'},
META:{'Apple_PubSub_Socket_Render': '/tmp/launch-RML1Hs/Render',
 'CA_XLOG_KEY': '12a',
 'COMMAND_MODE': 'unix2003',
 'CONTENT_LENGTH': '',
 'CONTENT_TYPE': 'text/plain'
 'HTTP_HOST': 'localhost:8000',
 'HTTP_USER_AGENT': 'Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_3; en-us) AppleWebKit/531.22.7 (KHTML, like Gecko) Version/4.0.5 Safari/531.22.7',
 'LANG': 'en_CA.UTF-8',
 'LOGNAME': 'andy',
 'OLDPWD': '/Users/andy/svn/private/sites',
 'PATH': '/opt/local/bin:/opt/local/sbin:/opt/local/bin:/opt/local/sbin:/Developer/Air/bin:/usr/bin:/bin:/usr/sbin:/sbin:/usr/local/bin:/usr/local/git/bin:/usr/X11/bin',
 'PATH_INFO': u'/error/sample_500',
 'PWD': '/Users/andy/svn/private/sites/arecibo_marketing',
 'QUERY_STRING': '',
 'REMOTE_ADDR': '127.0.0.1',
 'REMOTE_HOST': '',
 'REQUEST_METHOD': 'GET',
 'RUN_MAIN': 'true',
 'SCRIPT_NAME': u'',
 'SERVER_NAME': 'elrond.local',
 'SERVER_PORT': '8000',
 'SERVER_PROTOCOL': 'HTTP/1.1',
 'SERVER_SOFTWARE': 'WSGIServer/0.1 Python/2.6.1',
 'SHELL': '/bin/bash',
 'SHLVL': '1',
 'SSH_AUTH_SOCK': '/tmp/launch-dvJUky/Listeners',
 'TERM': 'xterm-color',
 'TERM_PROGRAM': 'Apple_Terminal',
 'TERM_PROGRAM_VERSION': '273',
 'TMPDIR': '/var/folders/rh/rhfbya9IFjWeiQ2YkrQoCU+++TI/-Tmp-/',
 'TM_PYCHECKER': 'pylint',
 'TZ': 'America/Vancouver',
 'USER': 'andy',
 'VERSIONER_PYTHON_PREFER_32_BIT': 'no',
 'VERSIONER_PYTHON_VERSION': '2.6',
 '_': '/usr/bin/python',
 '__CF_USER_TEXT_ENCODING': '0x1F5:0:0',
 'wsgi.errors': <open file '<stderr>', mode 'w' at 0x1001c5140>,
 'wsgi.file_wrapper': <class 'django.core.servers.basehttp.FileWrapper'>,
 'wsgi.input': <socket._fileobject object at 0x101053578>,
 'wsgi.multiprocess': False,
 'wsgi.multithread': True,
 'wsgi.run_once': False,
 'wsgi.url_scheme': 'http',
 'wsgi.version': (1, 0)}>
"""

sample_404_body = """Referrer: None
Requested URL: /error/awkdjhga?asd
User agent: Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_3; en-us) AppleW=
ebKit/531.22.7 (KHTML, like Gecko) Version/4.0.5 Safari/531.22.7
IP address: 127.0.0.1
"""

sample_404_body_parsed = {'url': '/error/awkdjhga?asd',
    'ip': '127.0.0.1',
    'request': 'HTTP_REFERER: None',
    'user_agent': 'Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_3; en-us) AppleWebKit/531.22.7 (KHTML, like Gecko) Version/4.0.5 Safari/531.22.7'
}


from mail_django import parse_404, parse_500

from django.test import TestCase

class ErrorTests(TestCase):
    # test the view for writing errors
    def testBasic(self):
        result = parse_404(sample_404_body)
        result = parse_500(sample_500_body)
