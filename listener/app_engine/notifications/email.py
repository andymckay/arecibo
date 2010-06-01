error_msg = """Arecibo is notifying you of the following errors: 
--------------------

%s  
--------------------
You are receiving this because it's the email address set for your account at %s. 

Please remember I'm just a bot and don't really exist, so replying to this email will 
not do you any good I'm afraid.
"""

from google.appengine.api import mail
from django.conf import settings
from app.utils import log

# this seriously needs some test coverage, because at the moment, it doesn't really
# have much

def as_text(error):
    details = ["    Error: %s%s" % (settings.SITE_URL, error.get_absolute_url()), ]
    if error.raw:
        details.append("    URL: %s" % error.raw)
    for key in ("timestamp", "status", "priority", "type", "server"):
        value = getattr(error, key)
        if value:
            details.append("    %s: %s" % (key.capitalize(), value))
    details.append("")
    details = "\n".join(details)
    return details

def send_error_email(holder):
    alot = 10
    data = "\n".join([ as_text(obj) for obj in holder.objs[:alot]])
    count = len(holder.objs)
    if count > 1:
        subject = "Reporting %s errors" % count
    else:
        subject = "Reporting an error"
    if count > alot:
        data += "\n...truncated. For more see the website.\n"
    log("Sending email to: %s of %s error(s)" % (holder.user.email, count))
    mail.send_mail(sender=settings.DEFAULT_FROM_EMAIL,
        to=holder.user.email,
        subject=subject,
        body=error_msg % (data, settings.SITE_URL))