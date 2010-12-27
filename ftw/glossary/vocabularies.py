from zope.schema import vocabulary
from zope.schema.interfaces import IVocabularyFactory
from zope.schema.vocabulary import SimpleTerm
from zope.interface import directlyProvides

def GlossaryCategories(context):
    """Returns a vocabulary of the available categories for
    GlossaryItems.
    """
    # context is the portal config options, whose context is the portal
    categories = ['Allgemein', 'Annabelle']
    terms = [SimpleTerm(value=c, token=c, title=c)
            for c in categories]

    directlyProvides(GlossaryCategories, IVocabularyFactory)
    return vocabulary.SimpleVocabulary(terms)
