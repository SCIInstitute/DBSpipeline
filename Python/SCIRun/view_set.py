# -*- coding: utf-8 -*-
"""
Created on Wed Mar 22 10:16:34 2023

@author: Matthew
"""

import os

path = os.getcwd()

'''
file = open(path+'\\Transform_Plans\\viewscene_translate.txt','r')
translate = [float(num) for num in file.read().split()]
file.close

file = open(path+'\\Transform_Plans\\viewscene_rotate.txt','r')
rotate = [float(num) for num in file.read().split()]
file.close

file = open(path+'\\Transform_Plans\\viewscene_zoom.txt','r')
zoom = float(file.read())
file.close

mods = scirun_module_ids()
for module in mods:
    if 'View' in module:
        scirun_set_module_state(module, 'CameraLookAt', translate)
        scirun_set_module_state(module, 'CameraRotation', rotate)
        scirun_set_module_state(module, 'CameraDistance', zoom)
        break
'''

file = open(path+'\\Transform_Plans\\viewscene.txt','r')
data = file.readlines()
translate = [float(num) for num in data[0].split(' ')]
rotate = [float(num) for num in data[1].split(' ')]
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