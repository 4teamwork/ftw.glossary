from zope.interface import implements, Interface

from Products.Five import BrowserView
from Products.CMFCore.utils import getToolByName

from ftw.glossary import glossaryMessageFactory as _


class IGlossaryItemView(Interface):
    """
    GlossaryItem view interface
    """

    def test():
        """ test method"""


class GlossaryItemView(BrowserView):
    """
    GlossaryItem browser view
    """
    implements(IGlossaryItemView)

    def __init__(self, context, request):
        self.context = context
        self.request = request

    @property
    def portal_catalog(self):
        return getToolByName(self.context, 'portal_catalog')

    @property
    def portal(self):
        return getToolByName(self.context, 'portal_url').getPortalObject()

