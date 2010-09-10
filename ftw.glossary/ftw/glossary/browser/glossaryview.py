import json
from zope.interface import implements, Interface

from Products.Five import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile

from Products.CMFCore.utils import getToolByName

from ftw.glossary import glossaryMessageFactory as _


class IGlossaryView(Interface):
    """
    Glossary view interface
    """

    def test():
        """ test method"""


class GlossaryView(BrowserView):
    """
    Glossary browser view
    """
    implements(IGlossaryView)

    template = ViewPageTemplateFile('glossaryview.pt')

    def __call__(self):
        form = self.request.form
        # Make sure we had a proper form submit, not just a GET request
        submitted = form.get('form.submitted', False)

        search_button = form.get('glossary-search-button', None) is not None
        if submitted and search_button:
            # Return search results
            # self.request.response.redirect(self.context.absolute_url())
            return ''
        else:
            return self.template()

    def search(self, pattern):
        """
        Search for GlossaryItems matching `pattern` and return a JSONified list 

        """

        catalog = getToolByName(self.context, 'portal_catalog')
        terms = [brain.term for brain in catalog(portal_type='GlossaryItem')]
        matches = [t for t in terms if t.lower().startswith(pattern.lower())]
        return json.dumps(matches)
