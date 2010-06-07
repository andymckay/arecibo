import transaction
from Products.CMFCore.utils import getToolByName
from Products.CMFCore.DirectoryView import createDirectoryView
from clearwind.arecibo.interfaces import IAreciboConfiguration
from clearwind.arecibo.config import AreciboConfiguration

EXTENSION_PROFILES = ('clearwind.arecibo:default',)

def uninstall(self):
    """ Uninstall """
    cp = getToolByName(self, 'portal_controlpanel')
    if "arecibo" in [ c.id for c in cp._actions ]:
        cp.unregisterConfiglet("arecibo")


def install(self, reinstall=False):
    """ We still have to do this? """
    
    portal_quickinstaller = getToolByName(self, 'portal_quickinstaller')
    portal_setup = getToolByName(self, 'portal_setup')

    sm = self.getSiteManager()

    if not sm.queryUtility(IAreciboConfiguration, 
        name='Arecibo_config'):
        sm.registerUtility(AreciboConfiguration(),
                           IAreciboConfiguration,
                           'Arecibo_config')

    for extension_id in EXTENSION_PROFILES:
        portal_setup.runAllImportStepsFromProfile('profile-%s' % extension_id, purge_old=False)
        product_name = extension_id.split(':')[0]
        portal_quickinstaller.notifyInstalled(product_name)
        transaction.savepoint()