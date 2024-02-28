# -*- coding: utf-8 -*-
"""
Created on Wed May 10 10:15:06 2023

@author: Matthew
"""

mods = scirun_module_ids()
for module in mods:
    if 'View' in module:
        scirun_set_module_state(module,'__UI__', True)