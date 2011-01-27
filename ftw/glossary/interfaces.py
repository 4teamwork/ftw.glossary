from zope.interface import Interface
from zope import schema


class IGlossaryItem(Interface):
    """A glossary item
    """


class IGlossaryCategory(Interface):
    """A glossary category.
    """


class IGlossaryMaintencanceView(Interface):
    """A browser view for various maintenance tasks.
    """
    
    def purge_all():
        """Deletes all glossary items in the current folder.
        """

    def index():
        """Catalogs all glossary items in the current folder.
        """

class IGlossarySettings(Interface):
    """Glossary settings"""

    glossary_path = schema.TextLine(
        title = u"Path of the glossary search page",
        default = u"/de/systeme/glossar",
    )
