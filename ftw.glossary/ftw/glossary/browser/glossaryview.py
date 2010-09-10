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

    def search(self, pattern):
        """Return those terms from the catalog that match pattern

        """


class GlossaryView(BrowserView):
    """
    Glossary browser view - Enable display of and search for terms

    """
    implements(IGlossaryView)

    template = ViewPageTemplateFile('glossaryview.pt')

    def __call__(self):
        # TODO: This is an attempt at a self-submitting form, but this method
        #       doesn't seem to get called at all yet.
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

    def search(self, term=None):
        """
        Search for GlossaryItems matching `pattern` and return a JSONified list 

        """
        if term is None:
            return []
        else:
            catalog = getToolByName(self.context, 'portal_catalog')
            terms = [brain.Title for brain in catalog(portal_type='GlossaryItem',
                                                      Title = "%s*" % term)]
            return json.dumps(terms)
