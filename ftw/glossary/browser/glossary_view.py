import json
import zope
from Acquisition import aq_inner

from plone.memoize.view import memoize_contextless
from plone.registry.interfaces import IRegistry
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

    def results():
        """Returns the rendered search results.
        """


class GlossaryView(BrowserView):
    """Glossary browser view - Enable display of and search for terms
    """

    implements(IGlossaryView)

    template = ViewPageTemplateFile('glossary_view.pt')
    results_template = ViewPageTemplateFile('results.pt')

    def __call__(self):
        """Self-submitting form that displays a search field and
           results from the search.
        """
        return self.template()

    def results(self):
        """Returns the rendered search results.
        """
        return self.results_template()

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
        term = term.strip()
        if not term:
            return []
        else:
            response = self.request.response
            response.setHeader('Content-Type','application/json')
            terms = [brain.Title for brain in self._catalog_search(term)]
            return json.dumps(terms)


    def glossary_items(self):
        """Returns a list of all matching glossary items.
        """
        search_term = self.request.form.get('glossary-search-field', '')
        search_letter = self.request.form.get('search_letter', '')

        # We're returning the alphabetical listing
        if search_letter not in ('', None):
            return self._catalog_search(search_letter.lower(), alphabetical=True)

        # We're searching for text
        elif search_term not in ('', None):
            return self._catalog_search(search_term)

        return []

    def categories(self):
        """Returns a sorted list of all available categories.
        """
        voc_factory = queryUtility(IVocabularyFactory, 'ftw.glossary.categories')
        vocabulary = voc_factory(self.context)
        terms = [term for term in vocabulary]
        terms.sort(key=lambda x:x.token)
        return terms

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
