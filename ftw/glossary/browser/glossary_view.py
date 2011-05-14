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
from zopyx.txng3.core.exceptions import LexiconError
from zopyx.txng3.core.parsers.english import QueryParserError


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

    def glossary_items(self):
        """Returns a list of all matching glossary items.
        """
        context = aq_inner(self.context)
        search_term = self.request.form.get('glossary-search-field', '').strip()
        search_index = self.request.form.get('search-index', 'titledefinition')
        search_letter = self.request.form.get('search_letter', '')
        categories = self.request.form.get('categories', [])

        catalog = getToolByName(context, 'glossary_catalog')
        query = {}

        query['sort_on'] = 'getSortableTitle'

        if categories:
            query['getCategories'] = categories
        
        if search_letter:
            query['getFirstLetter'] = search_letter.lower()[:1]
            return catalog(**query)

        if not search_term:
            return []

        # Remove some special characters from search term
        search_term = search_term.replace('/', ' ')
        search_term = search_term.replace('(', ' ')
        search_term = search_term.replace(')', ' ')
        search_term = search_term.replace('-', ' ')
        search_term = search_term.replace('+', ' ')
        search_term = search_term.replace(',', ' ')
        search_term = search_term.replace('.', ' ')
        search_term = search_term.replace(';', ' ')
        search_term = search_term.replace(':', ' ')
        search_term = search_term.replace('&', ' ')        
        search_term = search_term.strip()

        if search_index == 'title':
            query['glossaryText'] = dict(query=search_term, field='title')
        elif search_index == 'definition':
            query['glossaryText'] = dict(query=search_term, field='definition')
        else:
            query['glossaryText'] = dict(query=search_term, search_all_fields=1)
        
        try:
            return catalog(**query)
        except (QueryParserError, LexiconError):
            return []

    def matching_terms(self, term=None):
        """
        Search for GlossaryItems matching `term` and return a JSON list
        of just the terms to be used by jquery.ui.autocomplete()
        """
        term = term.strip()
        if not term.endswith('*'):
            term = '%s*' % term
        self.request.form.update({'glossary-search-field':term, 'search-index': 'title'})
        response = self.request.response
        response.setHeader('Content-Type','application/json')
        terms = [brain.Title for brain in self.glossary_items()[:50]]
        return json.dumps(terms)

    def form_submitted(self):
        """Returns true if the search form was submitted.
        """
        if self.request.form.get('search_letter', False):
            return False
        return self.request.form.get('form.submitted', False)

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
