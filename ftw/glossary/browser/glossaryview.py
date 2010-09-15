import json
import zope
from zope.interface import implements, Interface

from Products.Five import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile

from Products.CMFCore.utils import getToolByName

#from ftw.glossary import glossaryMessageFactory as _

# TODO: 
# - Implement categories
# - List / search only published GlossaryItems?
# - Search currently matches for each word invididually for multi-word terms
#       instead of the beginning of the whole term
# - Correctly declare search_term

class IGlossaryView(Interface):
    """
    Glossary view interface

    """
    search_term = zope.interface.Attribute("Search Term")

    def matching_terms(self, term):
        """
        Return a list of those terms from the catalog that match `term`.

        """

    def get_glossary_items(self, search_term=None, mode='python'):
        """
        Search for GlossaryItems matching `self.search_term` and return
        either a JSON list or a python list (depending on `mode`) of
        dicts with terms and definitions.

        """



class GlossaryView(BrowserView):
    """
    Glossary browser view - Enable display of and search for terms

    """
    AJAX_SEARCH_JS = """
        jq(function() {
                jq('input[name=glossary-search-button]').click(function(event) {
          event.preventDefault();
          jq.getJSON('%s', 
                     data={search_term:jq('input[name=glossary-search-field]').val(),
                           mode:'json'},
                     function(response) {
                         var results_html = jq('<dl/>');
                         for (var item in response) {
                             results_html.append(jq('<dt/>').append(response[item].term));
                             results_html.append(jq('<dd/>').append(response[item].description));
                         }
                         jq('div#search-results').html(results_html);
                     });
          });
        }
    );"""

    implements(IGlossaryView)

    template = ViewPageTemplateFile('glossaryview.pt')

    def __call__(self):
        """
        Self-submitting form that displays a search field and
        results from the search
        
        """
        self.ajax_search_js = self.AJAX_SEARCH_JS % (
            '/'.join([self.context.absolute_url(), 
                      self.__name__, 
                      'get_glossary_items']))

        form = self.request.form
        self.search_term = ''

        # Make sure we had a proper form submit, not just a GET request
        submitted = form.get('form.submitted', False)
        search_button = form.get('glossary-search-button', None) is not None
        if submitted and search_button:
            # Set search_term, to be used by get_glossary_items()
            self.search_term = form.get('glossary-search-field', '')
        return self.template()


    def _catalog_search(self, pattern):
        """Search catalog for GlossaryItems matching `pattern`"""
        if pattern is None or pattern == "":
            return None
        else:
            catalog = getToolByName(self.context, 'portal_catalog')
            brains = catalog(portal_type='GlossaryItem',
                             Title = "%s*" % pattern)
            return brains

    def matching_terms(self, term=None):
        """
        Search for GlossaryItems matching `term` and return a JSON list
        of just the terms to be used by jquery.ui.autocomplete()

        """
        if term is None:
            return []
        else:
            response = self.request.response
            response.setHeader('Content-Type','application/json')
            response.addHeader("Cache-Control", "no-cache")
            response.addHeader("Pragma", "no-cache")
            terms = [brain.Title for brain in self._catalog_search(term)]
            return json.dumps(terms)

    def get_glossary_items(self, search_term=None, mode='python'):
        """
        Search for GlossaryItems matching `self.search_term` and return
        either a JSON list or a python list (depending on `mode`) of
        dicts with terms and definitions.

        """
        if search_term is not None:
            self.search_term = search_term
        glossary_items = []
        if self.search_term != '':
            for brain in self._catalog_search(self.search_term):
                glossary_items.append(dict(term=brain.Title,
                                           description=brain.description))
            if mode == 'python':
                return glossary_items
            elif mode == 'json':
                response = self.request.response
                response.setHeader('Content-Type','application/json')
                response.addHeader("Cache-Control", "no-cache")
                response.addHeader("Pragma", "no-cache")
                return json.dumps(glossary_items)
            else:
                return []
