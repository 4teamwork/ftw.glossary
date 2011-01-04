import unittest
from ftw.glossary.tests.base import FtwGlossaryTestCase

from Products.CMFCore.utils import getToolByName

class TestContent(FtwGlossaryTestCase):
    
    def afterSetUp(self):
        self.workflow = getToolByName(self.portal, 'portal_workflow')
        self.acl_users = getToolByName(self.portal, 'acl_users')
        self.types = getToolByName(self.portal, 'portal_types')

        self.setRoles(('Manager',))
        self.portal.invokeFactory("Folder", "glossary")

    def test_glossary_item_content(self):
        self.portal.glossary.invokeFactory("GlossaryItem", "www")
        item = self.portal.glossary.www
        item.setTitle("WWW")
        item.setDefinition('World Wide Web')
        self.assertEquals(item.Title(), "WWW")
        self.assertEquals(item.getDefinition(), '<p>World Wide Web</p>')

    def test_glossary_item_content_markup(self):
        self.portal.glossary.invokeFactory("GlossaryItem", "python")
        item = self.portal.glossary.python
        item.setTitle("Python")
        item.setDefinition('A <strong>powerful</strong> object oriented language')
        self.assertEquals(item.Title(), "Python")
        self.assertEquals(item.getDefinition(), 'A <strong>powerful</strong> object oriented language')

    def test_catalog_metadata(self):
        # TODO: Make this test work
        return
        self.portal.glossary.invokeFactory("GlossaryItem", "zodb")
        item = self.portal.glossary.zodb
        item.setTitle("ZODB")
        item.setDefinition('The Zope <em>Object</em> Database')
        self.assertEquals(item.Title(), "ZODB")
        self.assertEquals(item.getDefinition(), 'The Zope <em>Object</em> Database')

        catalog = getToolByName(self.portal, 'glossary_catalog')
        brains = catalog(Title="ZODB")
        self.assertEquals(brains[0].Title(), "ZODB")
        self.assertEquals(brains[0].getDefinition(), 'The Zope <em>Object</em> Database')


def test_suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(TestContent))
    return suite
