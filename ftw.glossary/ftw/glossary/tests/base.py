from Products.Five import zcml
from Products.Five import fiveconfigure

from Testing import ZopeTestCase as ztc

from Products.PloneTestCase import PloneTestCase as ptc
from Products.PloneTestCase.layer import onsetup

@onsetup
def setup_ftw_glossary():
    """Set up the additional products required for the ftw.glossary Product.
    
    The @onsetup decorator causes the execution of this body to be deferred
    until the setup of the Plone site testing layer.
    """
    
    # Load the ZCML configuration for the ftw.glossary package.
    
    fiveconfigure.debug_mode = True
    import ftw.glossary
    zcml.load_config('configure.zcml', ftw.glossary)
    fiveconfigure.debug_mode = False
    
    # We need to tell the testing framework that these products
    # should be available. This can't happen until after we have loaded
    # the ZCML.
    
    ztc.installPackage('ftw.glossary')
    
# The order here is important: We first call the (deferred) function which
# installs the products we need for the ftw.glossary package. Then, we let 
# PloneTestCase set up this product on installation.

setup_ftw_glossary()
ptc.setupPloneSite(products=['ftw.glossary'])

class FtwGlossaryTestCase(ptc.PloneTestCase):
    """We use this base class for all the tests in this package. If necessary,
    we can put common utility or setup code in here.
    """