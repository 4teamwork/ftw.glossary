from Acquisition import aq_inner
from ftw.glossary import GlossarMessageFactory as _
from ftw.glossary.interfaces import IGlossarySettings

from plone.app.portlets.portlets import base
from plone.portlets.interfaces import IPortletDataProvider
from plone.registry.interfaces import IRegistry
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile

from zope.component import getMultiAdapter
from zope.component import getUtility
from zope.interface import implements


class IGlossarySearch(IPortletDataProvider):
    """
    """


class Assignment(base.Assignment):
    implements(IGlossarySearch)

    title = _(u'label_glossaryportlet', default=u'Glossary Portlet')


class Renderer(base.Renderer):
    render = ViewPageTemplateFile('search.pt')

    def get_glossary_url(self):
        """Returns the language dependent url of the glossary view.
        """
        context = aq_inner(self.context)
        registry = getUtility(IRegistry)
        settings = registry.forInterface(IGlossarySettings)
        portal = getMultiAdapter((context, self.request),
                                 name=u'plone_portal_state').portal()
        glossary_root = portal.unrestrictedTraverse(
            settings.glossary_path.encode('utf8').lstrip('/')).getTranslation()
        if glossary_root:
            translation = glossary_root.getTranslation()
            if translation:
                return translation.absolute_url()
            return glossary_root.absolute_url()
        return ''

class AddForm(base.NullAddForm):

    def create(self):
        return Assignment()
