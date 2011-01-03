"""Definition of the GlossaryItem content type.
"""

from zope.interface import implements

from Products.Archetypes import atapi

from Products.ATContentTypes.content import base
from Products.ATContentTypes.content.schemata import finalizeATCTSchema

from ftw.glossary.interfaces import IGlossaryItem
from ftw.glossary.config import PROJECTNAME

from ftw.glossary import GlossarMessageFactory as _

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

GlossaryItemSchema['excludeFromNav'].default = True


finalizeATCTSchema(GlossaryItemSchema, folderish=False, moveDiscussion=False)

class GlossaryItem(base.ATCTContent):
    """Describe a glossary item.
    """
    implements(IGlossaryItem)

    portal_type = "GlossaryItem"
    _at_rename_after_creation = True
    schema = GlossaryItemSchema

    def getFirstLetter(self):
        letter = ''
        title = self.Schema().getField('title').get(self)
        for i in range(len(title)):
            letter = title[i].lower()
            if letter.isalnum():
                break
        return letter

    def getSortableTitle(self):
        return self.Title().lower()

atapi.registerType(GlossaryItem, PROJECTNAME)

