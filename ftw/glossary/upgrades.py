import logging
from ftw.glossary.setuphandlers import add_catalog_indexes
from Products.CMFCore.utils import getToolByName

logger = logging.getLogger('ftw.glossary')


def migrate_to_textindexng3(context):
    catalog = getToolByName(context, 'glossary_catalog')
    indexes = catalog.indexes()

    # remove ZCTextIndex indexes
    if 'Title' in indexes:
        logger.info("Removing index 'Title'.")
        catalog.delIndex('Title')
    if 'getDefinition' in indexes:
        logger.info("Removing index 'getDefinition'.")
        catalog.delIndex('getDefinition')
    
    # remove lexicon
    if 'glossary_lexicon' in catalog.objectIds():
        logger.info("Removing glossary lexicon.")
        catalog.manage_delObjects(['glossary_lexicon',])
    
    add_catalog_indexes(context)


