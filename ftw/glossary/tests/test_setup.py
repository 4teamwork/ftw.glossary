from Products.CMFCore.utils import getToolByName

from ftw.glossary.tests import FunctionalTestCase


class TestSetup(FunctionalTestCase):

    def setUp(self):
        super(TestSetup, self).setUp()
        self.grant('Manager')

        self.workflow = getToolByName(self.portal, 'portal_workflow')
        self.acl_users = getToolByName(self.portal, 'acl_users')
        self.types = getToolByName(self.portal, 'portal_types')

        self.portal.invokeFactory("Folder", "glossary")

    def test_add_glossary_item_permissions(self):
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
        self.grant('Manager')
        self.portal.glossary.invokeFactory("GlossaryItem", "html")
        item = self.portal.glossary.html
        item.setTitle("HTML")
        item.setDefinition("Hyper Text Markup Language")
        self.assertEquals(item.Title(), "HTML")
        self.assertEquals(item.getDefinition(), '<p>Hyper Text Markup Language</p>')
