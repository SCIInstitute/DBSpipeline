# -*- coding: utf-8 -*-
"""
Created on Mon May 15 12:33:47 2023

@author: Matthew
"""

mods = scirun_module_ids()
for module in mods:
    if 'Probe' in module:
        if 'Thal Target' in scirun_get_module_state(module, 'ProbeLabel'):
            target = module
            
targY = scirun_get_module_state(target, 'YLocation')
scirun_set_module_state(target, 'YLocation',targY + -0.5)