"""Definition of the GlossaryItem content type.
"""
import re
from zope.interface import implements
from zope.component import getUtility
from Products.Archetypes import atapi
from Products.ATContentTypes.content import base
from Products.ATContentTypes.content.schemata import finalizeATCTSchema
from Products.CMFPlone.utils import safe_unicode
from plone.i18n.normalizer.interfaces import IIDNormalizer
from plone.i18n.normalizer.base import UNIDECODE_LIMIT
from ftw.glossary.interfaces import IGlossaryItem
from ftw.glossary.config import PROJECTNAME
from ftw.glossary import GlossarMessageFactory as _
from zopyx.txng3.core.content import IndexContentCollector
from zopyx.txng3.core.interfaces import IIndexableContent


GlossaryItemSchema = base.ATContentTypeSchema.copy() + atapi.Schema((

    atapi.TextField('definition',
        required=False,
        validators=('isTidyHtmlWithCleanup',),
        default_content_type='text/html',
        allowable_content_types=('text/html',),
        default_output_type='text/html',
        widget=atapi.RichWidget(
            label=_(u"label_definition", default="Definition"),
            description=_(u"help_definition", default="Rich text describing this term"),
            rows=25,
            allow_file_upload=False,
        ),
    ),

    atapi.LinesField('categories',
        multiValued=True,
        vocabulary_factory = 'ftw.glossary.categories',
        enforceVocabulary=True,
        widget=atapi.MultiSelectionWidget(
            label=_(u"label_categories", default="Categories"),
            description=_(u"help_categories", default="One or more categories this term belongs to"),
        ),
    ),

))

GlossaryItemSchema['title'].widget.label = _(u"label_term", default="Term")
GlossaryItemSchema['title'].widget.description = _(u"help_term", default="Term to be defined")
GlossaryItemSchema['description'].widget.visible = {'view': 'invisible', 'edit': 'invisible'}
GlossaryItemSchema['excludeFromNav'].default = True


finalizeATCTSchema(GlossaryItemSchema, folderish=False, moveDiscussion=False)

class GlossaryItem(base.ATCTContent):
    """Describe a glossary item.
    """
    implements(IGlossaryItem, IIndexableContent)

    portal_type = "GlossaryItem"
    _at_rename_after_creation = True
    schema = GlossaryItemSchema

    def getFirstLetter(self):
        """Returns the first letter of the glossary term for indexing.
        """
        for letter in self.normalizedTitle():
            if letter.isalpha():
                return letter.lower()
            # Index all digits as '0' because we treat them as the same first letter.
            elif letter.isdigit():
                return '0'
        # Terms without an alphanumeric character should show up somewhere
        return '0'

    def getSortableTitle(self):
        """Normalizes the glossary term for sorting.
        """
        # Code taken from sortable_title indexer in Products.CMFPlone.CatalogTool.py
        sortabletitle = self.normalizedTitle()
        # Replace numbers with zero filled numbers
        sortabletitle = num_sort_regex.sub(zero_fill, sortabletitle)
        # Truncate to prevent bloat
        sortabletitle = safe_unicode(sortabletitle)[:70].encode('utf-8')
        # Remove dashes. Sortable title should contain only characters and digits.
        sortabletitle = sortabletitle.replace('-', '')
        return sortabletitle

    def normalizedTitle(self):
        """Returns a normalized title that doesn't contain non-ascii
           characters.
        """
        normalizer = getUtility(IIDNormalizer)
        title = self.Title().strip().decode('utf8')
        # remove chars above unidecode limit of id normalizer
        title = u''.join([ch for ch in title if ord(ch)<UNIDECODE_LIMIT])
        return normalizer.normalize(title)

    def indexableContent(self, fields):
        """Returns index data for TextIndexNG3.
        """
        icc = IndexContentCollector()
        if 'definition' in fields:
            icc.addContent('definition', self.getDefinition(mimetype='text/plain').decode('utf8'), self.Language())
        if 'title' in fields:
            icc.addContent('title', self.Title().decode('utf8'), self.Language())
        return icc


def zero_fill(matchobj):
    return matchobj.group().zfill(6)

num_sort_regex = re.compile('\d+')


atapi.registerType(GlossaryItem, PROJECTNAME)

