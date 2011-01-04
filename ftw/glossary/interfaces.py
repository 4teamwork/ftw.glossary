from zope.interface import Interface


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