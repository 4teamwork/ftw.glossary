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

    def matching_terms(self, term):
        """
        Return those terms from the catalog that match pattern

        """
    def search_results(self):
        """
        Search for GlossaryItems matching `self.search_term` and return a
        list of dicts with terms and definitions

        """




class GlossaryView(BrowserView):
    """
    Glossary browser view - Enable display of and search for terms

    """
    implements(IGlossaryView)

    template = ViewPageTemplateFile('glossaryview.pt')

    def __call__(self):
        """
        Self-submitting form that displays a search field and
        results from the search
        """
        form = self.request.form
        self.search_term = ''

        # Make sure we had a proper form submit, not just a GET request
        submitted = form.get('form.submitted', False)
        search_button = form.get('glossary-search-button', None) is not None
        if submitted and search_button:
            # Set search_term, to be used by search_results()
            self.search_term = form.get('glossary-search-field', '')
        return self.template()

    def matching_terms(self, term=None):
        """Search for GlossaryItems matching `term` and return a JSON list"""
        if term is None:
            return []
        else:
            catalog = getToolByName(self.context, 'portal_catalog')
            terms = [brain.Title for brain in catalog(
                portal_type='GlossaryItem',
                Title = "%s*" % term)]
            return json.dumps(terms)

    def search_results(self):
        """
        Search for GlossaryItems matching `self.search_term` and return a
        list of dicts with terms and definitions

        """
        results = []
        if self.search_term != '':
            catalog = getToolByName(self.context, 'portal_catalog')
            for brain in catalog(portal_type='GlossaryItem',
                                 Title = "%s*" % self.search_term):
                results.append(dict(term=brain.Title,
                                    description=brain.description))
        return results

