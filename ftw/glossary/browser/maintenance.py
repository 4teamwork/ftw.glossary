from Acquisition import aq_inner
from Products.Five import BrowserView


class GlossaryMaintenanceView(BrowserView):
    """A browser view for various maintenance tasks.
    """


    def purge_all(self):
        """Deletes all glossary items in the current folder.
        """
        context = aq_inner(self.context)
        item_ids = context.objectIds('GlossaryItem')
        item_count = len(item_ids)
        context.manage_delObjects(ids=item_ids)
        return "Deleted %s items." % (item_count-len(item_ids))

    def index(self):
        """Catalogs all glossary items in the current folder
        """
        context = aq_inner(self.context)
        items = context.objectValues('GlossaryItem')
        for item in items:
            item.indexObject()
        return "Indexed %s items." % len(items)
