from zope.interface import Interface
from zope import schema
from ftw.glossary import GlossarMessageFactory as _

class IGlossaryItem(Interface):
    """A glossary item

    """
    term = schema.TextLine(title=_(u"Term"),
        required=True)

    description = schema.SourceText(title=_(u"Description"),
        description=_(u"Rich text describing this term"),
        required=True)

    category = schema.List(title=_(u"Category"),
        required=True)
