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


    atapi.TextField('description',
        required=False,
        accessor='Description',
        validators=('isTidyHtmlWithCleanup',),
        default_output_type='text/x-html-safe',
        widget=atapi.RichWidget(label=_(u"label_description", default="Description"),
                                description=_(u"help_description", default="Rich text describing this term"),
                                rows=25,
                                allow_file_upload=False),
        ),

    atapi.LinesField('category',
        multiValued=True,
        vocabulary = ["Foo", "Bar"],
        enforceVocabulary=True,
        widget=atapi.MultiSelectionWidget(label=_(u"label_category", 
            default="Category"),
            description=_(u"help_category", default="One or more categories this term belongs to")
            )
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

    def first_letter(self):
        letter = ''
        title = self.Schema().getField('title').get(self)
        for i in range(len(title)):
            letter = title[i].lower()
            if letter.isalnum():
                break
        return letter


atapi.registerType(GlossaryItem, PROJECTNAME)

