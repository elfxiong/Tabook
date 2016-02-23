"""
Settings used by Tabook_models project.
This consists of the general production settings, with an optional import of any local
settings.
"""

# Import production settings.
from Tabook_models.settings.production import *

# Import optional local settings.
try:
    from Tabook_models.settings.local import *
except ImportError:
    pass
