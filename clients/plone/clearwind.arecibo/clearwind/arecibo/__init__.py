from AccessControl import allow_module, allow_class, allow_type
from AccessControl import ModuleSecurityInfo, ClassSecurityInfo

ModuleSecurityInfo('clearwind.arecibo.wrapper').declarePublic('arecibo')

import config
import patch

def initialize(context):
    """Initializer called when used as a Zope 2 product."""