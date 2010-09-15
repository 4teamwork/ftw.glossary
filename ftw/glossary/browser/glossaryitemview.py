from zope.interface import implements, Interface

from Products.Five import BrowserView
from Products.CMFCore.utils import getToolByName

from ftw.glossary import glossaryMessageFactory as _


class IGlossaryItemView(Interface):
    """
    GlossaryItem view interface
    """


class GlossaryItemView(BrowserView):
    """
    GlossaryItem browser view
    """
    implements(IGlossaryItemView)

