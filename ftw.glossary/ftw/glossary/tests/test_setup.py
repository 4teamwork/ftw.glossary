import unittest
from ftw.glossary.tests.base import FtwGlossaryTestCase

from Products.CMFCore.utils import getToolByName

class TestSetup(FtwGlossaryTestCase):
    
    def afterSetUp(self):
        self.workflow = getToolByName(self.portal, 'portal_workflow')
        self.acl_users = getToolByName(self.portal, 'acl_users')
        self.types = getToolByName(self.portal, 'portal_types')
        
        self.setRoles(('Manager',))
        self.portal.invokeFactory("Folder", "glossary")
        self.setRoles(('Member',))
        

    def test_add_glossary_item_permissison(self):
        # The API of the permissionsOfRole() function sucks - it is bound too
        # closely up in the permission management screen's user interface
        roles = ['Manager', 'Editor', 'Contributor']
        for r in roles:
            selected_permissions = [p['name'] for p in 
                                    self.portal.permissionsOfRole(r) if p['selected']]
            self.failUnless('ftw.glossary: Add GlossaryItem' in selected_permissions)
            
    def test_glossary_item_installed(self):
        self.failUnless('GlossaryItem' in self.types.objectIds())
        
    def test_glossary_item_fti(self):
        document_fti = getattr(self.types, 'GlossaryItem')
        self.failUnless(document_fti.global_allow)
        
    def test_glossary_item_creation(self):
        self.setRoles(('Manager',))
        self.portal.glossary.invokeFactory("GlossaryItem", "html")
        item_html = self.portal.glossary.html
        item_html.term = "HTML"
        item_html.description = "Hyper Text Markup Language"
        self.assertEquals(item_html.term, "HTML")
        self.assertEquals(item_html.description, "Hyper Text Markup Language")


def test_suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(TestSetup))
    return suite
