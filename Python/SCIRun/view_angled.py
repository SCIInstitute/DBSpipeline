# -*- coding: utf-8 -*-
"""
Created on Thu May 11 09:44:15 2023

@author: Matthew
"""

file = open(path+'\\Transform_Plans\\viewscene.txt','r')
data = file.readlines()
translate = [float(num) for num in data[0].split(' ')]
rotate = [1.0, 1.0, 1.0, 0.0]
zoom = float(data[2])
winX = float(data[3])
winY = float(data[4])

mods = scirun_module_ids()
for module in mods:
    if 'View' in module:
        scirun_set_module_state(module, 'CameraLookAt', translate)
        scirun_set_module_state(module, 'CameraRotation', rotate)
        scirun_set_module_state(module, 'CameraDistance', zoom)
        scirun_set_module_state(module, 'WindowSizeX', winX)
        scirun_set_module_state(module, 'WindowSizeY', winY)
        scirun_set_module_state(module,'__UI__', False)
        break

file.close