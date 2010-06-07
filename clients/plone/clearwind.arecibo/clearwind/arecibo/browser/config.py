from zope.formlib import form
from Products.Five.formlib import formbase
from plone.app.controlpanel.form import ControlPanelForm 
from clearwind.arecibo.interfaces import IAreciboConfiguration

from zope.i18nmessageid import MessageFactory
_ = MessageFactory('clearwind.arecibo')

class AreciboConfigurationForm(ControlPanelForm):
    form_fields = form.Fields(IAreciboConfiguration)

    description = _(u"Configure Plone to work with your Arecibo account here.")
    form_name = _(u"Arecibo settings")
    label = _(u"Arecibo settings")