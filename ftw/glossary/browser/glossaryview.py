import json
import zope
from AccessControl import getSecurityManager
from ftw.glossary.vocabularies import GlossaryCategories
from Products.CMFCore import permissions
from Products.CMFCore.utils import getToolByName
from Products.Five import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from zope.interface import implements, Interface


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
            var edit_permission = %s;

            var display_results = function(response) {
                var results_html = jq('<dl/>');
                for (var item in response) {
                    if (edit_permission) {
                        var link = jq('<a/>').text(response[item].term);
                        link.attr('href', response[item].url);
                        var term = jq('<dt/>').append(link);
                    }
                    else {
                        var term = jq('<dt/>').html(response[item].term);
                    }
                    results_html.append(term);
                    results_html.append(jq('<dd/>').html(response[item].description));
                }
                jq('div#search-results').html(results_html);
            }

            // Load search results with AJAX
            jq('input[name=glossary-search-button]').click(function(event) {
                event.preventDefault();
                var formdata = jq('#glossaryform').serializeArray();
                formdata.push(new Object({name: 'mode', value: 'json'}));

                jq.getJSON('%s',
                    data=formdata,
                display_results);
            });

            // Load index query results with AJAX
            jq('a.glossary-index-links').click(function(event) {
                event.preventDefault();
                var formdata = jq('#glossaryform').serializeArray();
                formdata.push(new Object({name: 'mode', value: 'json'}));
                formdata.push(new Object({name: 'search_letter', value: jq(this).text()}));

                jq.getJSON('%s',
                    data=formdata,
                display_results);
            });
          
        });
"""

    implements(IGlossaryView)

    template = ViewPageTemplateFile('glossaryview.pt')

    def __call__(self):
        """
        Self-submitting form that displays a search field and
        results from the search
        """
        ajax_url = '/'.join([self.context.absolute_url(), 
                  self.__name__, 
                  'get_glossary_items'])

        edit_permission = getSecurityManager().checkPermission(permissions.ModifyPortalContent,self.context)

        self.ajax_search_js = self.AJAX_SEARCH_JS % (edit_permission and 'true' or 'false', ajax_url, ajax_url)

        return self.template()


    def _catalog_search(self, pattern, alphabetical=False):
        """Search catalog for GlossaryItems matching `pattern`"""

        def quotestring(s):
            return '"%s"' % s

        # We need to quote parentheses when searching text indices
        def quote_bad_chars(s):
            bad_chars = ["(", ")"]
            for char in bad_chars:
                s = s.replace(char, quotestring(char))
            return s

        if pattern is None or pattern == "":
            return None
        else:
            pattern = quote_bad_chars(pattern)
            catalog = getToolByName(self.context, 'portal_catalog')
            if not alphabetical:
                brains = catalog(portal_type='GlossaryItem', Title = "%s*" % pattern, sort_on='sortable_title')
            else:
                if not pattern == '0-9':
                    brains = catalog(portal_type='GlossaryItem', first_letter = pattern, sort_on='sortable_title')
                else:
                    brains = []
                    for digit in range(10):
                        brains += catalog(portal_type='GlossaryItem', first_letter = str(digit), sort_on='sortable_title')
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

    def get_glossary_items(self, search_term=None, search_letter=None, mode='python'):
        """
        Search for GlossaryItems matching `search_term` or `search_letter` 
        and return either a JSON list or a python list (depending on `mode`) 
        of dicts with terms and definitions.

        """

        glossary_items = []

        categories = self.request.get('categories', [])
        search_term = self.request.get('glossary-search-field')
        search_letter = self.request.get('search_letter')
        mode = self.request.get('mode', 'python')

        # We're returning the alphabetical listing
        if search_letter is not None:
            for brain in self._catalog_search(search_letter.lower(), alphabetical=True):
                include = False
                for category in categories:
                    if category in brain.category:
                        include = True
                if include:
                    glossary_items.append(dict(term=brain.Title,
                                           description=brain.Description,
                                           url=brain.getURL()))
        # We're searching for text
        elif search_term not in ('', None):
            for brain in self._catalog_search(search_term):
                include = False
                for category in categories:
                    if category in brain.category:
                        include = True
                if include:
                    glossary_items.append(dict(term=brain.Title,
                                           description=brain.Description,
                                           url=brain.getURL()))
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

    def getCategories(self):
        vocabulary = GlossaryCategories(self.context)
        categories = [term.value for term in vocabulary]
        return categories
