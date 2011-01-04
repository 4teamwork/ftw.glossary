from AccessControl import ClassSecurityInfo
from Products.ATContentTypes.content import base
from Products.ATContentTypes.content.schemata import finalizeATCTSchema
from zope.interface import implements
from Products.Archetypes import atapi
from ftw.glossary.interfaces import IGlossaryCategory
from ftw.glossary.config import PROJECTNAME

GlossaryCategorySchema = base.ATContentTypeSchema.copy()
finalizeATCTSchema(GlossaryCategorySchema, folderish=False,
                   moveDiscussion=False)


class GlossaryCategory(base.ATCTContent):
    """A glossary category.
    """
    implements(IGlossaryCategory)

    portal_type = "GlossaryCategory"
    schema = GlossaryCategorySchema
    security = ClassSecurityInfo()


atapi.registerType(GlossaryCategory, PROJECTNAME)
