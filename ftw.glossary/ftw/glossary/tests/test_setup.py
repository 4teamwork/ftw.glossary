import unittest
from ftw.glossary.tests.base import FtwGlossaryTestCase

from Products.CMFCore.utils import getToolByName

class TestSetup(FtwGlossaryTestCase):
    
    def afterSetUp(self):
        self.workflow = getToolByName(self.portal, 'portal_workflow')
        self.acl_users = getToolByName(self.portal, 'acl_users')
        self.types = getToolByName(self.portal, 'portal_types')

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



def test_suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(TestSetup))
    return suite
