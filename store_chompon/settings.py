# http://lethain.com/entry/2008/nov/03/development-to-deployment-in-django/
#from settings_production import *
from settings_devel import *

# Can override if needed
try:
    from settings_local import *
except ImportError:
    pass
