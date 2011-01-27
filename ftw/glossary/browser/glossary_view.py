import json
import zope
from AccessControl import getSecurityManager
from Acquisition import aq_inner

from plone.memoize.view import memoize_contextless
from plone.registry.interfaces import IRegistry
from Products.CMFCore import permissions
from Products.CMFCore.utils import getToolByName
from Products.Five import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from ftw.glossary.interfaces import IGlossarySettings

from zope.component import getMultiAdapter
from zope.component import getUtility
from zope.component import queryUtility
from zope.interface import implements, Interface
from zope.schema.interfaces import IVocabularyFactory


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
                jq('.template-glossary_view ul.ui-autocomplete').hide();
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

    template = ViewPageTemplateFile('glossary_view.pt')

    def __call__(self):
        """
        Self-submitting form that displays a search field and
        results from the search
        """
        ajax_url = '/'.join([self.context.absolute_url(),
                             self.__name__,
                             'get_glossary_items'])

        sm = getSecurityManager()
        edit_permission = sm.checkPermission(permissions.ModifyPortalContent,self.context)

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

        if pattern in (None, ''):
            return None
        else:
            pattern = quote_bad_chars(pattern)
            catalog = getToolByName(self.context, 'glossary_catalog')
            categories = self.request.form.get('categories', [])
            query = {}
            
            if categories:
                query['getCategories'] = categories

            if not alphabetical:
                query['Title'] = "%s*" % pattern
            else:
                query['getFirstLetter'] = pattern[:1]

            query['sort_on'] = 'getSortableTitle'
            return catalog(**query)

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
            # FIXME: temporary hack to get all terms in autocomplete.
            # Should be fixed to get only terms of the selected categories.
            self.request.form.update(dict(categories=self.getCategories()))
            terms = [brain.Title for brain in self._catalog_search(term)]
            return json.dumps(terms)

    def get_glossary_items(self, search_term=None, search_letter=None, mode='python'):
        """
        Search for GlossaryItems matching `search_term` or `search_letter`,
        filter the results by category and return either a JSON list or a
        python list (depending on `mode`) of dicts with terms and definitions.
        """
        glossary_items = []
        brains = []

        
        search_term = self.request.get('glossary-search-field')
        search_letter = self.request.get('search_letter')
        mode = self.request.get('mode', 'python')

        # We're returning the alphabetical listing
        if search_letter not in ('', None):
            brains = self._catalog_search(search_letter.lower(), alphabetical=True)

        # We're searching for text
        elif search_term not in ('', None):
            brains = self._catalog_search(search_term)

        # Filter results by category, including only those that match
        for brain in brains:
            glossary_items.append(dict(term=brain.Title,
                                       description=brain.getDefinition,
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
        voc_factory = queryUtility(IVocabularyFactory, 'ftw.glossary.categories')
        vocabulary = voc_factory(self.context)
        values = [term.value for term in vocabulary]
        values.sort()
        return values

    @memoize_contextless
    def glossary_url(self):
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
