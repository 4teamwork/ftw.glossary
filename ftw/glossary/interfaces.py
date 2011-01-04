from zope.interface import Interface
from zope import schema
from ftw.glossary import GlossarMessageFactory as _

class IGlossaryItem(Interface):
    """A glossary item

    """
    term = schema.TextLine(title=_(u"label_term", default="Term"),
        required=True)

    description = schema.SourceText(title=_(u"label_description", default="Description"),
        description=_(u"help_description", default="Rich text describing this term"),
        required=True)

    categories = schema.List(title=_(u"label_categories", default="Categories"),
        required=True)


class IGlossaryCategory(Interface):
    """A glossary category.
    """