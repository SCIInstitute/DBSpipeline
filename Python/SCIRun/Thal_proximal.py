# -*- coding: utf-8 -*-
"""
Created on Wed Apr 12 08:47:31 2023

@author: Matthew
"""
import math

mods = scirun_module_ids()
for module in mods:
    if 'Probe' in module:
        if 'Thal Target' in scirun_get_module_state(module, 'ProbeLabel'):
            target = module
        if 'Thal Entry' in scirun_get_module_state(module, 'ProbeLabel'):
            entry = module
            
targX = scirun_get_module_state(target, 'XLocation') #Get X,Y,Z coords
targY = scirun_get_module_state(target, 'YLocation')
targZ = scirun_get_module_state(target, 'ZLocation')

entryX = scirun_get_module_state(entry, 'XLocation')
entryY = scirun_get_module_state(entry, 'YLocation')
entryZ = scirun_get_module_state(entry, 'ZLocation')

line_dist = math.sqrt((entryX - targX)**2 + (entryY - targY)**2 + (entryZ - targZ)**2)
#print(line_dist)

v = [entryX - targX, entryY - targY, entryZ - targZ]

v_new = []
for point in v:
    v_new.append(point * 0.5 / line_dist) #Create new vector with length 0.5
#print(v, v_new)

targ_new = [targX + v_new[0], targY + v_new[1], targZ + v_new[2]]
#new_dist = math.sqrt((targ_new[0] - targX)**2 + (targ_new[1] - targY)**2 + (targ_new[2] - targZ)**2)
#print(new_dist)

scirun_set_module_state(target, 'XLocation', targ_new[0]) #Set new target point
scirun_set_module_state(target, 'YLocation', targ_new[1])
scirun_set_module_state(target, 'ZLocation', targ_new[2])