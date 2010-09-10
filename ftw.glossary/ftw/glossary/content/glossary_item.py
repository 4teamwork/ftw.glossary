"""Definition of the GlossaryItem content type.
"""

from zope.interface import implements
from zope.component import adapts

from Products.CMFCore.utils import getToolByName
from Products.Archetypes.interfaces import IObjectPostValidation

from Products.Archetypes import atapi

from Products.ATContentTypes.content import base
from Products.ATContentTypes.content.schemata import finalizeATCTSchema

from ftw.glossary.interfaces import IGlossaryItem
from ftw.glossary.config import PROJECTNAME

from ftw.glossary import GlossarMessageFactory as _

GlossaryItemSchema = base.ATContentTypeSchema.copy() + atapi.Schema((


    atapi.TextField('description',
        required=False,
        searchable=True,
        storage=atapi.AnnotationStorage(),
        validators=('isTidyHtmlWithCleanup',),
        default_output_type='text/x-html-safe',
        widget=atapi.RichWidget(label=_(u"Descriptive text"),
                                description=_(u""),
                                rows=25,
                                allow_file_upload=False),
        ),

    atapi.LinesField('category',
        multiValued=True,
        storage=atapi.AnnotationStorage(),
        vocabulary = ["Foo", "Bar"],
        enforceVocabulary=True,
        widget=atapi.MultiSelectionWidget(label=_(u"One or more categories this term belongs to"),
            description=_(u""))
        ),
    ))

GlossaryItemSchema['title'].storage = atapi.AnnotationStorage()
GlossaryItemSchema['title'].widget.label = _(u"Term")
GlossaryItemSchema['title'].widget.description = _(u"Term to be defined")


finalizeATCTSchema(GlossaryItemSchema, folderish=False, moveDiscussion=False)

class GlossaryItem(base.ATCTContent):
    """Describe a glossary item.
    """
    implements(IGlossaryItem)

    portal_type = "GlossaryItem"
    _at_rename_after_creation = True
    schema = GlossaryItemSchema

    term = atapi.ATFieldProperty('title')
    description = atapi.ATFieldProperty('description')
    category = atapi.ATFieldProperty('category')

atapi.registerType(GlossaryItem, PROJECTNAME)

