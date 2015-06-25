"""Effectively does a "from sage.all import *" on the imported
module. Designed to be imported/called in an external sage session."""

import importlib, sys
def attach_sage(module):
    attrs = {}
    sage_mod = importlib.import_module("sage.all")
    #do this rather than __dict__ to avoid binding private vars
    for attr in filter(lambda a: a[0] != '_', dir(sage_mod)):
        sys.modules[module].__dict__[attr] = getattr(sage_mod, attr)
