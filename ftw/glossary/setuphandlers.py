import logging
from Products.CMFCore.utils import getToolByName

# The profile id of this package:
PROFILE_ID = 'profile-ftw.glossary:default'

# Specify the indexes you want, with ('index_name', 'index_type')
INDEXES = (
    ('Title', 'ZCTextIndex'),
    ('getCategories', 'KeywordIndex'),
    ('getFirstLetter', 'FieldIndex'),
    ('getSortableTitle', 'FieldIndex'),
)

# Metadata columns
METADATA = (
    'Title',
    'getCategories',
    'getDefinition',
)


class Args(object):
    def __init__(self, **kw):
        self.__dict__.update(kw)


def add_catalog_indexes(context, logger=None):
    """Method to add our wanted indexes to the glossary_catalog.

    @parameters:

    When called from the import_various method below, 'context' is
    the plone site and 'logger' is the portal_setup logger.  But
    this method can also be used as upgrade step, in which case
    'context' will be portal_setup and 'logger' will be None.
    """
    if logger is None:
        # Called as upgrade step: define our own logger.
        logger = logging.getLogger('ftw.glossary')

    # Run the toolset.xml step to make sure we already have our
    # glossary_catalog.
    # We could instead add <depends name="toolset"/> to
    # the registration of our import step in zcml, but doing it in
    # code makes this method usable as upgrade step as well.
    setup = getToolByName(context, 'portal_setup')
    setup.runImportStepFromProfile(PROFILE_ID, 'toolset')

    catalog = getToolByName(context, 'glossary_catalog')


    # Add Lexicon
    if 'glossary_lexicon' not in catalog.objectIds():
        catalog.manage_addProduct['ZCTextIndex'].manage_addLexicon(
            'glossary_lexicon',
            elements=[
                Args(group="Word Splitter", name= "HTML aware splitter"),
                Args(group="Case Normalizer", name="Case Normalizer"),
                Args(group="Stop Words", name=" Don't remove stop words")
            ]
        )

    # Add indexes
    indexes = catalog.indexes()
    indexables = []
    for name, meta_type in INDEXES:
        if name not in indexes:
            if meta_type == 'ZCTextIndex':
                extra = Args(doc_attr=name,
                             lexicon_id='glossary_lexicon',
                             index_type='Okapi BM25 Rank')
                catalog.addIndex(name, meta_type, extra=extra)
            else:
                catalog.addIndex(name, meta_type)
            indexables.append(name)
            logger.info("Added %s for field %s.", meta_type, name)
    if len(indexables) > 0:
        logger.info("Indexing new indexes %s.", ', '.join(indexables))
        catalog.manage_reindexIndex(ids=indexables)

    # Add metadata columns
    reindex = False
    for metadata in METADATA:
        if not metadata in catalog.schema():
            catalog.addColumn(metadata)
            reindex = True
    if reindex:
        catalog.manage_reindexIndex()

    # Use glossary_catalog for glossary items.
    at_tool = getToolByName(context, 'archetype_tool')
    at_tool.setCatalogsByType('GlossaryItem', ['glossary_catalog'])


def import_various(context):
    """Miscellanous steps import handle
    """
    if context.readDataFile('ftw.glossary_various.txt') is None:
        return
    
    logger = context.getLogger('ftw.glossary')
    site = context.getSite()
    add_catalog_indexes(site, logger)
