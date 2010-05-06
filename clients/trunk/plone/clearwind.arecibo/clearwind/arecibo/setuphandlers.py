from Products.CMFCore.DirectoryView import createDirectoryView
from Products.CMFCore.utils import getToolByName
from Products.CMFPlone.interfaces import ISelectableConstrainTypes
from Products.CMFEditions.setuphandlers import DEFAULT_POLICIES
import string

def setupSkins(portal):
    def add(portal, name, location):
        portal_skins = getToolByName(portal, "portal_skins")
        if name not in portal_skins.objectIds():
            createDirectoryView(portal_skins, location, name)
    
        skins = portal_skins.getSkinSelections()
        for skin in skins:
            path = portal_skins.getSkinPath(skin)
            path = [ p.strip() for p in path.split(',') ]
            if name not in path:
                if 'custom' in path:
                    pos = path.index('custom') + 1
                else:
                    pos = 0
                path.insert(pos, name)
                path = ", ".join(path)
                portal_skins.addSkinSelection(skin, path)
    
    add(portal, "arecibo", "clearwind.arecibo:skins")    

def importVarious(context): 
    if context.readDataFile("clearwind.arecibo.txt") is None:
        return
    portal = context.getSite()
    setupSkins(portal)
