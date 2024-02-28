# -*- coding: utf-8 -*-
"""
Created on Mon May 15 12:44:31 2023

@author: Matthew
"""

mods = scirun_module_ids()
for module in mods:
    if 'Probe' in module:
        if 'Thal Target' in scirun_get_module_state(module, 'ProbeLabel'):
            target = module
            
targX = scirun_get_module_state(target, 'XLocation')
if targX < 0:
    scirun_set_module_state(target, 'XLocation',targX + -0.5)
else:
    scirun_set_module_state(target, 'XLocation',targX + 0.5)