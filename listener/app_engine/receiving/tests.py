sample_500_body = """Traceback (most recent call last):

File "/data/amo_python/www/prod/zamboni/vendor/src/django/django/core/handlers/base.py", line 100, in get_response
  response = callback(request, *callback_args, **callback_kwargs)

File "/data/amo_python/www/prod/zamboni/apps/users/views.py", line 78, in confirm_resend
  user.email_confirmation_code()

File "/data/amo_python/www/prod/zamboni/apps/users/models.py", line 254, in email_confirmation_code
  t.render(Context(c)), None, [self.email])

File "/data/amo_python/www/prod/zamboni/vendor/src/django/django/core/mail/__init__.py", line 61, in send_mail
  connection=connection).send()

File "/data/amo_python/www/prod/zamboni/vendor/src/django/django/core/mail/message.py", line 175, in send
  return self.get_connection(fail_silently).send_messages([self])

File "/data/amo_python/www/prod/zamboni/vendor/src/django/django/core/mail/backends/smtp.py", line 85, in send_messages
  sent = self._send(message)

File "/data/amo_python/www/prod/zamboni/vendor/src/django/django/core/mail/backends/smtp.py", line 101, in _send
  email_message.message().as_string())

File "/usr/lib/python2.6/smtplib.py", line 709, in sendmail
  raise SMTPRecipientsRefused(senderrs)

SMTPRecipientsRefused: {u'runnoex@hotmail.com': (553, 'Requested mail action aborted: Mailbox name has been suppressed.')}


<WSGIRequest
GET:<QueryDict: {}>,
POST:<QueryDict: {}>,
COOKIES:{'WT_FPC': 'id=25780a0ac63c363510a1290112372929:lv=1290112451748:ss=1290112372929',
'amo_home_promo_seen': '1',
'csrftoken': '35224bac87f70725a34afc8a97aa50d1',
'wtspl': '967280'},
META:{'CSRF_COOKIE': '35224bac87f70725a34afc8a97aa50d1',
'DOCUMENT_ROOT': '/data/www/addons.mozilla.org-remora/site/app/webroot',
'GATEWAY_INTERFACE': 'CGI/1.1',
'HTTPS': 'on',
'HTTP_ACCEPT': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
'HTTP_ACCEPT_CHARSET': 'ISO-8859-1,utf-8;q=0.7,*;q=0.7',
'HTTP_ACCEPT_ENCODING': 'gzip,deflate',
'HTTP_ACCEPT_LANGUAGE': 'pt-br,pt;q=0.8,en-us;q=0.5,en;q=0.3',
'HTTP_CONNECTION': 'Keep-Alive',
'HTTP_COOKIE': 'csrftoken=35224bac87f70725a34afc8a97aa50d1; WT_FPC=id=25780a0ac63c363510a1290112372929:lv=1290112451748:ss=1290112372929; wtspl=967280; amo_home_promo_seen=1',
'HTTP_HOST': 'addons.mozilla.org',
'HTTP_KEEP_ALIVE': '115',
'HTTP_REFERER': 'https://addons.mozilla.org/pt-BR/firefox/users/login',
'HTTP_SSLCLIENTCERTSTATUS': 'NoClientCert',
'HTTP_SSLCLIENTCIPHER': 'SSL_RSA_WITH_RC4_128_SHA, version=SSLv3, bits=128',
'HTTP_SSLSESSIONID': 'D76B89BB968FE44847A97FA889B9EA6F169D2A7B6A7B85EB11858851DA23DB47',
'HTTP_USER_AGENT': 'Mozilla/5.0 (Windows; U; Windows NT 5.1; pt-BR; rv:1.9.2.12) Gecko/20101026 Firefox/3.6.12',
'HTTP_X_CLUSTER_CLIENT_IP': '63.245.213.6',
'HTTP_X_FORWARDED_FOR': '201.73.138.6, 63.245.213.6',
'HTTP_X_ZEUS_DL_PT': '552612',
'PATH_INFO': u'/pt-BR/firefox/user/5550302/confirm/resend',
'PATH_TRANSLATED': '/data/amo_python/www/prod/zamboni/wsgi/zamboni.wsgi/pt-BR/firefox/user/5550302/confirm/resend',
'QUERY_STRING': '',
'REMOTE_ADDR': '201.73.138.6',
'REMOTE_PORT': '62955',
'REQUEST_METHOD': 'GET',
'REQUEST_URI': '/pt-BR/firefox/user/5550302/confirm/resend',
'SCRIPT_FILENAME': '/data/amo_python/www/prod/zamboni/wsgi/zamboni.wsgi',
'SCRIPT_NAME': u'',
'SCRIPT_URI': 'http://addons.mozilla.org/pt-BR/firefox/user/5550302/confirm/resend',
'SCRIPT_URL': '',
'SERVER_ADDR': '10.2.83.17',
'SERVER_ADMIN': 'webmaster@mozilla.com',
'SERVER_NAME': 'addons.mozilla.org',
'SERVER_PORT': '80',
'SERVER_PROTOCOL': 'HTTP/1.1',
'SERVER_SIGNATURE': '',
'SERVER_SOFTWARE': 'Apache',
'datetime': '2010-11-18 19:34:48.900860',
'hostname': 'pm-app-amo05',
'is-forwarded': '1',
'mod_wsgi.application_group': 'addons.mozilla.org|/z',
'mod_wsgi.callable_object': 'application',
'mod_wsgi.handler_script': '',
'mod_wsgi.input_chunked': '0',
'mod_wsgi.listener_host': '',
'mod_wsgi.listener_port': '81',
'mod_wsgi.process_group': 'zamboni_prod',
'mod_wsgi.request_handler': 'wsgi-script',
'mod_wsgi.script_reloading': '1',
'mod_wsgi.version': (3, 3),
'wsgi.errors': <mod_wsgi.Log object at 0xc6d09d0>,
'wsgi.file_wrapper': <built-in method file_wrapper of mod_wsgi.Adapter object at 0xc961890>,
'wsgi.input': <mod_wsgi.Input object at 0xc6d0b60>,
'wsgi.loaded': datetime.datetime(2010, 11, 18, 19, 31, 15, 188526),
'wsgi.multiprocess': True,
'wsgi.multithread': False,
'wsgi.run_once': False,
'wsgi.url_scheme': 'https',
'wsgi.version': (1, 1)}>
_______________________________________________
Amo-tracebacks mailing list
Amo-tracebacks@mozilla.org
https://mail.mozilla.org/listinfo/amo-tracebacks
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
        result = parse_404(sample_404_body, "")
        result = parse_500(sample_500_body, "")
