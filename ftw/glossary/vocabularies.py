from zope.schema import vocabulary
from zope.schema.interfaces import IVocabularyFactory
from zope.schema.vocabulary import SimpleTerm
from zope.interface import implements
from Products.CMFCore.utils import getToolByName


class GlossaryCategoriesVocabulary(object):
    """A vocabulary of the available categories for
    GlossaryItems.
    """
    implements(IVocabularyFactory)

    def __call__(self, context):
        ct = getToolByName(context, 'portal_catalog')
        categories = ct(portal_type='GlossaryCategory')
        terms = [SimpleTerm(value=c.Title, token=c.id, title=c.Title)
                 for c in categories]
        return vocabulary.SimpleVocabulary(terms)

GlossaryCategoriesVocabularyFactory = GlossaryCategoriesVocabulary()
