from zope.interface import Interface
from zope.schema import Choice
from zope.schema import TextLine
from zope.schema.vocabulary import SimpleTerm
from zope.schema.vocabulary import SimpleVocabulary

from zope.i18nmessageid import MessageFactory
_ = MessageFactory('clearwind.arecibo')

arecibo_choices = {
    _(u"Send via http"): "http",
    _(u"Send via email"): "smtp"
}
arecibo_choices_vocab = SimpleVocabulary(
    [SimpleTerm(v, v, k) for k, v in arecibo_choices.items()]
    )
    
class IAreciboConfiguration(Interface):
  """ This interface defines the configlet."""
  account_number = TextLine(title=_(u"Arecibo public account number"),
                                  required=True)
  transport = Choice(title=_(u'Transport'),
                description=_(u"""How errors will be sent to Arecibo, for mail 
                to work, your mail host must be correctly configured."""),
                default='http',
                vocabulary=arecibo_choices_vocab,
                required=False) 