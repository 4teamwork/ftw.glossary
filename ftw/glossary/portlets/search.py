from zope.interface import implements
from plone.portlets.interfaces import IPortletDataProvider
from plone.app.portlets.portlets import base
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile


class IGlossarySearch(IPortletDataProvider):
    """
    """


class Assignment(base.Assignment):
    implements(IGlossarySearch)


class Renderer(base.Renderer):
    render = ViewPageTemplateFile('search.pt')


class AddForm(base.NullAddForm):

    def create(self):
        return Assignment()
